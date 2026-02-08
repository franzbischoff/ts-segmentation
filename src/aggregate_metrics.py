#!/usr/bin/env python3
"""
Aggregate Grid Search Metrics by Parameter Combinations

Takes a detailed metrics CSV (one row per file/parameter combination) and
aggregates it by unique parameter sets, computing mean and std for each metric.

This produces a summary CSV suitable for comparative analysis without generating
visualizations.
"""

import argparse
import pandas as pd
from pathlib import Path


def aggregate_metrics(metrics_path):
    """Load metrics CSV and aggregate by parameters."""
    df = pd.read_csv(metrics_path)

    # Auto-detect parameter columns (detector-specific)
    all_cols = df.columns.tolist()

    # Known metric/metadata columns to exclude
    exclude_patterns = [
        'file_id', 'f1_', 'f3_', 'precision', 'recall', 'edd_', 'fp_per_min',
        'nab_score', 'tp', 'fp', 'fn', 'n_detections', 'n_gt_events'
    ]

    param_cols = []
    for col in all_cols:
        if any(pattern in col for pattern in exclude_patterns):
            continue
        # Include if it looks like a parameter (not a metric)
        if col in ['delta', 'lambda_', 'alpha', 'ma_window', 'min_gap_samples',
                   'drift_confidence', 'warning_confidence', 'two_side_option',
                   'lambda_option', 'ks_alpha', 'window_size', 'stat_size',
                   'min_instances', 'warning_level', 'out_control_level',
                   'use_derivative', 'regime_threshold', 'regime_landmark']:
            param_cols.append(col)

    if not param_cols:
        raise ValueError(f"No parameter columns detected in {metrics_path}")

    print(f"Detected parameters: {param_cols}")

    # Define metrics to aggregate
    metric_cols = [
        'f1_classic', 'f1_weighted', 'f3_classic', 'f3_weighted',
        'recall_4s', 'recall_10s', 'precision_4s', 'precision_10s',
        'edd_median_s', 'edd_p95_s', 'fp_per_min'
    ]

    # Add NAB metrics if they exist
    for nab_col in ['nab_score_standard', 'nab_score_low_fp', 'nab_score_low_fn']:
        if nab_col in df.columns:
            metric_cols.append(nab_col)

    # Group and calculate mean and std for each metric
    agg_dict = {}
    for col in metric_cols:
        if col in df.columns:
            agg_dict[col] = ['mean', 'std']

    grouped = df.groupby(param_cols).agg(agg_dict).reset_index()

    # Flatten column names
    grouped.columns = [
        '_'.join(col).strip('_') if col[1] else col[0]
        for col in grouped.columns.values
    ]

    return grouped


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate grid search metrics by parameter combinations'
    )
    parser.add_argument(
        '--metrics',
        '--input',
        dest='metrics',
        required=True,
        help='Path to input metrics CSV file'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to save aggregated metrics CSV'
    )

    args = parser.parse_args()

    # Validate input file exists
    metrics_path = Path(args.metrics)
    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

    print(f"Loading metrics from: {metrics_path}")
    df = aggregate_metrics(metrics_path)
    print(f"Aggregated to {len(df)} unique parameter combinations")

    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save aggregated metrics
    df.to_csv(output_path, index=False)
    print(f"✓ Saved aggregated metrics: {output_path}")

    # Show summary statistics
    print("\nSummary:")
    print(f"  Input rows: {pd.read_csv(metrics_path).shape[0]}")
    print(f"  Output rows (unique parameter sets): {len(df)}")
    print(f"  Columns: {len(df.columns)}")


if __name__ == '__main__':
    main()
