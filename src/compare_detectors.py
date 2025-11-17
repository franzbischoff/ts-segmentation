#!/usr/bin/env python3
"""
Compare results from multiple change point detectors

Generates comparative analysis including:
- Side-by-side best configurations
- Metric rankings
- Statistical comparisons
- Ensemble recommendations
"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict


def load_detector_report(detector_name: str, results_dir: Path) -> Dict:
    """Load final report JSON for a detector."""
    report_path = results_dir / detector_name / 'final_report_with_nab.json'

    if not report_path.exists():
        print(f"⚠️  Report not found for {detector_name}: {report_path}")
        return None

    with open(report_path, 'r') as f:
        return json.load(f)


def load_detector_metrics(detector_name: str, results_dir: Path) -> pd.DataFrame:
    """Load comprehensive metrics CSV for a detector."""
    metrics_path = results_dir / detector_name / 'metrics_comprehensive_with_nab.csv'

    if not metrics_path.exists():
        print(f"⚠️  Metrics not found for {detector_name}: {metrics_path}")
        return None

    df = pd.read_csv(metrics_path)
    df['detector'] = detector_name
    return df


def generate_best_configs_table(reports: Dict[str, Dict]) -> pd.DataFrame:
    """Create table comparing best configurations across detectors."""

    metrics = [
        'f3_weighted', 'f3_classic', 'f1_weighted', 'f1_classic',
        'nab_standard', 'nab_low_fp', 'nab_low_fn'
    ]

    rows = []
    for metric in metrics:
        row = {'metric': metric}

        for detector_name, report in reports.items():
            if report and 'best_parameters' in report:
                best = report['best_parameters'].get(metric, {})

                # Extract key info
                if best:
                    delta = best.get('delta', 'N/A')
                    ma_window = best.get('ma_window', 'N/A')
                    min_gap = best.get('min_gap_samples', 'N/A')

                    # Get score (try different naming patterns)
                    score_key = f"{metric}_mean"
                    if metric.startswith('nab_'):
                        score_key = f"nab_score_{metric[4:]}_mean"

                    score = best.get(score_key, best.get(metric, 'N/A'))

                    if isinstance(score, (int, float)):
                        score_str = f"{score:.4f}"
                    else:
                        score_str = str(score)

                    row[detector_name] = f"{score_str} (δ={delta}, ma={ma_window}, gap={min_gap})"
                else:
                    row[detector_name] = 'N/A'

        rows.append(row)

    return pd.DataFrame(rows)


def generate_metric_rankings(reports: Dict[str, Dict]) -> pd.DataFrame:
    """Rank detectors by each metric."""

    metrics_config = [
        ('f3_weighted_mean', 'F3-Weighted', 'maximize'),
        ('nab_score_standard_mean', 'NAB Standard', 'maximize'),
        ('recall_10s_mean', 'Recall@10s', 'maximize'),
        ('precision_10s_mean', 'Precision@10s', 'maximize'),
        ('fp_per_min_mean', 'FP/min', 'minimize'),
        ('edd_median_s_mean', 'EDD Median', 'minimize'),
    ]

    rows = []
    for metric_key, metric_name, direction in metrics_config:
        row = {'metric': metric_name}

        # Collect scores for this metric across detectors
        scores = {}
        for detector_name, report in reports.items():
            if report and 'best_parameters' in report:
                # Try to get from f3_weighted best config (primary)
                best = report['best_parameters'].get('f3_weighted', {})

                # Handle NAB naming pattern
                if metric_key.startswith('nab_'):
                    # Extract from appropriate nab_* best config
                    nab_type = metric_key.replace('nab_score_', '').replace('_mean', '')
                    best = report['best_parameters'].get(f'nab_{nab_type}', best)

                score = best.get(metric_key)
                if score is not None and score != 'N/A':
                    scores[detector_name] = float(score)

        # Rank
        if scores:
            if direction == 'maximize':
                sorted_detectors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            else:
                sorted_detectors = sorted(scores.items(), key=lambda x: x[1])

            for rank, (detector, score) in enumerate(sorted_detectors, 1):
                row[f'rank_{rank}'] = f"{detector} ({score:.4f})"

        rows.append(row)

    return pd.DataFrame(rows)


def generate_statistical_comparison(metrics_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Statistical comparison (mean, std, median) across detectors."""

    if not metrics_dfs:
        return pd.DataFrame()

    metrics_to_compare = [
        'f3_weighted', 'f1_weighted', 'recall_10s', 'precision_10s',
        'fp_per_min', 'edd_median_s', 'nab_score_standard'
    ]

    rows = []
    for metric in metrics_to_compare:
        row = {'metric': metric}

        for detector_name, df in metrics_dfs.items():
            if metric in df.columns:
                values = df[metric].dropna()

                mean_val = values.mean()
                std_val = values.std()
                median_val = values.median()

                row[f'{detector_name}_mean'] = f"{mean_val:.4f}"
                row[f'{detector_name}_std'] = f"{std_val:.4f}"
                row[f'{detector_name}_median'] = f"{median_val:.4f}"

        rows.append(row)

    return pd.DataFrame(rows)


def generate_markdown_report(
    detectors: List[str],
    best_configs: pd.DataFrame,
    rankings: pd.DataFrame,
    stats: pd.DataFrame,
    output_path: Path
):
    """Generate comprehensive markdown comparison report."""

    with open(output_path, 'w') as f:
        f.write("# Comparative Analysis: Change Point Detectors\n\n")
        f.write(f"**Date**: 2025-11-13\n")
        f.write(f"**Detectors**: {', '.join(detectors)}\n\n")

        f.write("---\n\n")

        # Best configurations
        f.write("## 1. Best Configurations by Metric\n\n")
        f.write("Comparison of optimal parameter settings for each metric:\n\n")
        f.write(best_configs.to_markdown(index=False))
        f.write("\n\n")

        # Rankings
        f.write("## 2. Detector Rankings\n\n")
        f.write("Detectors ranked by performance on key metrics:\n\n")
        f.write(rankings.to_markdown(index=False))
        f.write("\n\n")

        # Statistical comparison
        if not stats.empty:
            f.write("## 3. Statistical Comparison\n\n")
            f.write("Mean ± Std (Median) across all parameter combinations:\n\n")
            f.write(stats.to_markdown(index=False))
            f.write("\n\n")

        # Recommendations
        f.write("## 4. Recommendations\n\n")
        f.write("### For Maximum Recall (Don't miss events)\n")
        f.write("- **Primary**: Best F3-weighted configuration\n")
        f.write("- **Alternative**: Best NAB Low FN configuration\n\n")

        f.write("### For Minimum False Positives (Reduce alarms)\n")
        f.write("- **Primary**: Best NAB Low FP configuration\n")
        f.write("- **Consider**: Higher min_gap_samples values\n\n")

        f.write("### For Balanced Performance\n")
        f.write("- **Primary**: Pareto-optimal solutions\n")
        f.write("- **Metric**: NAB Standard or F3-weighted\n\n")

        f.write("### For Ensemble Methods\n")
        f.write("Combine detectors using:\n")
        f.write("- **Voting**: Majority vote (2/3 or 3/5)\n")
        f.write("- **Weighted**: Weight by F3-weighted score\n")
        f.write("- **Cascade**: Fast detector → Precise detector\n\n")

        f.write("---\n\n")
        f.write("## Appendix: Interpretation Guide\n\n")
        f.write("**Metrics**:\n")
        f.write("- F3-weighted: Emphasizes recall with temporal weighting (primary metric)\n")
        f.write("- NAB Standard: Balanced anomaly detection score\n")
        f.write("- NAB Low FP: Penalizes false positives 2×\n")
        f.write("- NAB Low FN: Penalizes false negatives 2×\n")
        f.write("- Recall@10s: % events detected within 10 seconds\n")
        f.write("- FP/min: False positive rate\n")
        f.write("- EDD: Expected detection delay (median)\n\n")

        f.write("**Parameters**:\n")
        f.write("- δ (delta): Detector sensitivity threshold\n")
        f.write("- ma (ma_window): Moving average window size\n")
        f.write("- gap (min_gap_samples): Minimum spacing between detections\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Compare results from multiple change point detectors'
    )
    parser.add_argument(
        '--detectors',
        nargs='+',
        required=True,
        help='List of detector names to compare (e.g., adwin page_hinkley kswin hddm_a hddm_w)'
    )
    parser.add_argument(
        '--results-dir',
        default='results',
        help='Base directory containing detector results'
    )
    parser.add_argument(
        '--output',
        default='results/comparisons/comparative_report.md',
        help='Output path for markdown report'
    )
    parser.add_argument(
        '--csv-output',
        default='results/comparisons/detector_rankings.csv',
        help='Output path for rankings CSV'
    )

    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_path = Path(args.output)
    csv_output_path = Path(args.csv_output)

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Comparing detectors: {', '.join(args.detectors)}")
    print(f"Results directory: {results_dir}")
    print()

    # Load reports
    print("Loading detector reports...")
    reports = {}
    for detector in args.detectors:
        report = load_detector_report(detector, results_dir)
        if report:
            reports[detector] = report
            print(f"  ✓ {detector}")
        else:
            print(f"  ✗ {detector} (not found)")

    if not reports:
        print("\n❌ No detector reports found. Exiting.")
        return

    print()

    # Load metrics
    print("Loading detector metrics...")
    metrics_dfs = {}
    for detector in args.detectors:
        df = load_detector_metrics(detector, results_dir)
        if df is not None:
            metrics_dfs[detector] = df
            print(f"  ✓ {detector} ({len(df)} evaluations)")
        else:
            print(f"  ✗ {detector} (not found)")

    print()

    # Generate comparisons
    print("Generating comparisons...")
    best_configs = generate_best_configs_table(reports)
    rankings = generate_metric_rankings(reports)
    stats = generate_statistical_comparison(metrics_dfs)

    # Save rankings CSV
    rankings.to_csv(csv_output_path, index=False)
    print(f"  ✓ Rankings saved: {csv_output_path}")

    # Generate markdown report
    generate_markdown_report(
        args.detectors,
        best_configs,
        rankings,
        stats,
        output_path
    )
    print(f"  ✓ Report saved: {output_path}")

    print()
    print("✅ Comparison complete!")
    print(f"\nView report: {output_path}")


if __name__ == '__main__':
    main()
