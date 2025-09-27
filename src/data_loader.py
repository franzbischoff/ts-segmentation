import os
import pandas as pd
import numpy as np
from typing import Tuple, Optional

SAMPLE_RATE_DEFAULT = 250

def generate_synthetic_ecg(
    path: str,
    n_segments: int = 5,
    segment_length: int = 1000,
    sample_rate: int = SAMPLE_RATE_DEFAULT,
    seed: int = 42,
    amplitude_shift_range: Tuple[float, float] = (0.25, 0.5),
    noise_range: Tuple[float, float] = (0.02, 0.05),
) -> str:
    """Generate a synthetic ECG-like signal with clearer regime changes.

    Changes introduced per regime:
      - Additive baseline shift (cumulative) to alter mean level.
      - Amplitude and noise adjustments.
    This increases detectability for mean-shift based detectors (PageHinkley, ADWIN).
    """
    rng = np.random.default_rng(seed)
    samples = []
    current_index = 0
    cumulative_shift = 0.0
    for seg in range(n_segments):
        # Each segment we shift the baseline further
        if seg > 0:
            cumulative_shift += rng.uniform(*amplitude_shift_range) * rng.choice([-1, 1])
        base_amp = 0.8 + 0.4 * rng.random()
        noise = rng.uniform(*noise_range)
        heart_rate_hz = 1.1 + 0.5 * rng.random()
        t = np.arange(segment_length) / sample_rate
        waveform = (
            cumulative_shift
            + base_amp * np.sin(2 * np.pi * heart_rate_hz * t)
            + 0.15 * np.sin(2 * np.pi * 2 * heart_rate_hz * t + 0.5)
            + 0.05 * np.sin(2 * np.pi * 3 * heart_rate_hz * t + 1.2)
        )
        waveform += rng.normal(0, noise, size=segment_length)
        for i in range(segment_length):
            samples.append(
                {
                    'sample_index': current_index,
                    'ecg': waveform[i],
                    'regime_change': 1 if i == 0 and seg > 0 else 0,
                }
            )
            current_index += 1
    df = pd.DataFrame(samples)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path

def load_dataset(
    csv_path: Optional[str],
    sample_rate: int = SAMPLE_RATE_DEFAULT,
    force_regenerate: bool = False,
    n_segments: int = 5,
    segment_length: int = 1000,
) -> Tuple[pd.DataFrame, int]:
    """Load dataset; if not exists (or forced) create synthetic with parameters.

    Returns (dataframe, sample_rate)
    """
    synthetic_default = os.path.join('data', 'synthetic_ecg.csv')
    if force_regenerate and csv_path is None:
        if os.path.exists(synthetic_default):
            os.remove(synthetic_default)
    if csv_path is None:
        csv_path = synthetic_default
    if force_regenerate or not os.path.exists(csv_path):
        generate_synthetic_ecg(csv_path, n_segments=n_segments, segment_length=segment_length, sample_rate=sample_rate)
    df = pd.read_csv(csv_path)
    if 'sample_index' not in df.columns:
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp').reset_index(drop=True)
            df['sample_index'] = np.arange(len(df))
        else:
            df['sample_index'] = np.arange(len(df))
    if 'regime_change' not in df.columns:
        df['regime_change'] = 0
    df = df.sort_values('sample_index').reset_index(drop=True)
    return df, sample_rate
