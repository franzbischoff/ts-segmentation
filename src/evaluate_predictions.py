#!/usr/bin/env python3
"""
Evaluate predictions from intermediate dataset.
Takes the predictions dataset and calculates comprehensive metrics,
saving them to a separate metrics file before generating final reports.
"""

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Any

import numpy as np
import pandas as pd

from src.evaluation import calculate_comprehensive_metrics


def evaluate_predictions_dataset(predictions_path: str, metrics_output_path: str,
                               tau: float = 10.0, plateau: float = 4.0) -> None:
    """
    Evaluate predictions dataset and calculate comprehensive metrics.

    Args:
        predictions_path: Path to predictions CSV/JSON file
        metrics_output_path: Path to save metrics results
        tau: Acceptance window in seconds (default 10s)
        plateau: Optimal detection window in seconds (default 4s)
    """

    print(f"Loading predictions from {predictions_path}")
    start_time = time.time()

    # Load predictions dataset
    if predictions_path.endswith('.jsonl'):
        # Load from JSON Lines
        predictions = []
        with open(predictions_path, 'r') as f:
            for line in f:
                predictions.append(json.loads(line.strip()))
        predictions_df = pd.DataFrame(predictions)
    else:
        # Load from CSV
        predictions_df = pd.read_csv(predictions_path)
        # Convert string representations back to lists
        for col in ['gt_indices', 'gt_times', 'det_indices', 'det_times']:
            predictions_df[col] = predictions_df[col].apply(eval)

    print(f"Loaded {len(predictions_df)} predictions from {predictions_df['record_id'].nunique()} files")

    # Calculate metrics for each prediction
    metrics_results = []

    for idx, row in predictions_df.iterrows():
        if (idx + 1) % 500 == 0:
            print(f"Processing prediction {idx + 1}/{len(predictions_df)}")

        try:
            # Calculate comprehensive metrics
            metrics = calculate_comprehensive_metrics(
                gt=row['gt_times'],
                det=row['det_times'],
                tau=tau,
                plateau=plateau,
                duration=row['duration_seconds']
            )

            # Combine with prediction metadata
            result = {
                'record_id': row['record_id'],
                'detector': row['detector'],
                'delta': row['delta'],
                'ma_window': row['ma_window'],
                'min_gap_samples': row['min_gap_samples'],
                'duration_samples': row['duration_samples'],
                'duration_seconds': row['duration_seconds'],
                'n_ground_truth': row['n_ground_truth'],
                'n_detections': row['n_detections'],
                **metrics  # Add all comprehensive metrics
            }

            metrics_results.append(result)

        except Exception as e:
            # Add error entry
            result = {
                'record_id': row['record_id'],
                'detector': row['detector'],
                'delta': row['delta'],
                'ma_window': row['ma_window'],
                'min_gap_samples': row['min_gap_samples'],
                'duration_samples': row['duration_samples'],
                'duration_seconds': row['duration_seconds'],
                'n_ground_truth': row['n_ground_truth'],
                'n_detections': row['n_detections'],
                'error': str(e)
            }
            metrics_results.append(result)

    elapsed_time = time.time() - start_time
    print(f"Metrics calculation completed in {elapsed_time:.1f}s")

    # Convert to DataFrame
    metrics_df = pd.DataFrame(metrics_results)

    # Save metrics dataset
    csv_path = metrics_output_path
    metrics_df.to_csv(csv_path, index=False)
    print(f"Metrics saved to: {csv_path}")

    # Save as JSON Lines for inspection
    jsonl_path = csv_path.replace('.csv', '.jsonl')
    with open(jsonl_path, 'w') as f:
        for result in metrics_results:
            f.write(json.dumps(result) + '\\n')
    print(f"JSONL format saved to: {jsonl_path}")

    # Save summary
    error_count = sum(1 for r in metrics_results if 'error' in r)
    summary = {
        'total_evaluations': len(metrics_results),
        'error_count': error_count,
        'successful_evaluations': len(metrics_results) - error_count,
        'unique_files': metrics_df['record_id'].nunique(),
        'unique_param_combinations': len(metrics_df[['delta', 'ma_window', 'min_gap_samples']].drop_duplicates()),
        'evaluation_time_seconds': elapsed_time,
        'tau_acceptance_window': tau,
        'plateau_optimal_window': plateau,
        'avg_evaluation_time': elapsed_time / len(metrics_results)
    }

    summary_path = csv_path.replace('.csv', '_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to: {summary_path}")

    return metrics_df


def generate_best_parameters_report(metrics_path: str, report_output_path: str) -> None:
    """
    Generate final report with best parameters based on different metrics.

    Args:
        metrics_path: Path to metrics CSV file
        report_output_path: Path to save final report
    """

    print(f"\\nGenerating report from metrics: {metrics_path}")

    # Load metrics
    metrics_df = pd.read_csv(metrics_path)

    # Filter valid results (no errors)
    if 'error' in metrics_df.columns:
        valid_results = metrics_df[pd.isna(metrics_df['error'])].copy()
    else:
        valid_results = metrics_df.copy()

    print(f"Using {len(valid_results)} valid results out of {len(metrics_df)} total")

    if len(valid_results) == 0:
        print("No valid results to analyze!")
        return

    # Parameter columns for grouping
    param_cols = ['delta', 'ma_window', 'min_gap_samples']

    # Aggregate metrics by parameter combination
    agg_metrics = {
        'f1_classic': ['mean', 'std', 'count'],
        'f1_weighted': ['mean', 'std', 'count'],
        'f3_classic': ['mean', 'std', 'count'],
        'f3_weighted': ['mean', 'std', 'count'],
        'recall_4s': ['mean', 'std'],
        'recall_10s': ['mean', 'std'],
        'precision_4s': ['mean', 'std'],
        'precision_10s': ['mean', 'std'],
        'edd_median_s': 'mean',
        'fp_per_min': 'mean',
        'n_ground_truth': 'sum',
        'n_detections': 'sum'
    }

    # Only include metrics that exist in the data
    available_metrics = {k: v for k, v in agg_metrics.items() if k in valid_results.columns}

    global_perf = valid_results.groupby(param_cols).agg(available_metrics).round(4)

    # Flatten column names
    global_perf.columns = ['_'.join(col).strip() for col in global_perf.columns]
    global_perf = global_perf.reset_index()

    # Find best parameters for different metrics
    best_results = {}

    # Helper function to convert numpy types to Python types
    def convert_numpy_types(obj):
        if hasattr(obj, 'item'):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(v) for v in obj]
        else:
            return obj

    # F3 weighted (primary)
    if 'f3_weighted_mean' in global_perf.columns:
        best_f3_weighted = global_perf.loc[global_perf['f3_weighted_mean'].idxmax()]
        best_results['f3_weighted'] = convert_numpy_types(best_f3_weighted.to_dict())

    # F1 weighted
    if 'f1_weighted_mean' in global_perf.columns:
        best_f1_weighted = global_perf.loc[global_perf['f1_weighted_mean'].idxmax()]
        best_results['f1_weighted'] = convert_numpy_types(best_f1_weighted.to_dict())

    # F1 classic
    if 'f1_classic_mean' in global_perf.columns:
        best_f1_classic = global_perf.loc[global_perf['f1_classic_mean'].idxmax()]
        best_results['f1_classic'] = convert_numpy_types(best_f1_classic.to_dict())

    # F3 classic
    if 'f3_classic_mean' in global_perf.columns:
        best_f3_classic = global_perf.loc[global_perf['f3_classic_mean'].idxmax()]
        best_results['f3_classic'] = convert_numpy_types(best_f3_classic.to_dict())

    # Generate report
    report = {
        'evaluation_summary': {
            'total_files': int(valid_results['record_id'].nunique()),
            'total_param_combinations': len(global_perf),
            'total_evaluations': len(valid_results),
            'total_ground_truth_events': int(valid_results['n_ground_truth'].sum()),
            'total_detections': int(valid_results['n_detections'].sum())
        },
        'best_parameters': best_results,
        'top_10_f3_weighted': convert_numpy_types(global_perf.nlargest(10, 'f3_weighted_mean')[param_cols + ['f3_weighted_mean']].to_dict('records')) if 'f3_weighted_mean' in global_perf.columns else [],
        'parameter_grid_coverage': {
            'delta_values': convert_numpy_types(sorted(global_perf['delta'].unique().tolist())),
            'ma_window_values': convert_numpy_types(sorted(global_perf['ma_window'].unique().tolist())),
            'min_gap_samples_values': convert_numpy_types(sorted(global_perf['min_gap_samples'].unique().tolist()))
        }
    }

    # Save report
    with open(report_output_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Final report saved to: {report_output_path}")

    # Print summary to console
    print("\\n" + "="*80)
    print("FINAL RESULTS SUMMARY")
    print("="*80)

    if 'f3_weighted' in best_results:
        best = best_results['f3_weighted']
        print(f"\\n=== BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric) ===")
        print(f"  delta: {best['delta']}")
        print(f"  ma_window: {int(best['ma_window'])}")
        print(f"  min_gap_samples: {int(best['min_gap_samples'])}")
        if 'f3_weighted_mean' in best:
            print(f"  F3 weighted: {best['f3_weighted_mean']:.4f} ± {best.get('f3_weighted_std', 0):.4f}")
        if 'f3_classic_mean' in best:
            print(f"  F3 classic:  {best['f3_classic_mean']:.4f} ± {best.get('f3_classic_std', 0):.4f}")
        if 'f1_weighted_mean' in best:
            print(f"  F1 weighted: {best['f1_weighted_mean']:.4f} ± {best.get('f1_weighted_std', 0):.4f}")
        if 'f1_classic_mean' in best:
            print(f"  F1 classic:  {best['f1_classic_mean']:.4f} ± {best.get('f1_classic_std', 0):.4f}")
        if 'recall_4s_mean' in best:
            print(f"  Recall@4s: {best['recall_4s_mean']:.4f}")
        if 'recall_10s_mean' in best:
            print(f"  Recall@10s: {best['recall_10s_mean']:.4f}")
        if 'precision_4s_mean' in best:
            print(f"  Precision@4s: {best['precision_4s_mean']:.4f}")
        if 'precision_10s_mean' in best:
            print(f"  Precision@10s: {best['precision_10s_mean']:.4f}")
        if 'edd_median_s_mean' in best:
            print(f"  EDD median: {best['edd_median_s_mean']:.2f}s")
        if 'fp_per_min_mean' in best:
            print(f"  FP/min: {best['fp_per_min_mean']:.2f}")

    print("\\n=== COMPARISON WITH OTHER METRICS ===")
    for metric_name, result in best_results.items():
        if metric_name != 'f3_weighted':
            print(f"{metric_name.replace('_', ' ').title()} best: delta={result['delta']}, ma_window={int(result['ma_window'])}, min_gap={int(result['min_gap_samples'])}")


def main():
    parser = argparse.ArgumentParser(description='Evaluate predictions and generate comprehensive metrics')
    parser.add_argument('--predictions', required=True, help='Path to predictions CSV/JSONL file')
    parser.add_argument('--metrics-output', required=True, help='Output path for metrics CSV')
    parser.add_argument('--report-output', required=True, help='Output path for final report JSON')
    parser.add_argument('--tau', type=float, default=10.0, help='Acceptance window in seconds')
    parser.add_argument('--plateau', type=float, default=4.0, help='Optimal detection window in seconds')
    parser.add_argument('--skip-evaluation', action='store_true', help='Skip metrics calculation (use existing metrics file)')

    args = parser.parse_args()

    if not args.skip_evaluation:
        # Step 1: Calculate metrics
        metrics_df = evaluate_predictions_dataset(
            predictions_path=args.predictions,
            metrics_output_path=args.metrics_output,
            tau=args.tau,
            plateau=args.plateau
        )

    # Step 2: Generate report
    generate_best_parameters_report(
        metrics_path=args.metrics_output,
        report_output_path=args.report_output
    )


if __name__ == '__main__':
    main()
