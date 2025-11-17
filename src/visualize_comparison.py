#!/usr/bin/env python3
"""
Visualize comparison between two detectors.

Creates comparative plots for detector performance.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import json


def load_detector_data(detector_name, results_dir):
    """Load metrics and report for a detector."""
    detector_dir = Path(results_dir) / detector_name

    # Load metrics
    metrics_path = detector_dir / "metrics_comprehensive_with_nab.csv"
    metrics_df = pd.read_csv(metrics_path)

    # Load report
    report_path = detector_dir / "final_report_with_nab.json"
    with open(report_path, 'r') as f:
        report = json.load(f)

    return metrics_df, report


def plot_radar_comparison(detector1_name, detector1_best, detector2_name, detector2_best, output_path):
    """Create radar chart comparing best configurations."""

    # Define metrics for radar chart (normalized 0-1, higher is better)
    metrics = {
        'F3*': ('f3_weighted_mean', False),  # False = don't invert
        'Recall@10s': ('recall_10s_mean', False),
        'Precision@10s': ('precision_10s_mean', False),
        'NAB Std': ('nab_score_standard_mean', True),  # True = invert (less negative is better)
        'Low Latency': ('edd_median_s_mean', True),  # Invert (lower is better)
        'Low FP Rate': ('fp_per_min_mean', True),  # Invert (lower is better)
    }

    categories = list(metrics.keys())
    N = len(categories)

    # Get values
    values1 = []
    values2 = []

    for metric_key, (col_name, invert) in metrics.items():
        val1 = detector1_best.get(col_name, 0)
        val2 = detector2_best.get(col_name, 0)

        if invert:
            # For metrics where lower is better, invert
            if col_name == 'nab_score_standard_mean':
                # NAB: convert to positive scale (closer to 0 is better)
                val1 = max(0, 10 + val1) / 10  # Normalize around [-10, 0]
                val2 = max(0, 10 + val2) / 10
            else:
                # For EDD and FP: normalize and invert
                max_val = max(val1, val2) if max(val1, val2) > 0 else 1
                val1 = 1 - (val1 / max_val)
                val2 = 1 - (val2 / max_val)

        values1.append(val1)
        values2.append(val2)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values1 += values1[:1]  # Complete the circle
    values2 += values2[:1]
    angles += angles[:1]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

    ax.plot(angles, values1, 'o-', linewidth=2, label=detector1_name.upper(), color='#2E86AB')
    ax.fill(angles, values1, alpha=0.25, color='#2E86AB')

    ax.plot(angles, values2, 'o-', linewidth=2, label=detector2_name.upper(), color='#A23B72')
    ax.fill(angles, values2, alpha=0.25, color='#A23B72')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=11)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0.25', '0.5', '0.75', '1.0'], size=9)
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    plt.title(f'Detector Performance Comparison\n{detector1_name.upper()} vs {detector2_name.upper()}',
              size=14, weight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_metric_bars(detector1_name, detector1_best, detector2_name, detector2_best, output_path):
    """Create bar chart comparing key metrics."""

    metrics = {
        'F3* Score': 'f3_weighted_mean',
        'F1* Score': 'f1_weighted_mean',
        'Recall@10s': 'recall_10s_mean',
        'Precision@10s': 'precision_10s_mean',
        'NAB Standard': 'nab_score_standard_mean',
        'FP/min': 'fp_per_min_mean',
        'EDD (s)': 'edd_median_s_mean',
    }

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()

    for idx, (metric_name, col_name) in enumerate(metrics.items()):
        ax = axes[idx]

        val1 = detector1_best.get(col_name, 0)
        val2 = detector2_best.get(col_name, 0)

        bars = ax.bar([detector1_name.upper(), detector2_name.upper()],
                      [val1, val2],
                      color=['#2E86AB', '#A23B72'])

        ax.set_ylabel(metric_name, fontsize=10, weight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=9)

        # Highlight winner
        if val1 > val2 if 'NAB' not in metric_name and 'FP' not in metric_name and 'EDD' not in metric_name else val1 < val2:
            bars[0].set_edgecolor('gold')
            bars[0].set_linewidth(3)
        else:
            bars[1].set_edgecolor('gold')
            bars[1].set_linewidth(3)

    # Hide extra subplot
    axes[-1].axis('off')

    plt.suptitle(f'Detector Metrics Comparison: {detector1_name.upper()} vs {detector2_name.upper()}',
                fontsize=16, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_distribution_comparison(detector1_name, metrics1_df, detector2_name, metrics2_df, output_path):
    """Create violin plots comparing metric distributions."""

    key_metrics = ['f3_weighted', 'recall_10s', 'precision_10s', 'fp_per_min']
    metric_labels = ['F3* Score', 'Recall@10s', 'Precision@10s', 'FP/min']

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    for idx, (metric, label) in enumerate(zip(key_metrics, metric_labels)):
        ax = axes[idx]

        # Prepare data
        data = []
        labels = []

        if metric in metrics1_df.columns:
            data.append(metrics1_df[metric].dropna())
            labels.append(detector1_name.upper())

        if metric in metrics2_df.columns:
            data.append(metrics2_df[metric].dropna())
            labels.append(detector2_name.upper())

        # Create violin plot
        parts = ax.violinplot(data, positions=range(len(data)),
                             showmeans=True, showmedians=True)

        # Color violins
        colors = ['#2E86AB', '#A23B72']
        for pc, color in zip(parts['bodies'], colors[:len(data)]):
            pc.set_facecolor(color)
            pc.set_alpha(0.6)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel(label, fontsize=11, weight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.suptitle(f'Metric Distribution Comparison: {detector1_name.upper()} vs {detector2_name.upper()}',
                fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Visualize detector comparison')
    parser.add_argument('--detector1', required=True, help='First detector name')
    parser.add_argument('--detector2', required=True, help='Second detector name')
    parser.add_argument('--results-dir', default='results', help='Results directory')
    parser.add_argument('--output-dir', default='results/comparisons', help='Output directory')

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading data for {args.detector1} and {args.detector2}...")

    # Load data
    metrics1_df, report1 = load_detector_data(args.detector1, args.results_dir)
    metrics2_df, report2 = load_detector_data(args.detector2, args.results_dir)

    # Extract best configs (use f3_weighted as primary metric)
    best1 = report1['best_parameters']['f3_weighted']
    best2 = report2['best_parameters']['f3_weighted']

    print("\nGenerating comparative visualizations...")

    # 1. Radar chart
    radar_path = output_dir / f"{args.detector1}_vs_{args.detector2}_radar.png"
    plot_radar_comparison(args.detector1, best1, args.detector2, best2, radar_path)

    # 2. Bar charts
    bars_path = output_dir / f"{args.detector1}_vs_{args.detector2}_bars.png"
    plot_metric_bars(args.detector1, best1, args.detector2, best2, bars_path)

    # 3. Distribution comparison
    dist_path = output_dir / f"{args.detector1}_vs_{args.detector2}_distributions.png"
    plot_distribution_comparison(args.detector1, metrics1_df, args.detector2, metrics2_df, dist_path)

    print(f"\n✅ All visualizations saved to: {output_dir}")


if __name__ == '__main__':
    main()
