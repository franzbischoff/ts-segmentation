"""ECG dataset preprocessing utilities translated from the R scripts (find_all_files.R, read_ecg.R, pre_process.R).

Features implemented:
 - File discovery for regime datasets (persistent_afib/per, paroxysmal_afib/par, non_afib/non)
 - Reading WFDB style .hea headers + compressed signal CSV (.csv.bz2) + annotation CSV (.atr.csv.bz2)
 - Extraction of sampling frequency, signal names, gains/baselines (minimal subset actually required)
 - Regime change extraction from annotation label codes (28, 32, 33) as in read_ecg.R
 - Optional resampling from original frequency (often 200 Hz) to target (e.g. 250 Hz) using linear interpolation
 - Cleaning of regime indices (deduplicate near events, drop events too close to edges) mirroring clean_truth()
 - Construction of a tidy DataFrame with columns: id, sample_index, ecg (selected lead), regime_change
 - CLI similar to R pre_process.R allowing class filtering and signal selection

Assumptions / Simplifications:
 - We select a single ECG lead (default 'II'). If not present, we fall back to the first signal column.
 - Header parsing: we only need frequency and signal count; detailed per-signal meta lines are kept simple.
 - Annotation CSV is assumed to contain at least columns: 'sample', 'label_store' (following R code usage).
 - Signal CSV columns are all numeric channel columns; first one corresponds to first signal definition line, etc.
 - Events (regimes) are kept as integer sample indices relative to (possibly resampled) series.

Future extensions:
 - Multi-lead selection and retention
 - Additional regime categories (vtach, etc.) via CLI flags
 - Caching of parsed headers
"""

from __future__ import annotations

import argparse
import bz2
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

import numpy as np
import pandas as pd


# -----------------------------
# Header / file discovery
# -----------------------------

REGIME_CLASS_SUFFIXES = {
    'persistent_afib': '.per',
    'paroxysmal_afib': '.par',
    'non_afib': '.non',
}

REGIME_LABEL_CODES = {28, 32, 33}  # as in R read_ecg.R (afib_regimes + malignantventricular)


def find_all_files(path: str | Path, classes: Sequence[str], limit_per_class: int | None = None) -> List[Path]:
    """Replicates logic of find_all_files.R for the 'regimes' dataset.

    We look for .hea files whose basename ends with the class suffix pattern.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    classes = list(classes)
    if 'all' in classes:
        pattern = '*.hea'
        files = sorted(path.rglob(pattern))
        return files

    selected: List[Path] = []
    for cls in classes:
        suffix = REGIME_CLASS_SUFFIXES.get(cls)
        if not suffix:
            raise ValueError(f"Unsupported class: {cls}")
        # pattern like *.<per|par|non>.hea
        pattern = f"*{suffix}.hea"
        matches = sorted(path.rglob(pattern))
        if limit_per_class is not None:
            matches = matches[:limit_per_class]
        selected.extend(matches)
    return selected


# -----------------------------
# Reading records
# -----------------------------

HEAD_LINE_RE = re.compile(r"^(?P<record>\S+)\s+(?P<n_sig>\d+)\s+(?P<fs>\d+)")


@dataclass
class ECGRecord:
    record_id: str
    fs: int
    signals: pd.DataFrame  # columns = signal names
    annotations: pd.DataFrame | None
    regimes: np.ndarray  # cleaned regime change indices (may be empty)


def _parse_header(hea_path: Path) -> tuple[int, List[str]]:
    content = hea_path.read_text().splitlines()
    # skip comment lines (starting with '#')
    non_comment = [ln for ln in content if ln and not ln.startswith('#')]
    if not non_comment:
        raise ValueError(f"Header empty: {hea_path}")
    m = HEAD_LINE_RE.search(non_comment[0])
    if not m:
        raise ValueError(f"Cannot parse head line in {hea_path}: {non_comment[0]}")
    n_sig = int(m.group('n_sig'))
    fs = int(m.group('fs'))
    # Subsequent n_sig lines describe signals; first token often like <file>/<fmt> ... we create generic names S1..Sn
    signal_names: List[str] = []
    for i in range(n_sig):
        if i + 1 >= len(non_comment):
            signal_names.append(f'S{i+1}')
        else:
            sig_line = non_comment[i + 1]
            # try to extract suggested name from like: 212 200/200(0)/mV 16 0 0 -32768 0 ECG
            parts = sig_line.split()
            if parts:
                candidate = parts[-1]
                # basic sanitation
                candidate = re.sub('[^A-Za-z0-9_]+', '', candidate)
                if candidate:
                    signal_names.append(candidate)
                    continue
            signal_names.append(f'S{i+1}')
    return fs, signal_names


def _read_signal_csv(csv_bz2: Path, n_signals: int) -> pd.DataFrame:
    with bz2.open(csv_bz2, 'rb') as fh:
        data = fh.read()
    # Try without header; some files may already include a header row of text.
    df = pd.read_csv(io.BytesIO(data), header=None, low_memory=False)
    # Coerce every column to numeric (invalid parsing -> NaN) to avoid object dtypes.
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    # Drop fully NaN columns (e.g., if a textual header slipped in)
    df = df.dropna(axis=1, how='all')
    # If the first row still has many NaNs suggesting a header line, try reread with header=0
    if df.head(1).isna().mean(axis=1).iloc[0] > 0.5:
        df2 = pd.read_csv(io.BytesIO(data))  # let pandas infer header
        # Coerce again
        for c in df2.columns:
            df2[c] = pd.to_numeric(df2[c], errors='coerce')
        # Prefer df2 if it produced more numeric columns
        if df2.select_dtypes(include=[float, int]).shape[1] >= df.select_dtypes(include=[float, int]).shape[1]:
            df = df2
        # Drop any non-numeric columns now
        non_num = [c for c in df.columns if not np.issubdtype(df[c].dtype, np.number)]
        df = df.drop(columns=non_num)
    # Keep only the first n_signals numeric columns
    df = df.iloc[:, :n_signals]
    # Final safety: fill remaining NaN (isolated) with forward fill then back fill, else zero
    if df.isna().any().any():
        df = df.ffill().bfill().fillna(0.0)
    return df


def _read_annotation_csv(atr_bz2: Path) -> pd.DataFrame:
    if not atr_bz2.exists():
        return None  # type: ignore
    with bz2.open(atr_bz2, 'rb') as fh:
        data = fh.read()
    ann = pd.read_csv(io.BytesIO(data))
    # Expect at least 'sample' and 'label_store'
    if 'sample' not in ann.columns:
        # attempt to find a column named similarly
        for c in ann.columns:
            if c.lower().startswith('sample'):
                ann.rename(columns={c: 'sample'}, inplace=True)
                break
    return ann


# -----------------------------
# Resampling & cleaning
# -----------------------------

def resample_signal(df: pd.DataFrame, orig_fs: int, target_fs: int) -> pd.DataFrame:
    if orig_fs == target_fs:
        return df
    factor = target_fs / orig_fs
    n_orig = len(df)
    n_new = int(round(n_orig * factor))
    new_index = np.linspace(0, n_orig - 1, n_new)
    resampled = {}
    for col in df.columns:
        series = df[col].to_numpy(dtype=float, copy=False)
        resampled[col] = np.interp(new_index, np.arange(n_orig), series)
    return pd.DataFrame(resampled)


def clean_truth(truth: Sequence[int], data_size: int, first: bool = True, last: bool = True) -> np.ndarray:
    """Mirror R clean_truth: remove events within 15 samples of each other; drop edges."""
    if last and data_size is None:
        raise ValueError("data_size must be provided when last is True")
    truth = np.sort(np.asarray(truth, dtype=int))
    if truth.size == 0:
        return truth
    # deduplicate near events (< =15 apart) keeping first occurrence
    keep_mask = np.concatenate(([True], np.diff(truth) > 15))
    truth = truth[keep_mask]
    if first and truth.size and truth[0] <= 10:
        truth = truth[1:] if truth.size > 1 else np.array([1])
    if last and truth.size and truth[-1] >= (data_size - 10):
        truth = truth[:-1] if truth.size > 1 else np.array([data_size])
    return truth


def build_regime_changes(annotations: pd.DataFrame | None) -> np.ndarray:
    if annotations is None or 'label_store' not in annotations.columns:
        return np.array([], dtype=int)
    mask = annotations['label_store'].isin(REGIME_LABEL_CODES)
    pts = annotations.loc[mask, 'sample'].astype(int).to_numpy()
    return np.sort(pts)


def load_record(hea_path: Path, resample_to: int | None = None) -> ECGRecord:
    fs, signal_names = _parse_header(hea_path)
    csv_path = hea_path.with_suffix('.csv.bz2')
    atr_path = hea_path.with_suffix('.atr.csv.bz2')
    sig_df = _read_signal_csv(csv_path, len(signal_names))
    annotations = _read_annotation_csv(atr_path)
    regimes_raw = build_regime_changes(annotations)
    if resample_to:
        orig_len = len(sig_df)
        sig_df = resample_signal(sig_df, fs, resample_to)
        # adjust regime indices to new sample space by proportional mapping
        if regimes_raw.size:
            regimes_raw = (regimes_raw * (len(sig_df) / orig_len)).round().astype(int)
        fs = resample_to
    regimes_clean = clean_truth(regimes_raw, len(sig_df)) if regimes_raw.size else regimes_raw
    sig_df.columns = signal_names[: sig_df.shape[1]]
    return ECGRecord(record_id=hea_path.stem, fs=fs, signals=sig_df, annotations=annotations, regimes=regimes_clean)


# -----------------------------
# Tidy dataset construction
# -----------------------------

def build_tidy(records: List[ECGRecord], lead: str = 'II') -> pd.DataFrame:
    rows = []
    for rec in records:
        if rec.signals.empty:
            continue
        # choose lead
        if lead in rec.signals.columns:
            ecg = rec.signals[lead].to_numpy()
        else:
            ecg = rec.signals.iloc[:, 0].to_numpy()
        regime_vec = np.zeros_like(ecg, dtype=int)
        if rec.regimes.size:
            regime_vec[np.clip(rec.regimes, 0, len(ecg) - 1)] = 1
        df_part = pd.DataFrame({
            'id': rec.record_id,
            'sample_index': np.arange(len(ecg), dtype=int),
            'ecg': ecg,
            'regime_change': regime_vec,
        })
        rows.append(df_part)
    if not rows:
        return pd.DataFrame(columns=['id', 'sample_index', 'ecg', 'regime_change'])
    return pd.concat(rows, ignore_index=True)


# -----------------------------
# CLI
# -----------------------------

def parse_args():
    p = argparse.ArgumentParser(description='Convert WFDB regime ECG collection into tidy CSV for streaming drift detection.')
    p.add_argument('--root', required=True, help='Root folder containing .hea/.csv.bz2/.atr.csv.bz2 files')
    p.add_argument('--classes', nargs='+', default=['all'], help='Subset of classes (all, persistent_afib, paroxysmal_afib, non_afib)')
    p.add_argument('--limit-per-class', type=int, default=None, help='Limit number of files per class')
    p.add_argument('--lead', default='II', help='ECG lead to extract (fallback to first if missing)')
    p.add_argument('--resample-to', type=int, default=250, help='Target sampling rate (Hz); if different from original, linear resample applied')
    p.add_argument('--output', required=True, help='Output CSV path')
    return p.parse_args()


def main():
    args = parse_args()
    hea_files = find_all_files(args.root, args.classes, args.limit_per_class)
    if not hea_files:
        raise SystemExit('No header files found.')
    records: List[ECGRecord] = []
    for h in hea_files:
        try:
            rec = load_record(h, resample_to=args.resample_to)
            if rec.regimes.size == 0:  # drop records with no regime change
                continue
            records.append(rec)
        except Exception as e:  # noqa
            # Skip problematic file but continue
            print(f"[WARN] Failed {h.name}: {e}")
    tidy = build_tidy(records, lead=args.lead)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    tidy.to_csv(args.output, index=False)
    print(f"Wrote {len(tidy)} rows from {len(records)} records to {args.output}")


if __name__ == '__main__':  # pragma: no cover
    main()
