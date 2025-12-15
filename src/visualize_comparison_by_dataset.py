"""
Visualize comparison of multiple detectors for a single dataset.

Generates 4 plots:
1. radar_6detectors.png - Radar chart (6 detectors × 6 metrics)
2. f3_vs_fp_scatter.png - Scatter plot (F3 vs FP/min trade-off)
3. heatmap_metrics_comparison.png - Heatmap (6 detectors × 7 metrics)
4. parameter_tradeoffs.png - 3D scatter (Recall × FP × EDD)

Usage:
    python -m src.visualize_comparison_by_dataset \
        --dataset afib_paroxysmal \
        --output-dir results/comparisons/by_dataset/afib_paroxysmal/visualizations
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm
from matplotlib.patches import Circle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Detector color scheme (consistent across all plots)
DETECTOR_COLORS = {
    'adwin': '#1f77b4',        # Blue
    'page_hinkley': '#2ca02c', # Green
    'kswin': '#ff7f0e',        # Orange
    'hddm_a': '#d62728',       # Red
    'hddm_w': '#9467bd',       # Purple
    'floss': '#7f7f7f'         # Gray
}

DETECTOR_LABELS = {
    'adwin': 'ADWIN',
    'page_hinkley': 'Page-Hinkley',
    'kswin': 'KSWIN',
    'hddm_a': 'HDDM_A',
    'hddm_w': 'HDDM_W',
    'floss': 'FLOSS'
}


def load_detector_metrics(dataset: str, detector: str, results_base: Path) -> pd.DataFrame:
    """Load metrics CSV for a detector."""
    metrics_path = results_base / dataset / detector / 'metrics_comprehensive_with_nab.csv'

    if not metrics_path.exists():
        logger.warning(f"Metrics file not found: {metrics_path}")
        return pd.DataFrame()

    logger.info(f"Loading {detector} metrics from {metrics_path}")
    return pd.read_csv(metrics_path)


def load_best_configs(dataset: str, detector: str, results_base: Path) -> Dict:
    """Load best configurations from final report JSON."""
    report_path = results_base / dataset / detector / 'final_report_with_nab.json'

    if not report_path.exists():
        logger.warning(f"Report file not found: {report_path}")
        return {}

    with open(report_path, 'r') as f:
        report = json.load(f)

    return report.get('best_parameters', {})


def normalize_metric(values: np.ndarray, invert: bool = False) -> np.ndarray:
    """Normalize metric values to [0, 1] range."""
    if len(values) == 0 or np.all(np.isnan(values)):
        return values

    min_val = np.nanmin(values)
    max_val = np.nanmax(values)

    if max_val == min_val:
        return np.ones_like(values) * 0.5

    normalized = (values - min_val) / (max_val - min_val)

    if invert:
        normalized = 1 - normalized

    return normalized


def create_radar_chart(detector_metrics: Dict[str, Dict], output_path: Path):
    """
    Create radar chart comparing 6 detectors across 4 core metrics.

    All metrics use interpretable scales:
    - F3, Recall, Precision: 0-100% (actual values)
    - EDD: 0-10s scale (inverted: lower EDD = higher on radar)

    Metrics:
    1. F3-weighted (0-1, higher better)
    2. Recall@10s (0-1, higher better)
    3. Precision@10s (0-1, higher better)
    4. Fast Detection (0-10s, inverted - lower better)
    """
    logger.info("Creating radar chart...")

    # Define metrics to plot
    # Format: (key, label, invert, skip_normalization, fixed_scale)
    metrics = [
        ('f3_weighted', 'F3-Weighted', False, True, None),           # Already 0-1
        ('recall_10s', 'Recall@10s', False, True, None),             # Already 0-1
        ('precision_10s', 'Precision@10s', False, True, None),       # Already 0-1
        ('edd_median_s', 'Fast Detection', True, True, (0, 10))      # Fixed 0-10s scale + inversion
    ]

    # Collect data
    detectors = []
    values_matrix = []

    for detector, data in detector_metrics.items():
        if not data:
            continue

        detectors.append(detector)
        row = []

        for metric_key, _, _, _, _ in metrics:
            value = data.get(metric_key, np.nan)
            row.append(value)

        values_matrix.append(row)

    if not values_matrix:
        logger.warning("No data for radar chart")
        return

    # Process each metric column
    values_matrix = np.array(values_matrix)
    for i, (_, _, invert, skip_norm, fixed_scale) in enumerate(metrics):
        if skip_norm and fixed_scale is None:
            # Keep original values (already in [0, 1])
            pass
        elif fixed_scale is not None:
            # Apply fixed scale
            min_scale, max_scale = fixed_scale
            # Clip values to scale and normalize
            clipped = np.clip(values_matrix[:, i], min_scale, max_scale)
            values_matrix[:, i] = (clipped - min_scale) / (max_scale - min_scale)
            if invert:
                values_matrix[:, i] = 1 - values_matrix[:, i]
        else:
            # Normalize to [0, 1] based on actual values
            values_matrix[:, i] = normalize_metric(values_matrix[:, i], invert=invert)

    # Set up radar chart
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle

    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))

    # Plot each detector
    for idx, detector in enumerate(detectors):
        values = values_matrix[idx].tolist()
        values += values[:1]  # Complete the circle

        color = DETECTOR_COLORS.get(detector, '#000000')
        label = DETECTOR_LABELS.get(detector, detector.upper())

        ax.plot(angles, values, 'o-', linewidth=2, label=label, color=color)
        ax.fill(angles, values, alpha=0.15, color=color)

    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([m[1] for m in metrics], size=11)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=9)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Title and legend
    ax.set_title('Multi-Detector Performance Radar\n(F3/Recall/Precision: % | Fast Detection: 0-10s scale)',
                 size=14, weight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10, ncol=2)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Radar chart saved: {output_path}")


def create_f3_vs_fp_scatter(detector_metrics: Dict[str, Dict], output_path: Path):
    """
    Create scatter plot showing F3-weighted vs FP/min trade-off.
    Bubble size represents Recall@10s.
    """
    logger.info("Creating F3 vs FP scatter plot...")

    fig, ax = plt.subplots(figsize=(12, 8))

    for detector, data in detector_metrics.items():
        if not data:
            continue

        f3 = data.get('f3_weighted', np.nan)
        fp = data.get('fp_per_min', np.nan)
        recall = data.get('recall_10s', 0.5) * 100  # For sizing

        if np.isnan(f3) or np.isnan(fp):
            continue

        color = DETECTOR_COLORS.get(detector, '#000000')
        label = DETECTOR_LABELS.get(detector, detector.upper())

        # Bubble size proportional to recall
        size = 100 + recall * 8  # Base size + scaled recall

        ax.scatter(fp, f3, s=size, alpha=0.6, color=color,
                  edgecolors='black', linewidth=1.5, label=label)

        # Annotate
        ax.annotate(label, (fp, f3), xytext=(8, 8), textcoords='offset points',
                   fontsize=10, weight='bold')

    # Labels and styling
    ax.set_xlabel('False Positives per Minute (FP/min)', fontsize=13, weight='bold')
    ax.set_ylabel('F3-Weighted Score', fontsize=13, weight='bold')
    ax.set_title('Performance Trade-off: F3 vs False Alarm Rate\n(Bubble size = Recall@10s)',
                fontsize=16, weight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='best', fontsize=10, ncol=2)

    # Add quadrant annotations
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    mid_x = (xlim[0] + xlim[1]) / 2
    mid_y = (ylim[0] + ylim[1]) / 2

    ax.text(xlim[1] * 0.95, ylim[1] * 0.95, 'High F3\nHigh FP',
           ha='right', va='top', fontsize=9, alpha=0.5, style='italic')
    ax.text(xlim[0] + (xlim[1] - xlim[0]) * 0.05, ylim[1] * 0.95, 'High F3\nLow FP ✓',
           ha='left', va='top', fontsize=9, alpha=0.5, style='italic', weight='bold')
    ax.text(xlim[1] * 0.95, ylim[0] + (ylim[1] - ylim[0]) * 0.05, 'Low F3\nHigh FP',
           ha='right', va='bottom', fontsize=9, alpha=0.5, style='italic')
    ax.text(xlim[0] + (xlim[1] - xlim[0]) * 0.05, ylim[0] + (ylim[1] - ylim[0]) * 0.05,
           'Low F3\nLow FP',
           ha='left', va='bottom', fontsize=9, alpha=0.5, style='italic')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ F3 vs FP scatter saved: {output_path}")


def create_heatmap_comparison(detector_metrics: Dict[str, Dict], output_path: Path):
    """
    Create heatmap showing 6 detectors × 7 metrics.
    Values are normalized per metric column.
    """
    logger.info("Creating heatmap comparison...")

    # Define metrics
    metrics = [
        ('f3_weighted', 'F3-Weighted'),
        ('f3_classic', 'F3-Classic'),
        ('recall_10s', 'Recall@10s'),
        ('precision_10s', 'Precision@10s'),
        ('fp_per_min', 'FP/min'),
        ('edd_median_s', 'EDD (s)'),
        ('nab_score_standard', 'NAB Standard')
    ]

    # Collect data
    detectors = []
    data_matrix = []

    for detector, data in detector_metrics.items():
        if not data:
            continue

        detectors.append(DETECTOR_LABELS.get(detector, detector.upper()))
        row = [data.get(m[0], np.nan) for m in metrics]
        data_matrix.append(row)

    if not data_matrix:
        logger.warning("No data for heatmap")
        return

    df = pd.DataFrame(data_matrix, index=detectors, columns=[m[1] for m in metrics])

    # Normalize each column
    df_normalized = df.copy()
    for col in df.columns:
        # Invert FP/min and EDD (lower is better)
        if col in ['FP/min', 'EDD (s)']:
            df_normalized[col] = normalize_metric(df[col].values, invert=True)
        # Invert NAB (less negative is better)
        elif col == 'NAB Standard':
            df_normalized[col] = normalize_metric(df[col].values, invert=True)
        else:
            df_normalized[col] = normalize_metric(df[col].values, invert=False)

    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(df_normalized, annot=df.round(3), fmt='', cmap='RdYlGn',
                center=0.5, vmin=0, vmax=1, linewidths=1, linecolor='white',
                cbar_kws={'label': 'Normalized Score (0=worst, 1=best)'},
                ax=ax, annot_kws={'size': 10})

    ax.set_title('Detector Performance Heatmap (Normalized by Metric)',
                fontsize=16, weight='bold', pad=15)
    ax.set_xlabel('Metrics', fontsize=13, weight='bold')
    ax.set_ylabel('Detectors', fontsize=13, weight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Heatmap saved: {output_path}")


def create_3d_tradeoff(detector_metrics: Dict[str, Dict], output_path: Path):
    """
    Create 3D scatter plot showing Recall@10s × FP/min × EDD trade-offs.
    Color represents F3-weighted score.
    """
    logger.info("Creating 3D trade-off plot...")

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    for detector, data in detector_metrics.items():
        if not data:
            continue

        recall = data.get('recall_10s', np.nan) * 100  # Percentage
        fp = data.get('fp_per_min', np.nan)
        edd = data.get('edd_median_s', np.nan)
        f3 = data.get('f3_weighted', np.nan)

        if any(np.isnan([recall, fp, edd, f3])):
            continue

        color = DETECTOR_COLORS.get(detector, '#000000')
        label = DETECTOR_LABELS.get(detector, detector.upper())

        # Plot point
        ax.scatter(recall, fp, edd, s=200, alpha=0.7, color=color,
                  edgecolors='black', linewidth=2, label=label)

        # Annotate
        ax.text(recall, fp, edd, f'  {label}', fontsize=9, weight='bold')

    # Labels and styling
    ax.set_xlabel('Recall@10s (%)', fontsize=12, weight='bold', labelpad=10)
    ax.set_ylabel('FP/min', fontsize=12, weight='bold', labelpad=10)
    ax.set_zlabel('EDD (seconds)', fontsize=12, weight='bold', labelpad=10)
    ax.set_title('3D Performance Trade-off: Recall × FP × Detection Speed',
                fontsize=16, weight='bold', pad=20)

    # Legend
    ax.legend(loc='upper left', fontsize=10, ncol=2)

    # Grid
    ax.grid(True, alpha=0.3)

    # View angle
    ax.view_init(elev=20, azim=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ 3D trade-off plot saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate comparison visualizations for multiple detectors on a single dataset'
    )
    parser.add_argument('--dataset', required=True,
                       choices=['afib_paroxysmal', 'malignantventricular', 'vtachyarrhythmias'],
                       help='Dataset name')
    parser.add_argument('--output-dir', type=Path, required=True,
                       help='Output directory for PNG files')
    parser.add_argument('--results-base', type=Path, default=Path('results'),
                       help='Base directory for results (default: results/)')
    parser.add_argument('--detectors', nargs='+',
                       default=['adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w', 'floss'],
                       help='List of detectors to include')

    args = parser.parse_args()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting visualization for dataset: {args.dataset}")
    logger.info(f"Detectors: {', '.join(args.detectors)}")

    # Load best configurations for each detector
    detector_metrics = {}

    for detector in args.detectors:
        best_configs = load_best_configs(args.dataset, detector, args.results_base)

        # Get best config for f3_weighted (primary metric)
        if 'f3_weighted' in best_configs:
            config = best_configs['f3_weighted']
            # Extract mean values (with _mean suffix in JSON)
            detector_metrics[detector] = {
                'f3_weighted': config.get('f3_weighted_mean', np.nan),
                'f3_classic': config.get('f3_classic_mean', np.nan),
                'f1_weighted': config.get('f1_weighted_mean', np.nan),
                'f1_classic': config.get('f1_classic_mean', np.nan),
                'recall_4s': config.get('recall_4s_mean', np.nan),
                'recall_10s': config.get('recall_10s_mean', np.nan),
                'precision_4s': config.get('precision_4s_mean', np.nan),
                'precision_10s': config.get('precision_10s_mean', np.nan),
                'fp_per_min': config.get('fp_per_min_mean', np.nan),
                'edd_median_s': config.get('edd_median_s_mean', np.nan),
                'nab_score_standard': config.get('nab_score_standard_mean', np.nan),
                'nab_score_low_fp': config.get('nab_score_low_fp_mean', np.nan),
                'nab_score_low_fn': config.get('nab_score_low_fn_mean', np.nan),
            }
            f3_value = detector_metrics[detector].get('f3_weighted', np.nan)
            recall_value = detector_metrics[detector].get('recall_10s', np.nan)
            fp_value = detector_metrics[detector].get('fp_per_min', np.nan)

            if not np.isnan(f3_value):
                logger.info(f"✓ {detector:15s}: F3={f3_value:.4f}, Recall@10s={recall_value*100:.1f}%, FP/min={fp_value:.2f}")
        else:
            logger.warning(f"✗ {detector:15s}: No f3_weighted config in report")
            detector_metrics[detector] = {}

    logger.info("")  # Empty line

    # Generate visualizations
    try:
        # 1. Radar chart
        create_radar_chart(
            detector_metrics,
            args.output_dir / 'radar_6detectors.png'
        )

        # 2. F3 vs FP scatter
        create_f3_vs_fp_scatter(
            detector_metrics,
            args.output_dir / 'f3_vs_fp_scatter.png'
        )

        # 3. Heatmap
        create_heatmap_comparison(
            detector_metrics,
            args.output_dir / 'heatmap_metrics_comparison.png'
        )

        # 4. 3D trade-off
        create_3d_tradeoff(
            detector_metrics,
            args.output_dir / 'parameter_tradeoffs.png'
        )

        logger.info(f"\n✅ All visualizations generated successfully!")
        logger.info(f"   Output directory: {args.output_dir}")
        logger.info(f"   Generated 4 PNG files")

    except Exception as e:
        logger.error(f"Error generating visualizations: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
