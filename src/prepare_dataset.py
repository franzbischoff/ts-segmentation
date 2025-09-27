from __future__ import annotations
import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def build_regime_change_column(df: pd.DataFrame, events_df: pd.DataFrame | None,
                               sample_rate: int, events_col_index: str | None,
                               events_col_time: str | None) -> pd.Series:
    rc = np.zeros(len(df), dtype=int)
    if events_df is None:
        return pd.Series(rc)
    if events_col_index and events_col_index in events_df.columns:
        idxs = events_df[events_col_index].astype(int).tolist()
        for i in idxs:
            if 0 <= i < len(rc):
                rc[i] = 1
    elif events_col_time and events_col_time in events_df.columns and 'timestamp' in df.columns:
        # map times to nearest sample_index
        t_series = df['timestamp']
        for t in events_df[events_col_time]:
            # nearest index (assuming sorted)
            idx = (np.abs(t_series - t)).argmin()
            rc[idx] = 1
    return pd.Series(rc)


def parse_args():
    ap = argparse.ArgumentParser(description='Preparar dataset ECG para pipeline streaming')
    ap.add_argument('--input', required=True, help='CSV de entrada com sinal')
    ap.add_argument('--output', required=True, help='CSV de saída normalizado')
    ap.add_argument('--ecg-col', default='ecg', help='Nome da coluna do sinal')
    ap.add_argument('--timestamp-col', default=None, help='Nome da coluna de timestamp (opcional)')
    ap.add_argument('--events-csv', default=None, help='CSV com eventos de mudança')
    ap.add_argument('--events-col-index', default=None, help='Coluna no events-csv com índices de mudança')
    ap.add_argument('--events-col-time', default=None, help='Coluna no events-csv com tempos de mudança')
    ap.add_argument('--sample-rate', type=int, default=250, help='Frequência de amostragem')
    ap.add_argument('--zscore', action='store_true', help='Aplicar z-score ao sinal')
    return ap.parse_args()


def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    if args.timestamp_col and args.timestamp_col in df.columns:
        df = df.sort_values(args.timestamp_col).reset_index(drop=True)
        df['sample_index'] = np.arange(len(df))
        df.rename(columns={args.timestamp_col: 'timestamp'}, inplace=True)
    else:
        if 'sample_index' not in df.columns:
            df['sample_index'] = np.arange(len(df))

    if args.ecg_col not in df.columns:
        raise SystemExit(f"Coluna {args.ecg_col} não encontrada no dataset.")

    df.rename(columns={args.ecg_col: 'ecg'}, inplace=True)

    events_df = None
    if args.events_csv:
        events_df = pd.read_csv(args.events_csv)

    df['regime_change'] = build_regime_change_column(df, events_df, args.sample_rate,
                                                     args.events_col_index, args.events_col_time)

    if args.zscore:
        mu = df['ecg'].mean()
        sigma = df['ecg'].std(ddof=0) or 1.0
        df['ecg'] = (df['ecg'] - mu) / sigma

    out_cols = ['sample_index', 'ecg', 'regime_change']
    if 'timestamp' in df.columns:
        out_cols.insert(1, 'timestamp')

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df[out_cols].to_csv(args.output, index=False)
    print(f"Dataset preparado em {args.output} ({len(df)} linhas)")


if __name__ == '__main__':
    main()
