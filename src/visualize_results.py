#!/usr/bin/env python3
"""
Visualize Grid Search Results for ECG Change Point Detection

Generates comprehensive visualizations including:
1. Precision-Recall scatter plots with temporal thresholds
2. Pareto fronts for multi-objective optimization
3. Parameter heatmaps
4. Score distribution comparisons
5. 3D trade-off surfaces
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def load_metrics(metrics_path):
    """Load metrics CSV and aggregate by parameters."""
    df = pd.read_csv(metrics_path)

    # Auto-detect parameter columns (detector-specific)
    # Common parameter patterns: delta, lambda_, alpha, ma_window, min_gap_samples,
    # drift_confidence, warning_confidence, etc.
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
def plot_pr_scatter(df, output_dir):
    """
    Precision-Recall scatter plot with multiple temporal thresholds.
    Each point is a parameter combination, colored by delta or ma_window.
    """
    # Select color variable: min_gap_samples if available, else ma_window, else delta
    if 'min_gap_samples' in df.columns:
        color_var = 'min_gap_samples'
        color_label = 'Min Gap (samples)'
    elif 'ma_window' in df.columns:
        color_var = 'ma_window'
        color_label = 'MA Window'
    elif 'delta' in df.columns:
        color_var = 'delta'
        color_label = 'Delta'
    else:
        color_var = 'f3_weighted_mean'
        color_label = 'F3-weighted Score'

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Recall@4s vs Precision@4s
    ax1 = axes[0]
    scatter1 = ax1.scatter(
        df['recall_4s_mean'],
        df['precision_4s_mean'],
        c=df[color_var],
        s=50,
        alpha=0.6,
        cmap='viridis',
        edgecolors='black',
        linewidth=0.5
    )
    ax1.set_xlabel('Recall @ 4s', fontsize=12)
    ax1.set_ylabel('Precision @ 4s', fontsize=12)
    ax1.set_title('Precision-Recall Trade-off (4s window)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label(color_label, fontsize=10)

    # Add best point
    best_idx = df['f3_weighted_mean'].idxmax()
    ax1.scatter(
        df.loc[best_idx, 'recall_4s_mean'],
        df.loc[best_idx, 'precision_4s_mean'],
        s=200,
        marker='*',
        c='red',
        edgecolors='black',
        linewidth=2,
        label='Best F3',
        zorder=10
    )
    ax1.legend()

    # Plot 2: Recall@10s vs Precision@10s
    ax2 = axes[1]
    scatter2 = ax2.scatter(
        df['recall_10s_mean'],
        df['precision_10s_mean'],
        c=df[color_var],
        s=50,
        alpha=0.6,
        cmap='viridis',
        edgecolors='black',
        linewidth=0.5
    )
    ax2.set_xlabel('Recall @ 10s', fontsize=12)
    ax2.set_ylabel('Precision @ 10s', fontsize=12)
    ax2.set_title('Precision-Recall Trade-off (10s window)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label(color_label, fontsize=10)

    # Add best point
    ax2.scatter(
        df.loc[best_idx, 'recall_10s_mean'],
        df.loc[best_idx, 'precision_10s_mean'],
        s=200,
        marker='*',
        c='red',
        edgecolors='black',
        linewidth=2,
        label='Best F3',
        zorder=10
    )
    ax2.legend()

    plt.tight_layout()
    output_path = output_dir / 'pr_scatter_plots.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_pareto_front(df, output_dir):
    """
    Pareto front showing Recall@10s vs FP/min trade-off.
    Identifies non-dominated solutions.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Extract objectives (maximize recall, minimize FP/min)
    recall = df['recall_10s_mean'].values
    fp_rate = df['fp_per_min_mean'].values
    f3_scores = df['f3_weighted_mean'].values

    # Find Pareto front (simple approach: non-dominated solutions)
    pareto_mask = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                # j dominates i if: higher recall AND lower FP
                if recall[j] >= recall[i] and fp_rate[j] <= fp_rate[i]:
                    if recall[j] > recall[i] or fp_rate[j] < fp_rate[i]:
                        pareto_mask[i] = False
                        break

    # Plot all points
    scatter = ax.scatter(
        recall[~pareto_mask],
        fp_rate[~pareto_mask],
        c=f3_scores[~pareto_mask],
        s=30,
        alpha=0.4,
        cmap='viridis',
        label='Dominated solutions'
    )

    # Plot Pareto front
    pareto_recall = recall[pareto_mask]
    pareto_fp = fp_rate[pareto_mask]
    pareto_f3 = f3_scores[pareto_mask]

    # Sort for line connection
    sorted_idx = np.argsort(pareto_recall)

    ax.scatter(
        pareto_recall,
        pareto_fp,
        c=pareto_f3,
        s=100,
        alpha=0.9,
        cmap='viridis',
        edgecolors='red',
        linewidth=2,
        label='Pareto front',
        zorder=10
    )

    ax.plot(
        pareto_recall[sorted_idx],
        pareto_fp[sorted_idx],
        'r--',
        alpha=0.5,
        linewidth=2
    )

    ax.set_xlabel('Recall @ 10s (↑ better)', fontsize=12)
    ax.set_ylabel('False Positives per minute (↓ better)', fontsize=12)
    ax.set_title('Pareto Front: Recall vs False Positive Rate', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('F3-weighted Score', fontsize=10)

    # Annotate number of Pareto optimal solutions
    ax.text(
        0.02, 0.98,
        f'Pareto optimal: {pareto_mask.sum()} / {len(df)}',
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )

    plt.tight_layout()
    output_path = output_dir / 'pareto_front.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_parameter_heatmaps(df, output_dir):
    """
    Heatmaps showing how parameters affect different metrics.
    Creates heatmaps based on available parameters.
    """
    # Identify parameter columns
    param_cols = [col for col in df.columns if col.replace('_mean', '').replace('_std', '') in
                  ['delta', 'lambda_', 'alpha', 'ma_window', 'min_gap_samples',
                   'drift_confidence', 'warning_confidence', 'ks_alpha', 'window_size',
                   'regime_threshold', 'regime_landmark']]

    # Filter to just the base parameter names (without _mean/_std)
    param_cols = [col for col in param_cols if not col.endswith('_mean') and not col.endswith('_std')]

    # Filter out parameters with only 1 unique value (no variation)
    param_cols = [col for col in param_cols if df[col].nunique() > 1]

    if len(param_cols) < 2:
        print(f"Warning: Need at least 2 parameters with variation for heatmaps, found {len(param_cols)}. Skipping heatmaps.")
        return

    # Try to find a grouping parameter (prefer min_gap_samples if it has variation, then others)
    group_param = None
    if 'min_gap_samples' in param_cols and df['min_gap_samples'].nunique() > 1:
        group_param = 'min_gap_samples'
    elif len(param_cols) > 2:
        # Use the parameter with fewest unique values for grouping (but more than 1)
        group_param = min(param_cols, key=lambda p: df[p].nunique())

    # Get top values for grouping parameter
    if group_param:
        top_gaps = df[group_param].value_counts().head(3).index.sort_values()
        heatmap_params = [p for p in param_cols if p != group_param][:2]  # Use first 2 remaining
    else:
        top_gaps = [None]  # No grouping, single heatmap
        heatmap_params = param_cols[:2]

    metrics = [
        ('f3_weighted_mean', 'F3-Weighted Score'),
        ('nab_score_standard_mean', 'NAB Standard Score'),
        ('recall_10s_mean', 'Recall @ 10s'),
        ('fp_per_min_mean', 'FP per minute')
    ]

    for metric_col, metric_name in metrics:
        if metric_col not in df.columns:
            continue

        fig, axes = plt.subplots(1, len(top_gaps), figsize=(5 * len(top_gaps), 4))
        if len(top_gaps) == 1:
            axes = [axes]

        for idx, gap in enumerate(top_gaps):
            if gap is not None:
                subset = df[df[group_param] == gap]
                title_suffix = f'{group_param} = {gap}'
            else:
                subset = df
                title_suffix = ''

            # Pivot for heatmap using detected parameters
            if len(heatmap_params) >= 2:
                pivot = subset.pivot_table(
                    values=metric_col,
                    index=heatmap_params[0],
                    columns=heatmap_params[1],
                    aggfunc='mean'
                )
            else:
                continue  # Skip if not enough parameters

            ax = axes[idx]
            sns.heatmap(
                pivot,
                annot=True,
                fmt='.3f',
                cmap='RdYlGn' if 'fp_per_min' not in metric_col else 'RdYlGn_r',
                ax=ax,
                cbar_kws={'label': metric_name}
            )
            ax.set_title(title_suffix, fontsize=12, fontweight='bold')
            ax.set_xlabel(heatmap_params[1].replace('_', ' ').title(), fontsize=10)
            ax.set_ylabel(heatmap_params[0].replace('_', ' ').title(), fontsize=10)

        plt.suptitle(f'{metric_name} by Parameters', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        safe_name = metric_col.replace('_mean', '').replace('_', '-')
        output_path = output_dir / f'heatmap_{safe_name}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
        plt.close()


def plot_score_distributions(df, output_dir):
    """
    Box plots comparing distributions of different scoring metrics.
    Shows variability and central tendencies.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: F-scores
    ax1 = axes[0, 0]
    f_scores = df[['f1_weighted_mean', 'f1_classic_mean', 'f3_weighted_mean', 'f3_classic_mean']]
    f_scores.columns = ['F1 Weighted', 'F1 Classic', 'F3 Weighted', 'F3 Classic']
    f_scores.boxplot(ax=ax1)
    ax1.set_ylabel('Score', fontsize=11)
    ax1.set_title('F-Score Distributions', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Plot 2: NAB scores
    ax2 = axes[0, 1]
    nab_cols = ['nab_score_standard_mean', 'nab_score_low_fp_mean', 'nab_score_low_fn_mean']
    if all(col in df.columns for col in nab_cols):
        nab_scores = df[nab_cols]
        nab_scores.columns = ['Standard', 'Low FP', 'Low FN']
        nab_scores.boxplot(ax=ax2)
        ax2.set_ylabel('NAB Score', fontsize=11)
        ax2.set_title('NAB Score Distributions', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'NAB scores not available', ha='center', va='center')
        ax2.set_title('NAB Score Distributions', fontsize=12, fontweight='bold')

    # Plot 3: Recall at different thresholds
    ax3 = axes[1, 0]
    recall_scores = df[['recall_4s_mean', 'recall_10s_mean']]
    recall_scores.columns = ['Recall @ 4s', 'Recall @ 10s']
    recall_scores.boxplot(ax=ax3)
    ax3.set_ylabel('Recall', fontsize=11)
    ax3.set_title('Recall Distributions (Temporal Thresholds)', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0, 1])

    # Plot 4: FP rate and EDD
    ax4 = axes[1, 1]
    ax4_twin = ax4.twinx()

    bp1 = ax4.boxplot([df['fp_per_min_mean']], positions=[1], widths=0.6,
                       patch_artist=True, boxprops=dict(facecolor='lightblue'))
    bp2 = ax4_twin.boxplot([df['edd_median_s_mean']], positions=[2], widths=0.6,
                            patch_artist=True, boxprops=dict(facecolor='lightcoral'))

    ax4.set_ylabel('FP per minute', fontsize=11, color='blue')
    ax4_twin.set_ylabel('EDD (seconds)', fontsize=11, color='red')
    ax4.set_xticks([1, 2])
    ax4.set_xticklabels(['FP/min', 'EDD'])
    ax4.set_title('False Positive Rate and Detection Delay', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='y', labelcolor='blue')
    ax4_twin.tick_params(axis='y', labelcolor='red')

    plt.tight_layout()
    output_path = output_dir / 'score_distributions.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_3d_tradeoff(df, output_dir):
    """
    3D scatter plot showing Recall vs FP/min vs EDD.
    Points colored by F3 score.
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    x = df['recall_10s_mean'].values
    y = df['fp_per_min_mean'].values
    z = df['edd_median_s_mean'].values
    colors = df['f3_weighted_mean'].values

    scatter = ax.scatter(
        x, y, z,
        c=colors,
        s=50,
        alpha=0.6,
        cmap='viridis',
        edgecolors='black',
        linewidth=0.5
    )

    ax.set_xlabel('Recall @ 10s (↑)', fontsize=11, labelpad=10)
    ax.set_ylabel('FP per min (↓)', fontsize=11, labelpad=10)
    ax.set_zlabel('EDD median (↓)', fontsize=11, labelpad=10)
    ax.set_title('3D Trade-off Surface: Recall vs FP vs Delay', fontsize=14, fontweight='bold', pad=20)

    cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label('F3-weighted Score', fontsize=10)

    # Mark best point
    best_idx = df['f3_weighted_mean'].idxmax()
    ax.scatter(
        [x[best_idx]], [y[best_idx]], [z[best_idx]],
        s=300,
        marker='*',
        c='red',
        edgecolors='black',
        linewidth=2,
        label='Best F3'
    )
    ax.legend()

    plt.tight_layout()
    output_path = output_dir / '3d_tradeoff.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_parameter_sensitivity(df, output_dir):
    """
    Line plots showing how each parameter affects key metrics.
    """
    # Auto-detect parameters
    param_cols = [col for col in df.columns if col in
                  ['delta', 'lambda_', 'alpha', 'ma_window', 'min_gap_samples',
                   'drift_confidence', 'warning_confidence', 'ks_alpha', 'window_size',
                   'stat_size', 'lambda_option']]

    if not param_cols:
        print("Warning: No parameters found for sensitivity analysis. Skipping.")
        return

    # Limit to 6 parameters max (2 rows × 3 cols)
    params = param_cols[:6]
    n_params = len(params)
    n_cols = min(3, n_params)
    n_rows = (n_params + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.5 * n_cols, 5 * n_rows))
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1 or n_cols == 1:
        axes = axes.reshape(n_rows, n_cols)
    metrics = [
        ('f3_weighted_mean', 'F3-Weighted'),
        ('recall_10s_mean', 'Recall @ 10s')
    ]

    plot_idx = 0
    for metric_col, metric_name in metrics:
        for param in params:
            if plot_idx >= n_rows * n_cols:
                break
            row_idx = plot_idx // n_cols
            col_idx = plot_idx % n_cols
            ax = axes[row_idx, col_idx]
            plot_idx += 1

            # Group by parameter and calculate mean/std
            grouped = df.groupby(param)[metric_col].agg(['mean', 'std']).reset_index()

            ax.plot(grouped[param], grouped['mean'], marker='o', linewidth=2, markersize=6)
            ax.fill_between(
                grouped[param],
                grouped['mean'] - grouped['std'],
                grouped['mean'] + grouped['std'],
                alpha=0.3
            )

            param_label = param.replace('_', ' ').title()
            ax.set_xlabel(param_label, fontsize=10)
            ax.set_ylabel(metric_name, fontsize=10)
            ax.set_title(f'{metric_name} vs {param_label}', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)

            # Log scale for certain parameters
            if param in ['ma_window', 'window_size', 'stat_size']:
                ax.set_xscale('log')

    # Hide unused subplots
    for idx in range(plot_idx, n_rows * n_cols):
        row_idx = idx // n_cols
        col_idx = idx % n_cols
        axes[row_idx, col_idx].set_visible(False)

    plt.tight_layout()
    output_path = output_dir / 'parameter_sensitivity.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Generate comprehensive visualizations from grid search results'
    )
    parser.add_argument(
        '--metrics',
        default='results/metrics_comprehensive_with_nab.csv',
        help='Path to metrics CSV file'
    )
    parser.add_argument(
        '--output-dir',
        default='results/visualizations',
        help='Directory to save visualization plots'
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading metrics from: {args.metrics}")
    df = load_metrics(args.metrics)
    print(f"Loaded {len(df)} parameter combinations\n")

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'

    print("Generating visualizations...")
    print("-" * 60)

    # Generate all plots
    plot_pr_scatter(df, output_dir)
    plot_pareto_front(df, output_dir)
    plot_parameter_heatmaps(df, output_dir)
    plot_score_distributions(df, output_dir)
    plot_3d_tradeoff(df, output_dir)
    plot_parameter_sensitivity(df, output_dir)

    print("-" * 60)
    print(f"\n✅ All visualizations saved to: {output_dir}/")
    print("\nGenerated plots:")
    print("  1. pr_scatter_plots.png - Precision-Recall trade-offs")
    print("  2. pareto_front.png - Non-dominated solutions")
    print("  3. heatmap_*.png - Parameter sensitivity heatmaps")
    print("  4. score_distributions.png - Metric distributions")
    print("  5. 3d_tradeoff.png - 3D trade-off surface")
    print("  6. parameter_sensitivity.png - Parameter effect on metrics")


if __name__ == '__main__':
    main()
