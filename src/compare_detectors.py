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
    report_path = results_dir / detector_name / "final_report_with_nab.json"

    if not report_path.exists():
        print(f"⚠️  Report not found for {detector_name}: {report_path}")
        return None

    with open(report_path, "r") as f:
        return json.load(f)


def load_detector_metrics(detector_name: str, results_dir: Path) -> pd.DataFrame:
    """Load comprehensive metrics CSV for a detector."""
    metrics_path = results_dir / detector_name / "metrics_comprehensive_with_nab.csv"

    if not metrics_path.exists():
        print(f"⚠️  Metrics not found for {detector_name}: {metrics_path}")
        return None

    df = pd.read_csv(metrics_path)
    df["detector"] = detector_name
    return df


def generate_best_configs_table(metrics_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Generate table of best configurations for each metric."""
    metrics_config = [
        ("f3_weighted", "F3-Weighted", "maximize"),
        ("f1_weighted", "F1-Weighted", "maximize"),
        ("nab_score_standard", "NAB Standard", "maximize"),
        ("nab_score_low_fp", "NAB Low FP", "maximize"),
        ("nab_score_low_fn", "NAB Low FN", "maximize"),
        ("recall_10s", "Recall@10s", "maximize"),
        ("precision_10s", "Precision@10s", "maximize"),
        ("fp_per_min", "FP/min", "minimize"),
        ("edd_median_s", "EDD Median", "minimize"),
    ]

    # Parameter name mapping for brevity
    param_map = {
        "delta": "δ",
        "ma_window": "ma",
        "min_gap_samples": "gap",
        "threshold": "th",
        "alpha": "α",
        "lambda": "λ",
        "forgetting_factor": "ff",
    }

    known_metrics = {
        "f1_classic",
        "f1_weighted",
        "f3_classic",
        "f3_weighted",
        "recall_4s",
        "recall_10s",
        "precision_4s",
        "precision_10s",
        "edd_median_s",
        "edd_p95_s",
        "fp_per_min",
        "nab_score_standard",
        "nab_score_low_fp",
        "nab_score_low_fn",
        "record_id",
        "detector",
        "duration_samples",
        "duration_seconds",
        "n_ground_truth",
        "n_detections",
        "tp",
        "fp",
        "fn",
        "tp_weight_sum",
    }

    rows = []
    for metric_key, metric_name, direction in metrics_config:
        row = {"metric": metric_key}

        for detector_name, df in metrics_dfs.items():
            if metric_key not in df.columns:
                row[detector_name] = "N/A"
                continue

            # Aggregate first to get correct best config
            agg_df = aggregate_metrics_by_params(df)

            # Identify parameter columns for this specific detector
            param_cols = [c for c in agg_df.columns if c not in known_metrics]

            # Find best row
            if direction == "maximize":
                best_idx = agg_df[metric_key].idxmax()
            else:
                best_idx = agg_df[metric_key].idxmin()

            best_row = agg_df.loc[best_idx]
            score = best_row[metric_key]

            # Format parameters dynamically
            params_str_parts = []
            for p in param_cols:
                if p in best_row and pd.notna(best_row[p]):
                    short_name = param_map.get(p, p)
                    val = best_row[p]
                    # Format value nicely (remove trailing zeros if float)
                    if isinstance(val, float):
                        val_str = f"{val:g}"
                    else:
                        val_str = str(val)
                    params_str_parts.append(f"{short_name}={val_str}")

            params_str = ", ".join(params_str_parts)
            row[detector_name] = f"{score:.4f} ({params_str})"

        rows.append(row)

    return pd.DataFrame(rows)


def generate_metric_rankings(reports: Dict[str, Dict]) -> pd.DataFrame:
    """Rank detectors by each metric."""

    metrics_config = [
        ("f3_weighted_mean", "F3-Weighted", "maximize"),
        ("nab_score_standard_mean", "NAB Standard", "maximize"),
        ("recall_10s_mean", "Recall@10s", "maximize"),
        ("precision_10s_mean", "Precision@10s", "maximize"),
        ("fp_per_min_mean", "FP/min", "minimize"),
        ("edd_median_s_mean", "EDD Median", "minimize"),
    ]

    rows = []
    for metric_key, metric_name, direction in metrics_config:
        row = {"metric": metric_name}

        # Collect scores for this metric across detectors
        scores = {}
        for detector_name, report in reports.items():
            if report and "best_parameters" in report:
                # Try to get from f3_weighted best config (primary)
                best = report["best_parameters"].get("f3_weighted", {})

                # Handle NAB naming pattern
                if metric_key.startswith("nab_"):
                    # Extract from appropriate nab_* best config
                    nab_type = metric_key.replace("nab_score_", "").replace("_mean", "")
                    best = report["best_parameters"].get(f"nab_{nab_type}", best)

                score = best.get(metric_key)
                if score is not None and score != "N/A":
                    scores[detector_name] = float(score)

        # Rank
        if scores:
            if direction == "maximize":
                sorted_detectors = sorted(
                    scores.items(), key=lambda x: x[1], reverse=True
                )
            else:
                sorted_detectors = sorted(scores.items(), key=lambda x: x[1])

            for rank, (detector, score) in enumerate(sorted_detectors, 1):
                row[f"rank_{rank}"] = f"{detector} ({score:.4f})"

        rows.append(row)

    return pd.DataFrame(rows)


def aggregate_metrics_by_params(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate metrics by parameter configuration.
    Groups by all columns except metrics and metadata (record_id, etc.),
    calculating the mean for numeric metric columns.
    """
    # Columns to exclude from grouping (metadata + metrics)
    exclude_cols = {
        "record_id",
        "detector",
        "duration_samples",
        "duration_seconds",
        "n_ground_truth",
        "n_detections",
        "tp",
        "fp",
        "fn",
        "tp_weight_sum",
    }

    # Identify potential parameter columns (all columns that are NOT metrics/metadata)
    # We'll assume any column that is not in our known metric list and not excluded is a parameter
    known_metrics = {
        "f1_classic",
        "f1_weighted",
        "f3_classic",
        "f3_weighted",
        "recall_4s",
        "recall_10s",
        "precision_4s",
        "precision_10s",
        "edd_median_s",
        "edd_p95_s",
        "fp_per_min",
        "nab_score_standard",
        "nab_score_low_fp",
        "nab_score_low_fn",
    }

    # Filter columns present in df
    param_cols = [
        c for c in df.columns if c not in exclude_cols and c not in known_metrics
    ]
    metric_cols = [c for c in df.columns if c in known_metrics]

    if not param_cols:
        # If no parameters found (unlikely), return mean of everything
        return df[metric_cols].mean().to_frame().T

    # Group by parameters and calculate mean of metrics
    # We use as_index=False to keep parameters as columns
    aggregated = df.groupby(param_cols, as_index=False)[metric_cols].mean()

    return aggregated


def generate_robustness_analysis(metrics_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Analyze peak performance and parameter robustness.

    Robustness (Param Tolerance) is defined as the geometric mean of the
    normalized valid range for each parameter.

    For each parameter:
    Tolerance = (Max Good - Min Good) / (Max Tested - Min Tested)
    where "Good" means achieving >= 90% of the best score.
    """
    metrics_config = [
        ("f3_weighted", "F3-Weighted", "maximize"),
        ("f1_weighted", "F1-Weighted", "maximize"),
        ("nab_score_standard", "NAB Standard", "maximize"),
        ("nab_score_low_fp", "NAB Low FP", "maximize"),
        ("nab_score_low_fn", "NAB Low FN", "maximize"),
        ("recall_10s", "Recall@10s", "maximize"),
        ("precision_10s", "Precision@10s", "maximize"),
        ("fp_per_min", "FP/min", "minimize"),
        ("edd_median_s", "EDD Median", "minimize"),
    ]

    rows = []
    for metric_key, metric_name, direction in metrics_config:
        for detector_name, df in metrics_dfs.items():
            if metric_key not in df.columns:
                continue

            # Aggregate first!
            agg_df = aggregate_metrics_by_params(df)

            # Drop NaNs for the specific metric but keep index alignment
            # We need to operate on the subset where metric is valid
            valid_idx = agg_df[metric_key].dropna().index
            if len(valid_idx) == 0:
                continue

            # Work with the valid subset
            subset_df = agg_df.loc[valid_idx].copy()
            values = subset_df[metric_key]

            # Determine best value and threshold
            if direction == "maximize":
                best_val = values.max()
                top_10 = values.nlargest(10).mean()
                if best_val > 0:
                    threshold = best_val * 0.9
                else:
                    threshold = best_val - 0.1 * abs(best_val)

                good_mask = values >= threshold
            else:
                best_val = values.min()
                top_10 = values.nsmallest(10).mean()
                threshold = best_val + 0.1 * abs(best_val)
                good_mask = values <= threshold

            # Calculate Parameter Tolerance
            known_metrics = {
                "f1_classic",
                "f1_weighted",
                "f3_classic",
                "f3_weighted",
                "recall_4s",
                "recall_10s",
                "precision_4s",
                "precision_10s",
                "edd_median_s",
                "edd_p95_s",
                "fp_per_min",
                "nab_score_standard",
                "nab_score_low_fp",
                "nab_score_low_fn",
            }
            param_cols = [c for c in agg_df.columns if c not in known_metrics]

            tolerances = []
            for param in param_cols:
                # Check if parameter is numeric and NOT boolean
                # Boolean columns (bool or object-bool) cause subtraction errors
                if not pd.api.types.is_numeric_dtype(subset_df[param]):
                    continue
                if pd.api.types.is_bool_dtype(subset_df[param]):
                    continue

                full_min = subset_df[param].min()
                full_max = subset_df[param].max()
                full_range = full_max - full_min

                if full_range == 0:
                    tolerances.append(1.0)
                    continue

                # Apply mask to subset_df
                good_params = subset_df.loc[good_mask, param]
                if good_params.empty:
                    tolerances.append(0.0)
                    continue

                good_min = good_params.min()
                good_max = good_params.max()
                good_range = good_max - good_min

                tolerances.append(good_range / full_range)

            # Geometric mean of tolerances
            if tolerances:
                # add small epsilon to avoid 0
                import numpy as np

                geo_mean = np.exp(np.mean(np.log(np.array(tolerances) + 1e-6)))
                robust_score = geo_mean * 100.0
            else:
                robust_score = 0.0

            rows.append(
                {
                    "Metric": metric_name,
                    "Detector": detector_name,
                    "Best": f"{best_val:.4f}",
                    "Top-10 Mean": f"{top_10:.4f}",
                    "Param Tolerance (%)": f"{robust_score:.1f}%",
                    "Total Configs": len(values),
                }
            )

    return pd.DataFrame(rows)


def generate_constrained_analysis(metrics_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Analyze trade-offs (e.g., Best Precision when Recall > X).
    """
    rows = []

    # Scenario 1: High Recall Requirement (Recall > 0.8) -> Maximize Precision
    for detector_name, df in metrics_dfs.items():
        # Aggregate first!
        agg_df = aggregate_metrics_by_params(df)

        if "recall_10s" in agg_df.columns and "precision_10s" in agg_df.columns:
            subset = agg_df[agg_df["recall_10s"] >= 0.8]
            if not subset.empty:
                best_prec = subset["precision_10s"].max()
                rows.append(
                    {
                        "Scenario": "High Recall (>0.8)",
                        "Target": "Max Precision",
                        "Detector": detector_name,
                        "Score": f"{best_prec:.4f}",
                    }
                )
            else:
                rows.append(
                    {
                        "Scenario": "High Recall (>0.8)",
                        "Target": "Max Precision",
                        "Detector": detector_name,
                        "Score": "N/A (No config found)",
                    }
                )

    # Scenario 2: High Precision Requirement (Precision > 0.8) -> Maximize Recall
    for detector_name, df in metrics_dfs.items():
        agg_df = aggregate_metrics_by_params(df)

        if "recall_10s" in agg_df.columns and "precision_10s" in agg_df.columns:
            subset = agg_df[agg_df["precision_10s"] >= 0.8]
            if not subset.empty:
                best_rec = subset["recall_10s"].max()
                rows.append(
                    {
                        "Scenario": "High Precision (>0.8)",
                        "Target": "Max Recall",
                        "Detector": detector_name,
                        "Score": f"{best_rec:.4f}",
                    }
                )
            else:
                rows.append(
                    {
                        "Scenario": "High Precision (>0.8)",
                        "Target": "Max Recall",
                        "Detector": detector_name,
                        "Score": "N/A (No config found)",
                    }
                )

    # Scenario 3: Balanced (F1 > 0.8) -> Minimize Delay
    for detector_name, df in metrics_dfs.items():
        agg_df = aggregate_metrics_by_params(df)

        if "f1_weighted" in agg_df.columns and "edd_median_s" in agg_df.columns:
            subset = agg_df[agg_df["f1_weighted"] >= 0.8]
            if not subset.empty:
                best_edd = subset["edd_median_s"].min()
                rows.append(
                    {
                        "Scenario": "High F1 (>0.8)",
                        "Target": "Min Delay (s)",
                        "Detector": detector_name,
                        "Score": f"{best_edd:.4f}",
                    }
                )
            else:
                rows.append(
                    {
                        "Scenario": "High F1 (>0.8)",
                        "Target": "Min Delay (s)",
                        "Detector": detector_name,
                        "Score": "N/A",
                    }
                )

    return pd.DataFrame(rows)


def generate_markdown_report(
    detectors: List[str],
    best_configs: pd.DataFrame,
    rankings: pd.DataFrame,
    robustness: pd.DataFrame,
    tradeoffs: pd.DataFrame,
    output_path: Path,
):
    """Generate comprehensive markdown comparison report."""

    with open(output_path, "w") as f:
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

        # Robustness
        if not robustness.empty:
            f.write("## 3. Performance & Robustness Analysis\n\n")
            f.write("Analysis of peak performance and parameter sensitivity.\n")
            f.write("- **Best**: The single highest score achieved.\n")
            f.write(
                "- **Top-10 Mean**: Average of the top 10 configurations (indicates stability of the peak).\n"
            )
            f.write(
                "- **Param Tolerance**: Geometric mean of the normalized valid range for each parameter. "
                "Indicates how much you can vary parameters (0% to 100% of tested range) while maintaining >90% performance.\n\n"
            )
            f.write(robustness.to_markdown(index=False))
            f.write("\n\n")

        # Trade-offs
        if not tradeoffs.empty:
            f.write("## 4. Trade-off Analysis (Constrained Optimization)\n\n")
            f.write(
                "Performance in specific scenarios (e.g., 'What is the best Precision I can get if I need Recall > 0.8?').\n\n"
            )
            f.write(tradeoffs.to_markdown(index=False))
            f.write("\n\n")

        # Recommendations
        f.write("## 5. Recommendations\n\n")
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
        f.write(
            "- F3-weighted: Emphasizes recall with temporal weighting (primary metric)\n"
        )
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
        description="Compare results from multiple change point detectors"
    )
    parser.add_argument(
        "--detectors",
        nargs="+",
        default=["adwin", "page_hinkley", "kswin", "hddm_a", "hddm_w", "floss"],
        help="List of detector names to compare (e.g., adwin page_hinkley kswin hddm_a hddm_w)",
    )
    parser.add_argument(
        "--results-dir",
        default="results",
        help="Base directory containing detector results",
    )
    parser.add_argument(
        "--dataset",
        default="afib_paroxysmal",
        help="Dataset name to compare (default: afib_paroxysmal). This should match the folder inside results/; _full/_tidy suffixes are automatically stripped.",
    )
    parser.add_argument(
        "--table-output",
        default=None,
        help="Output path for a table with summarized metrics per detector (default: comparisons/<dataset>/detector_summary.csv)",
    )
    parser.add_argument(
        "--stat-top-percent",
        type=float,
        default=10.0,
        help="When computing statistical comparisons, restrict to the top X percent of parameter combinations by `--stat-metric`. Set 0 to use all combinations (default: 10)",
    )
    parser.add_argument(
        "--stat-metric",
        default="f3_weighted",
        help="Metric to use for selecting top performing parameter combinations when --stat-top-percent > 0 (default: f3_weighted)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path for markdown report (default: comparisons/<dataset>/comparative_report.md)",
    )
    parser.add_argument(
        "--csv-output",
        default=None,
        help="Output path for rankings CSV (default: comparisons/<dataset>/detector_rankings.csv)",
    )

    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    dataset_name = args.dataset
    # Clean dataset name (strip _full, _tidy*) to match sanitized results folder
    import re

    clean_dataset = re.sub(r"(_full$|_tidy.*$)", "", dataset_name)

    # Determine output directory and paths
    base_output_dir = Path("comparisons") / clean_dataset

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = base_output_dir / "comparative_report.md"

    if args.csv_output:
        csv_output_path = Path(args.csv_output)
    else:
        csv_output_path = base_output_dir / "detector_rankings.csv"

    if args.table_output:
        table_output_path = Path(args.table_output)
    else:
        table_output_path = base_output_dir / "detector_summary.csv"

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    csv_output_path.parent.mkdir(parents=True, exist_ok=True)
    table_output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Comparing detectors: {', '.join(args.detectors)}")
    print(f"Results directory: {results_dir}")
    print(f"Dataset (clean): {clean_dataset}")
    print(f"Output directory: {base_output_dir}")
    print()

    # Load reports
    print("Loading detector reports...")
    reports = {}
    for detector in args.detectors:
        # Try the cleaned dataset folder first, then fallback to original dataset name
        report = load_detector_report(detector, results_dir / clean_dataset)
        if report is None:
            report = load_detector_report(detector, results_dir / dataset_name)
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
        df = load_detector_metrics(detector, results_dir / clean_dataset)
        if df is None:
            df = load_detector_metrics(detector, results_dir / dataset_name)
        if df is not None:
            metrics_dfs[detector] = df
            print(f"  ✓ {detector} ({len(df)} evaluations)")
        else:
            print(f"  ✗ {detector} (not found)")

    print()

    # Generate comparisons
    print("Generating comparisons...")
    best_configs = generate_best_configs_table(metrics_dfs)
    rankings = generate_metric_rankings(reports)
    # stats = generate_statistical_comparison(metrics_dfs, top_percent=args.stat_top_percent, stat_metric=args.stat_metric)
    robustness = generate_robustness_analysis(metrics_dfs)
    tradeoffs = generate_constrained_analysis(metrics_dfs)

    # Save rankings CSV
    rankings.to_csv(csv_output_path, index=False)
    print(f"  ✓ Rankings saved: {csv_output_path}")

    # Save summarized table with mean metric values per detector
    def summarize_metrics_per_detector(metrics_dfs: Dict[str, pd.DataFrame]):
        metrics_of_interest = [
            "f3_weighted",
            "f1_weighted",
            "recall_10s",
            "precision_10s",
            "fp_per_min",
            "edd_median_s",
            "nab_score_standard",
        ]

        rows = []
        for detector_name, df in metrics_dfs.items():
            if df is None or df.empty:
                continue
            row = {"detector": detector_name}
            for metric in metrics_of_interest:
                if metric in df.columns:
                    row[f"{metric}_mean"] = df[metric].mean()
                    row[f"{metric}_median"] = df[metric].median()
                else:
                    row[f"{metric}_mean"] = None
                    row[f"{metric}_median"] = None
            rows.append(row)

        return pd.DataFrame(rows)

    summary_table = summarize_metrics_per_detector(metrics_dfs)
    summary_table.to_csv(table_output_path, index=False)
    print(f"  ✓ Summary table saved: {table_output_path}")

    # Generate markdown report
    generate_markdown_report(
        args.detectors, best_configs, rankings, robustness, tradeoffs, output_path
    )
    print(f"  ✓ Report saved: {output_path}")

    print()
    print("✅ Comparison complete!")
    print(f"\nView report: {output_path}")


if __name__ == "__main__":
    main()
