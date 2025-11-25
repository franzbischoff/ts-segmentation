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
from datetime import datetime

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
        # Convert string representations back to lists (only if columns exist)
        for col in ['gt_indices', 'gt_times', 'det_indices', 'det_times']:
            if col in predictions_df.columns:
                predictions_df[col] = predictions_df[col].apply(eval)

    print(f"Loaded {len(predictions_df)} predictions from {predictions_df['record_id'].nunique()} files")

    # Identify parameter columns (exclude data columns)
    exclude_cols = ['record_id', 'detector', 'duration_samples', 'duration_seconds',
                   'gt_indices', 'gt_times', 'det_indices', 'det_times',
                   'n_detections', 'n_ground_truth', 'processing_time', 'error']
    param_cols = [col for col in predictions_df.columns if col not in exclude_cols]
    print(f"Detected parameter columns: {param_cols}")

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
            }

            # Add all parameter columns dynamically
            for col in param_cols:
                if col in row:
                    result[col] = row[col]

            # Add metadata
            if 'duration_samples' in row:
                result['duration_samples'] = row['duration_samples']
            result['duration_seconds'] = row['duration_seconds']
            result['n_ground_truth'] = row['n_ground_truth']
            result['n_detections'] = row['n_detections']

            # Add all comprehensive metrics
            result.update(metrics)

            metrics_results.append(result)

        except Exception as e:
            # Add error entry
            result = {
                'record_id': row['record_id'],
                'detector': row['detector'],
            }

            # Add all parameter columns dynamically
            for col in param_cols:
                if col in row:
                    result[col] = row[col]

            if 'duration_samples' in row:
                result['duration_samples'] = row['duration_samples']
            result['duration_seconds'] = row['duration_seconds']
            result['n_ground_truth'] = row['n_ground_truth']
            result['n_detections'] = row['n_detections']
            result['error'] = str(e)
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
            f.write(json.dumps(result) + '\n')
    print(f"JSONL format saved to: {jsonl_path}")

    # Identify parameter columns dynamically for summary
    exclude_cols_summary = ['record_id', 'detector', 'duration_samples', 'duration_seconds',
                           'n_ground_truth', 'n_detections', 'error',
                           'f1_classic', 'f1_weighted', 'f3_classic', 'f3_weighted',
                           'recall_4s', 'recall_10s', 'precision_4s', 'precision_10s',
                           'edd_median_s', 'edd_p95_s', 'fp_per_min',
                           'nab_score_standard', 'nab_score_low_fp', 'nab_score_low_fn',
                           'tp', 'fp', 'fn', 'tp_weight_sum']
    param_cols_summary = [col for col in metrics_df.columns if col not in exclude_cols_summary]

    # Save summary
    error_count = sum(1 for r in metrics_results if 'error' in r)
    summary = {
        'total_evaluations': len(metrics_results),
        'error_count': error_count,
        'successful_evaluations': len(metrics_results) - error_count,
        'unique_files': metrics_df['record_id'].nunique(),
        'unique_param_combinations': len(metrics_df[param_cols_summary].drop_duplicates()) if param_cols_summary else 0,
        'parameter_columns': param_cols_summary,
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

    print(f"\nGenerating report from metrics: {metrics_path}")

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

    # Identify parameter columns dynamically
    exclude_cols_params = ['record_id', 'detector', 'duration_samples', 'duration_seconds',
                          'n_ground_truth', 'n_detections', 'error',
                          'f1_classic', 'f1_weighted', 'f3_classic', 'f3_weighted',
                          'recall_4s', 'recall_10s', 'precision_4s', 'precision_10s',
                          'edd_median_s', 'edd_p95_s', 'fp_per_min',
                          'nab_score_standard', 'nab_score_low_fp', 'nab_score_low_fn',
                          'tp', 'fp', 'fn', 'tp_weight_sum']
    param_cols = [col for col in valid_results.columns if col not in exclude_cols_params]
    print(f"Parameter columns for grouping: {param_cols}")

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
        'nab_score_standard': ['mean', 'std'],
        'nab_score_low_fp': ['mean', 'std'],
        'nab_score_low_fn': ['mean', 'std'],
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

    # NAB Standard
    if 'nab_score_standard_mean' in global_perf.columns:
        best_nab_standard = global_perf.loc[global_perf['nab_score_standard_mean'].idxmax()]
        best_results['nab_standard'] = convert_numpy_types(best_nab_standard.to_dict())

    # NAB Low FP
    if 'nab_score_low_fp_mean' in global_perf.columns:
        best_nab_low_fp = global_perf.loc[global_perf['nab_score_low_fp_mean'].idxmax()]
        best_results['nab_low_fp'] = convert_numpy_types(best_nab_low_fp.to_dict())

    # NAB Low FN
    if 'nab_score_low_fn_mean' in global_perf.columns:
        best_nab_low_fn = global_perf.loc[global_perf['nab_score_low_fn_mean'].idxmax()]
        best_results['nab_low_fn'] = convert_numpy_types(best_nab_low_fn.to_dict())

    # Generate report
    # Derive dataset name from path if possible: results/<dataset>/<detector>/metrics.csv
    try:
        dataset_name = Path(metrics_path).parent.parent.name
    except Exception:
        dataset_name = None

    report = {
        'evaluation_summary': {
            'total_files': int(valid_results['record_id'].nunique()),
            'dataset': dataset_name,
            'total_param_combinations': len(global_perf),
            'total_evaluations': len(valid_results),
            'total_ground_truth_events': int(valid_results['n_ground_truth'].sum()),
            'total_detections': int(valid_results['n_detections'].sum())
        },
        'best_parameters': best_results,
        'top_10_f3_weighted': convert_numpy_types(global_perf.nlargest(10, 'f3_weighted_mean')[param_cols + ['f3_weighted_mean']].to_dict('records')) if 'f3_weighted_mean' in global_perf.columns else [],
        'top_10_nab_standard': convert_numpy_types(global_perf.nlargest(10, 'nab_score_standard_mean')[param_cols + ['nab_score_standard_mean']].to_dict('records')) if 'nab_score_standard_mean' in global_perf.columns else [],
        'parameter_grid_coverage': {}
    }

    # Add parameter value ranges dynamically
    for param_col in param_cols:
        if param_col in global_perf.columns:
            report['parameter_grid_coverage'][f'{param_col}_values'] = convert_numpy_types(sorted(global_perf[param_col].unique().tolist()))

    # Save report
    with open(report_output_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Final report saved to: {report_output_path}")

    # Also save a human-friendly markdown copy of the report with timestamp
    try:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        # Place markdown next to JSON report, using a timestamp to avoid overwrites
        report_p = Path(report_output_path)
        md_name = report_p.stem + f"_{ts}.md"
        md_path = report_p.with_name(md_name)

        lines = []
        lines.append("# Comparative Report — Temporary Snapshot")
        lines.append(f"Generated: {datetime.utcnow().isoformat()} UTC")
        if dataset_name:
            lines.append(f"**Dataset**: {dataset_name}")
        lines.append("---")

        # Evaluation summary
        lines.append("## Evaluation Summary")
        for k, v in report.get('evaluation_summary', {}).items():
            lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")

        # Best parameters (match CLI output)
        lines.append("## Best Parameter Configurations")
        # Output the main 'best' (F3 weighted primary) as the CLI does
        bp = report.get('best_parameters', {})
        primary = bp.get('f3_weighted') or next(iter(bp.values()), None)
        if primary:
            lines.append("### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)")
            # Print parameters first
            for p in param_cols:
                if p in primary:
                    lines.append(f"- {p}: {primary[p]}")

            # Collect numeric metrics and format mean±std when available
            metric_pairs = []
            for k, v in primary.items():
                if k in param_cols:
                    continue
                # look for mean/std pairs
                if k.endswith('_mean'):
                    base = k[:-5]
                    mean = v
                    std = primary.get(f"{base}_std")
                    if std is not None:
                        metric_pairs.append((base, f"{mean:.4f} ± {std:.4f}"))
                    else:
                        metric_pairs.append((base, f"{mean:.4f}"))
                elif not k.endswith('_std') and not k.endswith('_count'):
                    # single metric (not mean/std pair)
                    try:
                        fv = float(v)
                        metric_pairs.append((k, f"{fv:.4f}"))
                    except Exception:
                        metric_pairs.append((k, str(v)))

            # Re-order some human-friendly metrics for presentation
            order = ['f3_weighted', 'f3_classic', 'f1_weighted', 'f1_classic',
                     'recall_4s', 'recall_10s', 'precision_4s', 'precision_10s',
                     'edd_median_s', 'fp_per_min']

            for name in order:
                for m, val in metric_pairs:
                    if m == name:
                        # pretty label
                        label = name.replace('_', ' ').upper() if 'nab' not in name else name
                        lines.append(f"- {label}: {val}")
            # any remaining metrics
            for m, val in metric_pairs:
                if m not in order:
                    lines.append(f"- {m}: {val}")

            # NAB scores grouped
            nab_keys = [k for k in primary.keys() if k.startswith('nab_score_') and k.endswith('_mean')]
            if nab_keys:
                lines.append('- NAB Scores:')
                for nk in nab_keys:
                    base = nk.replace('_mean', '')
                    mean = primary.get(nk)
                    std = primary.get(f"{base}_std", 0)
                    lines.append(f"  - {base}: {mean:.4f} ± {std:.4f}")

            # separate sections with a single blank line
            lines.append("")

        # Comparison with other metrics (like CLI)
        if bp:
            lines.append('## Comparison With Other Metrics')
            for metric_name, result in bp.items():
                if metric_name == 'f3_weighted':
                    continue
                # parameter string
                param_strs = []
                for p in param_cols:
                    if p in result:
                        val = result[p]
                        param_strs.append(f"{p}={val}")
                params_line = ", ".join(param_strs)

                # determine score
                score_key = f"{metric_name}_mean"
                score = None
                if score_key in result:
                    score = result[score_key]
                elif metric_name in result:
                    score = result[metric_name]

                if score is not None:
                    lines.append(f"- {metric_name.replace('_', ' ').title()} best: {params_line} (score={score:.4f})")
                else:
                    lines.append(f"- {metric_name.replace('_', ' ').title()} best: {params_line}")
            # separate sections with a single blank line
            lines.append("")

        # Top-10 lists (if present)
        if report.get('top_10_f3_weighted'):
            lines.append("## Top 10 (F3-weighted)")
            # convert to simple table
            top10 = report['top_10_f3_weighted']
            # Table header
            header = [c for c in param_cols] + ['f3_weighted_mean']
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "---|" * len(header) + "")
            for row in top10:
                row_values = [str(row.get(c, '')) for c in header]
                lines.append("| " + " | ".join(row_values) + " |")
            # keep no extra blank line after table

        # Top-10 NAB (if present)
        if report.get('top_10_nab_standard'):
            lines.append("## Top 10 (NAB Standard)")
            topn = report['top_10_nab_standard']
            header = [c for c in param_cols] + ['nab_score_standard_mean']
            lines.append("| " + " | ".join(header) + " |")
            lines.append("|" + "---|" * len(header) + "")
            for row in topn:
                row_values = [str(row.get(c, '')) for c in header]
                lines.append("| " + " | ".join(row_values) + " |")
            # keep no extra blank line after table

        # Footer: temp note
        lines.append("---")
        lines.append("_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._")

        md_text = "\n".join(lines)
        with open(md_path, 'w') as f:
            f.write(md_text)

        print(f"Markdown snapshot saved to: {md_path}")
    except Exception as e:
        print(f"Warning: failed to write markdown snapshot: {e}")

    # Print summary to console
    print("\n" + "="*80)
    print("FINAL RESULTS SUMMARY")
    print("="*80)

    if 'f3_weighted' in best_results:
        best = best_results['f3_weighted']
        print(f"\n=== BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric) ===")
        # Print all parameter values dynamically
        for param_col in param_cols:
            if param_col in best:
                val = best[param_col]
                # Format integers vs floats nicely
                if isinstance(val, (int, np.integer)) or (isinstance(val, float) and val.is_integer()):
                    print(f"  {param_col}: {int(val)}")
                else:
                    print(f"  {param_col}: {val}")

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

        # NAB scores
        if 'nab_score_standard_mean' in best:
            print(f"\n  NAB Scores:")
            print(f"    Standard:  {best['nab_score_standard_mean']:.4f} ± {best.get('nab_score_standard_std', 0):.4f}")
        if 'nab_score_low_fp_mean' in best:
            print(f"    Low FP:    {best['nab_score_low_fp_mean']:.4f} ± {best.get('nab_score_low_fp_std', 0):.4f}")
        if 'nab_score_low_fn_mean' in best:
            print(f"    Low FN:    {best['nab_score_low_fn_mean']:.4f} ± {best.get('nab_score_low_fn_std', 0):.4f}")

    print("\n=== COMPARISON WITH OTHER METRICS ===")
    for metric_name, result in best_results.items():
        if metric_name != 'f3_weighted':
            # Format parameters dynamically
            param_strs = []
            for param_col in param_cols:
                if param_col in result:
                    val = result[param_col]
                    if isinstance(val, (int, np.integer)) or (isinstance(val, float) and val.is_integer()):
                        param_strs.append(f"{param_col}={int(val)}")
                    else:
                        param_strs.append(f"{param_col}={val}")
            params = ", ".join(param_strs)

            # Add score if available - try multiple naming patterns
            score = ""
            # Try with _mean suffix
            score_key = f"{metric_name}_mean"
            if score_key in result:
                score = f" (score={result[score_key]:.4f})"
            else:
                # For NAB metrics, try with nab_score_ prefix
                if metric_name.startswith('nab_'):
                    nab_score_key = f"nab_score_{metric_name[4:]}_mean"  # Remove 'nab_' and add 'nab_score_' prefix
                    if nab_score_key in result:
                        score = f" (score={result[nab_score_key]:.4f})"
                # Try without suffix
                elif metric_name in result:
                    score = f" (score={result[metric_name]:.4f})"

            # Format metric name
            display_name = metric_name.replace('_', ' ').title()
            if 'Nab' in display_name:
                display_name = display_name.replace('Nab', 'NAB').replace(' Fp', ' FP').replace(' Fn', ' FN')

            print(f"{display_name} best: {params}{score}")
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
