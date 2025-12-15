#!/usr/bin/env python3
"""
visualize_cross_dataset_summary.py
Gera 4 visualizações de análise cross-dataset (opções 1, 2, 3 e matriz de decisão).

Usage:
    python -m src.visualize_cross_dataset_summary --output-dir results/comparisons/cross_dataset
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cores consistentes por detector
DETECTOR_COLORS = {
    'adwin': '#1f77b4',          # Azul
    'page_hinkley': '#2ca02c',   # Verde
    'kswin': '#ff7f0e',          # Laranja
    'hddm_a': '#d62728',         # Vermelho
    'hddm_w': '#9467bd',         # Roxo
    'floss': '#7f7f7f'           # Cinza
}

DETECTOR_ORDER = ['adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w', 'floss']


def load_option1_data(base_path: Path) -> pd.DataFrame:
    """Carrega dados de ceiling analysis (Option 1)."""
    csv_path = base_path / "cross_dataset_generalization_option1.csv"
    if not csv_path.exists():
        logger.error(f"Option1 CSV not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    logger.info(f"✓ Loaded Option1 data: {len(df)} detectors")
    return df


def load_option2_data(base_path: Path) -> pd.DataFrame:
    """Carrega dados de portability (Option 2)."""
    csv_path = base_path / "parameter_portability_option2.csv"
    if not csv_path.exists():
        logger.error(f"Option2 CSV not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    logger.info(f"✓ Loaded Option2 data: {len(df)} transfer scenarios")

    # Calcular média de transferabilidade por detector
    summary = df.groupby('detector').agg({
        'transferability_ratio': ['mean', 'std'],
        'performance_drop_pct': ['mean', 'std']
    }).reset_index()

    summary.columns = ['detector', 'avg_transferability', 'std_transferability',
                       'avg_drop_pct', 'std_drop_pct']

    logger.info(f"✓ Computed transferability summary for {len(summary)} detectors")
    return summary


def load_option3_data(base_path: Path) -> pd.DataFrame:
    """Carrega dados de unified score (Option 3)."""
    csv_path = base_path / "unified_robustness_option3.csv"
    if not csv_path.exists():
        logger.error(f"Option3 CSV not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    logger.info(f"✓ Loaded Option3 data: {len(df)} detectors")
    return df


def create_option1_ceiling_chart(df: pd.DataFrame, output_path: Path):
    """
    Gera gráfico de barras com error bars: F3-weighted ceiling por detector.
    """
    logger.info("Creating Option1 ceiling analysis chart...")

    if df.empty:
        logger.error("Option1 dataframe is empty, skipping chart")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    # Ordenar detectores
    df = df.set_index('detector').reindex(DETECTOR_ORDER).reset_index()

    # Criar gradient de cores (verde=bom, vermelho=fraco)
    f3_values = df['mean_cross_fold_f3'].values
    colors = plt.cm.RdYlGn((f3_values - f3_values.min()) / (f3_values.max() - f3_values.min()))

    # Plot bars com error bars
    bars = ax.bar(df['detector'], df['mean_cross_fold_f3'],
                   yerr=df['std_dev'], capsize=5, color=colors,
                   edgecolor='black', linewidth=1.2, alpha=0.85)

    # Anotações: F3 value + CV%
    for i, (detector, row) in enumerate(df.iterrows()):
        f3_val = row['mean_cross_fold_f3']
        cv_pct = row['cv_percent']
        ax.text(i, f3_val + row['std_dev'] + 0.01,
                f"{f3_val:.3f}\nCV={cv_pct:.1f}%",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Detector', fontsize=12, fontweight='bold')
    ax.set_ylabel('F3-weighted Ceiling (mean ± std)', fontsize=12, fontweight='bold')
    ax.set_title('Option 1: Cross-Dataset Generalization Ceiling',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(df['mean_cross_fold_f3'] + df['std_dev']) * 1.15)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Option1 ceiling chart saved: {output_path}")


def create_option2_portability_heatmap(df: pd.DataFrame, output_path: Path):
    """
    Gera heatmap: rows=detectores, cols=transferability % (média).
    """
    logger.info("Creating Option2 portability heatmap...")

    if df.empty:
        logger.error("Option2 dataframe is empty, skipping heatmap")
        return

    fig, ax = plt.subplots(figsize=(8, 6))

    # Preparar dados: converter ratio para percentagem
    df = df.set_index('detector').reindex(DETECTOR_ORDER).reset_index()
    df['transferability_pct'] = df['avg_transferability'] * 100

    # Criar heatmap (1 coluna apenas)
    heatmap_data = df[['transferability_pct']].T
    heatmap_data.columns = df['detector']

    # Plot heatmap
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn',
                cbar_kws={'label': 'Transferability %'},
                vmin=45, vmax=100, linewidths=1, linecolor='black',
                ax=ax, annot_kws={'fontsize': 11, 'fontweight': 'bold'})

    ax.set_xlabel('Detector', fontsize=12, fontweight='bold')
    ax.set_ylabel('')
    ax.set_title('Option 2: Parameter Portability (Transferability %)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_yticklabels(['Transferability'], rotation=0)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Option2 portability heatmap saved: {output_path}")


def create_option3_unified_score_chart(df: pd.DataFrame, output_path: Path):
    """
    Gera gráfico de barras: X=detectores (ordenado por unified score), Y=score.
    """
    logger.info("Creating Option3 unified score ranking chart...")

    if df.empty:
        logger.error("Option3 dataframe is empty, skipping chart")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    # Ordenar por unified_score decrescente
    df = df.sort_values('unified_score', ascending=False).reset_index(drop=True)

    # Criar gradient de cores (verde=bom, vermelho=fraco)
    scores = df['unified_score'].values
    colors = plt.cm.RdYlGn((scores - scores.min()) / (scores.max() - scores.min()))

    # Plot bars
    bars = ax.bar(df['detector'], df['unified_score'],
                   color=colors, edgecolor='black', linewidth=1.2, alpha=0.85)

    # Anotações: score + ranking
    for i, (idx, row) in enumerate(df.iterrows()):
        score_val = row['unified_score']
        rank = row['rank']
        ax.text(i, score_val + 0.005,
                f"{score_val:.4f}\n#{int(rank)}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('Detector (Ranked by Unified Score)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Unified Robustness Score', fontsize=12, fontweight='bold')
    ax.set_title('Option 3: Unified Robustness Score Ranking',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(scores.min() * 0.98, scores.max() * 1.02)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Option3 unified score chart saved: {output_path}")


def create_production_decision_matrix(option1_df: pd.DataFrame,
                                       option2_df: pd.DataFrame,
                                       option3_df: pd.DataFrame,
                                       output_path: Path):
    """
    Gera bubble chart: X=ceiling F3, Y=transferability%, size=unified score.
    Quadrantes anotados com recomendações.
    """
    logger.info("Creating production decision matrix...")

    if option1_df.empty or option2_df.empty or option3_df.empty:
        logger.error("One or more dataframes empty, skipping decision matrix")
        return

    # Merge datasets
    merged = option1_df[['detector', 'mean_cross_fold_f3']].copy()
    merged = merged.merge(option2_df[['detector', 'avg_transferability']], on='detector')
    merged = merged.merge(option3_df[['detector', 'unified_score']], on='detector')

    # Converter para %
    merged['transferability_pct'] = merged['avg_transferability'] * 100

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot bubbles
    for _, row in merged.iterrows():
        detector = row['detector']
        x = row['mean_cross_fold_f3']
        y = row['transferability_pct']
        size = row['unified_score'] * 1000  # Scale for visibility

        ax.scatter(x, y, s=size, color=DETECTOR_COLORS.get(detector, 'gray'),
                   alpha=0.6, edgecolors='black', linewidth=2,
                   label=detector)

        # Anotação: nome detector
        ax.text(x, y, detector.upper(), ha='center', va='center',
                fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))

    # Linhas de quadrantes (mediana)
    median_f3 = merged['mean_cross_fold_f3'].median()
    median_trans = merged['transferability_pct'].median()

    ax.axvline(median_f3, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.axhline(median_trans, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

    # Anotações de quadrantes
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Top-left: Max Performance
    ax.text(xlim[0] + (median_f3 - xlim[0]) * 0.5,
            median_trans + (ylim[1] - median_trans) * 0.9,
            "Low Performance\nHigh Portability", ha='center', va='top',
            fontsize=11, fontweight='bold', color='orange',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    # Top-right: Portable & Good
    ax.text(median_f3 + (xlim[1] - median_f3) * 0.5,
            median_trans + (ylim[1] - median_trans) * 0.9,
            "High Performance\nHigh Portability\n★ IDEAL ★", ha='center', va='top',
            fontsize=11, fontweight='bold', color='green',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

    # Bottom-left: Poor
    ax.text(xlim[0] + (median_f3 - xlim[0]) * 0.5,
            ylim[0] + (median_trans - ylim[0]) * 0.1,
            "Low Performance\nLow Portability\n⚠ POOR ⚠", ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='darkred',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8))

    # Bottom-right: Overkill
    ax.text(median_f3 + (xlim[1] - median_f3) * 0.5,
            ylim[0] + (median_trans - ylim[0]) * 0.1,
            "High Performance\nLow Portability", ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='blue',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

    ax.set_xlabel('Ceiling F3-weighted (mean)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Transferability %', fontsize=12, fontweight='bold')
    ax.set_title('Production Decision Matrix\n(Bubble size = Unified Score)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(alpha=0.3, linestyle='--')

    # Legend (sem duplicados)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(),
              loc='upper left', fontsize=10, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"✓ Production decision matrix saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate cross-dataset summary visualizations (4 PNG files)"
    )
    parser.add_argument(
        '--results-base',
        type=str,
        default='results/cross_dataset_analysis',
        help='Base directory with cross-dataset analysis CSVs'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results/comparisons/cross_dataset',
        help='Output directory for PNG files'
    )

    args = parser.parse_args()

    results_base = Path(args.results_base)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting cross-dataset summary visualizations")
    logger.info(f"Results base: {results_base}")
    logger.info(f"Output directory: {output_dir}")

    # Carregar dados
    option1_df = load_option1_data(results_base)
    option2_df = load_option2_data(results_base)
    option3_df = load_option3_data(results_base)

    if option1_df.empty or option2_df.empty or option3_df.empty:
        logger.error("❌ One or more CSV files missing, cannot proceed")
        sys.exit(1)

    logger.info("")

    # Gerar visualizações
    create_option1_ceiling_chart(
        option1_df,
        output_dir / "option1_ceiling_analysis.png"
    )

    create_option2_portability_heatmap(
        option2_df,
        output_dir / "option2_portability_heatmap.png"
    )

    create_option3_unified_score_chart(
        option3_df,
        output_dir / "option3_unified_score_ranking.png"
    )

    create_production_decision_matrix(
        option1_df, option2_df, option3_df,
        output_dir / "production_decision_matrix.png"
    )

    logger.info("")
    logger.info("✅ All cross-dataset visualizations generated successfully!")
    logger.info(f"   Output directory: {output_dir}")
    logger.info(f"   Generated 4 PNG files")


if __name__ == '__main__':
    main()
