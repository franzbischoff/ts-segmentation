#!/usr/bin/env python3
"""
Cross-Dataset Analysis: Macro-Average

Calculates macro-average (simple mean) of metrics across multiple datasets
for each parameter configuration, to identify robust settings that generalize well.

Usage:
    python -m src.cross_dataset_analysis --detector adwin --output results/cross_dataset_analysis/adwin/
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_dataset_metrics(
    detector: str, dataset: str, base_dir: str = "results"
) -> pd.DataFrame:
    """
    Load metrics CSV for a specific detector and dataset.

    Args:
        detector: Detector name (e.g., 'adwin')
        dataset: Dataset name (e.g., 'afib_paroxysmal')
        base_dir: Base results directory

    Returns:
        DataFrame with metrics, adding 'dataset' column
    """
    metrics_path = (
        Path(base_dir) / dataset / detector / "metrics_comprehensive_with_nab.csv"
    )

    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics not found: {metrics_path}")

    logger.info(f"Loading metrics from: {metrics_path}")
    df = pd.read_csv(metrics_path)
    df["dataset"] = dataset

    logger.info(f"  Loaded {len(df)} configurations from {dataset}")
    return df


def identify_parameter_columns(df: pd.DataFrame) -> List[str]:
    """
    Identify parameter columns (exclude metrics and metadata).

    Args:
        df: DataFrame with metrics

    Returns:
        List of parameter column names
    """
    # Exclude known metadata/result columns
    exclude_cols = {
        # Metadata
        "record_id",
        "detector",
        "dataset",
        # Data statistics
        "duration_samples",
        "duration_seconds",
        "n_ground_truth",
        "n_detections",
        # Confusion matrix
        "tp",
        "fp",
        "fn",
        "tp_weight_sum",
        # F-scores
        "f1_classic",
        "f1_weighted",
        "f3_classic",
        "f3_weighted",
        # Temporal metrics
        "recall_4s",
        "recall_10s",
        "precision_4s",
        "precision_10s",
        "edd_median_s",
        "edd_p95_s",
        "fp_per_min",
        # NAB scores
        "nab_score_standard",
        "nab_score_low_fp",
        "nab_score_low_fn",
    }

    param_cols = [col for col in df.columns if col not in exclude_cols]

    return param_cols


def calculate_file_weighted_average(
    datasets_dfs: List[pd.DataFrame],
    param_cols: List[str],
    metric_col: str = "f3_weighted",
) -> pd.DataFrame:
    """
    Calculate FILE-WEIGHTED average (micro-average) across datasets.

    This concatenates all files from all datasets and calculates mean,
    giving more weight to datasets with more files.

    Args:
        datasets_dfs: List of DataFrames, one per dataset
        param_cols: Parameter column names
        metric_col: Metric column to average

    Returns:
        DataFrame with file-weighted averages, ranked by score
    """
    # Concatenate all datasets (all files)
    all_data = pd.concat(datasets_dfs, ignore_index=True)

    logger.info(f"Calculating FILE-WEIGHTED average for {len(all_data)} total rows")
    logger.info(f"  Parameter columns: {param_cols}")
    logger.info(f"  Metric column: {metric_col}")

    # Group by parameter configuration
    grouped = all_data.groupby(param_cols, dropna=False)

    # Calculate file-weighted average (mean of ALL files)
    file_weighted_avg = grouped[metric_col].mean().reset_index()
    file_weighted_avg.rename(columns={metric_col: f"{metric_col}_file_weighted_avg"}, inplace=True)

    # Calculate std (robustness indicator)
    file_weighted_std = grouped[metric_col].std().reset_index()
    file_weighted_std.rename(columns={metric_col: f"{metric_col}_std"}, inplace=True)

    # Count number of datasets with this config
    n_datasets = grouped["dataset"].nunique().reset_index()
    n_datasets.rename(columns={"dataset": "n_datasets"}, inplace=True)

    # Merge all statistics
    result = file_weighted_avg.merge(file_weighted_std, on=param_cols)
    result = result.merge(n_datasets, on=param_cols)

    # Sort by file-weighted average (descending)
    result = result.sort_values(f"{metric_col}_file_weighted_avg", ascending=False).reset_index(drop=True)

    logger.info(f"Calculated file-weighted average for {len(result)} unique configurations")

    return result


def calculate_true_macro_average(
    datasets_dfs: List[pd.DataFrame],
    param_cols: List[str],
    metric_col: str = "f3_weighted",
) -> pd.DataFrame:
    """
    Calculate TRUE MACRO-AVERAGE across datasets.

    This first calculates the mean PER DATASET, then averages those means.
    Each dataset contributes equally (1/3 each), regardless of number of files.

    Args:
        datasets_dfs: List of DataFrames, one per dataset
        param_cols: Parameter column names
        metric_col: Metric column to average

    Returns:
        DataFrame with macro-averaged metrics, ranked by score
    """
    logger.info(f"Calculating TRUE MACRO-AVERAGE (per-dataset means)")
    logger.info(f"  Parameter columns: {param_cols}")
    logger.info(f"  Metric column: {metric_col}")

    # Step 1: Calculate mean per dataset
    dataset_means = []
    for df in datasets_dfs:
        dataset_name = df['dataset'].iloc[0]
        logger.info(f"  Calculating mean for {dataset_name} ({len(df)} files)")

        # Group by parameters and calculate mean within this dataset
        dataset_avg = df.groupby(param_cols, dropna=False)[metric_col].mean().reset_index()
        dataset_avg.rename(columns={metric_col: f"{metric_col}_{dataset_name}"}, inplace=True)
        dataset_means.append(dataset_avg)

    # Step 2: Merge all dataset means
    result = dataset_means[0]
    for dataset_avg in dataset_means[1:]:
        result = result.merge(dataset_avg, on=param_cols, how='outer')

    # Step 3: Calculate macro-average (mean of dataset means)
    dataset_cols = [col for col in result.columns if metric_col in col and col != metric_col]
    result[f"{metric_col}_macro_avg"] = result[dataset_cols].mean(axis=1)

    # Step 4: Calculate std across datasets (robustness)
    result[f"{metric_col}_std"] = result[dataset_cols].std(axis=1)

    # Step 5: Count number of datasets with this config
    result['n_datasets'] = result[dataset_cols].notna().sum(axis=1)

    # Sort by macro-average (descending)
    result = result.sort_values(f"{metric_col}_macro_avg", ascending=False).reset_index(drop=True)

    # Keep only essential columns
    essential_cols = param_cols + [f"{metric_col}_macro_avg", f"{metric_col}_std", 'n_datasets']
    result = result[essential_cols]

    logger.info(f"Calculated TRUE macro-average for {len(result)} unique configurations")
    logger.info(f"  Each dataset weighted equally: 1/{len(datasets_dfs)}")

    return result



def generate_report(
    rankings_df: pd.DataFrame,
    param_cols: List[str],
    detector: str,
    datasets: List[str],
    metric_col: str = "f3_weighted",
    mode: str = "true_macro",
) -> Dict:
    """
    Generate JSON report with top configurations.

    Args:
        rankings_df: DataFrame with ranked configurations
        param_cols: Parameter column names
        detector: Detector name
        datasets: List of dataset names
        metric_col: Metric column used
        mode: Aggregation mode ('file_weighted' or 'true_macro')

    Returns:
        Report dictionary
    """
    top_10 = rankings_df.head(10)

    # Determine correct column names based on mode
    if mode == "file_weighted":
        avg_col = f"{metric_col}_file_weighted_avg"
        score_key = "file_weighted_avg_score"
        method_desc = "file-weighted average (micro-average: all files concatenated, larger datasets have more weight)"
    else:  # true_macro
        avg_col = f"{metric_col}_macro_avg"
        score_key = "macro_avg_score"
        method_desc = "true macro-average (mean of dataset means, each dataset weighted equally: 1/3)"

    # Convert top configs to list of dicts
    top_configs = []
    for idx, row in top_10.iterrows():
        config = {col: row[col] for col in param_cols}
        config[score_key] = float(row[avg_col])
        config["std_across_datasets"] = float(row[f"{metric_col}_std"])
        config["n_datasets"] = int(row["n_datasets"])
        config["rank"] = int(idx) + 1
        top_configs.append(config)

    # Overall statistics
    best_config = top_configs[0] if top_configs else None

    report = {
        "detector": detector,
        "datasets": datasets,
        "metric": metric_col,
        "aggregation_mode": mode,
        "aggregation_method": method_desc,
        "total_configurations": len(rankings_df),
        "best_configuration": best_config,
        "top_10_configurations": top_configs,
        "statistics": {
            f"mean_{mode}": float(rankings_df[avg_col].mean()),
            f"median_{mode}": float(rankings_df[avg_col].median()),
            f"max_{mode}": float(rankings_df[avg_col].max()),
            "min_std": float(rankings_df[f"{metric_col}_std"].min()),
            "max_std": float(rankings_df[f"{metric_col}_std"].max()),
        },
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Cross-dataset analysis: Calculate macro-average of metrics"
    )
    parser.add_argument(
        "--detector",
        type=str,
        required=True,
        help="Detector name (e.g., adwin, page_hinkley)",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["afib_paroxysmal", "malignantventricular", "vtachyarrhythmias"],
        help="List of datasets to include (default: all 3)",
    )
    parser.add_argument(
        "--metric",
        type=str,
        default="f3_weighted",
        help="Metric column to aggregate (default: f3_weighted)",
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default="results",
        help="Base directory for results (default: results)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["file_weighted", "true_macro"],
        default="true_macro",
        help="Aggregation mode: 'file_weighted' (all files concatenated, favors larger datasets) or 'true_macro' (mean of dataset means, equal weight per dataset). Default: true_macro",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory (default: results/cross_dataset_analysis/<detector>)",
    )

    args = parser.parse_args()

    # Set output directory
    if args.output is None:
        output_dir = Path(args.base_dir) / "cross_dataset_analysis" / args.detector
    else:
        output_dir = Path(args.output)

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Aggregation mode: {args.mode}")

    # Load metrics from all datasets
    logger.info(f"\nLoading metrics for detector: {args.detector}")
    datasets_dfs = []
    for dataset in args.datasets:
        try:
            df = load_dataset_metrics(args.detector, dataset, args.base_dir)
            datasets_dfs.append(df)
        except FileNotFoundError as e:
            logger.warning(f"Skipping {dataset}: {e}")

    if not datasets_dfs:
        logger.error("No datasets loaded. Exiting.")
        return

    logger.info(f"\nSuccessfully loaded {len(datasets_dfs)} datasets")

    # Identify parameter columns
    param_cols = identify_parameter_columns(datasets_dfs[0])
    logger.info(f"Detected parameter columns: {param_cols}")

    # Calculate average based on mode
    if args.mode == "file_weighted":
        logger.info(f"\nCalculating FILE-WEIGHTED average...")
        rankings_df = calculate_file_weighted_average(datasets_dfs, param_cols, args.metric)
        rankings_csv = output_dir / "file_weighted_rankings.csv"
        avg_col_name = "file_weighted_avg"
    else:  # true_macro
        logger.info(f"\nCalculating TRUE MACRO-AVERAGE...")
        rankings_df = calculate_true_macro_average(datasets_dfs, param_cols, args.metric)
        rankings_csv = output_dir / "true_macro_average_rankings.csv"
        avg_col_name = "macro_avg"

    # Save rankings CSV
    rankings_df.to_csv(rankings_csv, index=False)
    logger.info(f"\n✅ Saved rankings to: {rankings_csv}")
    logger.info(f"   {len(rankings_df)} configurations ranked")

    # Generate and save report
    report = generate_report(
        rankings_df, param_cols, args.detector, args.datasets, args.metric, args.mode
    )
    report_json = output_dir / f"{args.mode}_report.json"
    with open(report_json, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"✅ Saved report to: {report_json}")

    # Display top 5 configurations
    print("\n" + "=" * 80)
    print(f"TOP 5 CONFIGURATIONS (by {args.metric} {args.mode})")
    print("=" * 80)
    for idx, config in enumerate(report["top_10_configurations"][:5], 1):
        print(f"\nRank #{idx}:")
        for key, value in config.items():
            if key in param_cols:
                print(f"  {key}: {value}")
        print(f"  → Average score: {config[f'{avg_col_name}_score']:.4f}")
        print(f"  → Std across datasets: {config['std_across_datasets']:.4f}")
        print(f"  → Present in {config['n_datasets']} datasets")

    print("\n" + "=" * 80)
    print(f"Best configuration: {report['best_configuration']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
