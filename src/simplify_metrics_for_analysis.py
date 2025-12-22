#!/usr/bin/env python3
"""
Simplify metrics CSV by aggregating results per parameter combination (model).

Each unique parameter combination becomes a "model" with aggregated metrics
across all files in the dataset.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def identify_parameter_columns(df):
    """
    Automatically identify parameter columns from the dataframe.
    """
    known_params = [
        'delta', 'lambda_', 'alpha', 'ma_window', 'min_gap_samples',
        'drift_confidence', 'warning_confidence', 'ks_alpha', 'window_size',
        'stat_size', 'lambda_option', 'regime_threshold', 'regime_landmark'
    ]
    param_cols = [col for col in df.columns if col in known_params]
    return param_cols


def identify_metric_columns(df, param_cols):
    """
    Identify metric columns (excluding parameters and metadata).
    """
    exclude_cols = ['record_id', 'detector', 'duration_seconds'] + param_cols
    metric_cols = [col for col in df.columns if col not in exclude_cols]
    return metric_cols


def aggregate_metrics(df, param_cols, metric_cols, aggregation='mean'):
    """
    Aggregate metrics by parameter combination.

    Parameters
    ----------
    df : pd.DataFrame
        Input metrics dataframe
    param_cols : list
        List of parameter column names
    metric_cols : list
        List of metric column names
    aggregation : str or dict
        Aggregation method ('mean', 'median') or dict with per-metric methods

    Returns
    -------
    pd.DataFrame
        Aggregated dataframe with model IDs
    """
    # Group by parameter combinations
    grouped = df.groupby(param_cols, dropna=False)

    # Define aggregation functions
    if isinstance(aggregation, str):
        if aggregation == 'mean':
            agg_dict = {col: 'mean' for col in metric_cols}
        elif aggregation == 'median':
            agg_dict = {col: 'median' for col in metric_cols}
        else:
            raise ValueError(f"Unknown aggregation method: {aggregation}")
    else:
        agg_dict = aggregation

    # Add count of records per model
    agg_dict['record_id'] = 'count'

    # Aggregate
    result = grouped.agg(agg_dict).reset_index()

    # Rename count column
    result = result.rename(columns={'record_id': 'n_records'})

    # Add model ID
    result.insert(0, 'model_id', [f'model_{i+1}' for i in range(len(result))])

    # Reorder columns: model_id, parameters, n_records, metrics
    cols_order = ['model_id'] + param_cols + ['n_records'] + metric_cols
    result = result[cols_order]

    return result


def add_statistics(df, param_cols, metric_cols):
    """
    Add additional statistics (std, min, max) for key metrics.
    """
    # Group by parameter combinations
    grouped = df.groupby(param_cols, dropna=False)

    # Calculate statistics for selected metrics
    key_metrics = [col for col in ['f3_weighted', 'recall_10s', 'nab_score_standard']
                   if col in metric_cols]

    stats_dict = {}
    for metric in key_metrics:
        stats_dict[f'{metric}_std'] = grouped[metric].std()
        stats_dict[f'{metric}_min'] = grouped[metric].min()
        stats_dict[f'{metric}_max'] = grouped[metric].max()

    stats_df = pd.DataFrame(stats_dict).reset_index()

    return stats_df


def main():
    parser = argparse.ArgumentParser(
        description='Simplify metrics CSV for external analysis (e.g., SHAP in R)'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to input metrics_comprehensive_with_nab.csv'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to output simplified CSV'
    )
    parser.add_argument(
        '--aggregation',
        default='mean',
        choices=['mean', 'median'],
        help='Aggregation method for metrics across files (default: mean)'
    )
    parser.add_argument(
        '--add-stats',
        action='store_true',
        help='Add std/min/max columns for key metrics'
    )
    parser.add_argument(
        '--detector',
        help='Filter by specific detector (optional)'
    )

    args = parser.parse_args()

    # Load data
    print(f"Loading {args.input}...")
    df = pd.read_csv(args.input)
    print(f"  → Loaded {len(df):,} rows")

    # Filter by detector if specified
    if args.detector:
        df = df[df['detector'] == args.detector]
        print(f"  → Filtered to detector '{args.detector}': {len(df):,} rows")

    # Identify columns
    param_cols = identify_parameter_columns(df)
    metric_cols = identify_metric_columns(df, param_cols)

    print(f"\nIdentified columns:")
    print(f"  Parameters ({len(param_cols)}): {', '.join(param_cols)}")
    print(f"  Metrics ({len(metric_cols)}): {', '.join(metric_cols[:5])}...")

    # Aggregate by model
    print(f"\nAggregating by parameter combinations ({args.aggregation})...")
    result = aggregate_metrics(df, param_cols, metric_cols, args.aggregation)
    print(f"  → {len(result):,} unique models")

    # Add statistics if requested
    if args.add_stats:
        print("Adding statistics (std/min/max)...")
        stats_df = add_statistics(df, param_cols, metric_cols)
        # Merge statistics
        result = result.merge(stats_df, on=param_cols, how='left')

    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    print(f"\n✓ Saved: {output_path}")
    print(f"  Dimensions: {result.shape[0]} models × {result.shape[1]} columns")

    # Summary statistics
    print("\nSummary:")
    print(f"  Records per model: {result['n_records'].min()}-{result['n_records'].max()} "
          f"(mean: {result['n_records'].mean():.1f})")

    # Show sample
    print("\nFirst 3 models:")
    print(result.head(3).to_string())


if __name__ == '__main__':
    main()
