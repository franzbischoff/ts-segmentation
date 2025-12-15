#!/usr/bin/env python3
"""
generate_comparison_reports.py
Wrapper que executa visualize_comparison_by_dataset.py + visualize_cross_dataset_summary.py
para todos os datasets e atualiza READMEs com timestamps.

Usage:
    python -m src.generate_comparison_reports \
        --datasets afib_paroxysmal malignantventricular vtachyarrhythmias \
        --output-base results/comparisons
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DETECTOR_LIST = ['adwin', 'page_hinkley', 'kswin', 'hddm_a', 'hddm_w', 'floss']


def run_command(cmd: List[str], description: str) -> bool:
    """
    Executa comando e retorna True se sucesso, False caso contrário.
    """
    logger.info(f"Running: {description}")
    logger.info(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed with exit code {e.returncode}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return False


def generate_by_dataset_visualizations(dataset: str, output_base: Path) -> bool:
    """
    Executa visualize_comparison_by_dataset.py para um dataset específico.
    """
    output_dir = output_base / "by_dataset" / dataset / "visualizations"

    cmd = [
        sys.executable, '-m', 'src.visualize_comparison_by_dataset',
        '--dataset', dataset,
        '--output-dir', str(output_dir)
    ]

    return run_command(cmd, f"By-dataset visualizations for {dataset}")


def generate_cross_dataset_visualizations(output_base: Path) -> bool:
    """
    Executa visualize_cross_dataset_summary.py.
    """
    output_dir = output_base / "cross_dataset"

    cmd = [
        sys.executable, '-m', 'src.visualize_cross_dataset_summary',
        '--output-dir', str(output_dir)
    ]

    return run_command(cmd, "Cross-dataset summary visualizations")


def update_by_dataset_readme(dataset: str, output_base: Path, success: bool):
    """
    Atualiza README do dataset com timestamp e status da última geração.
    """
    readme_path = output_base / "by_dataset" / dataset / "README.md"

    if not readme_path.exists():
        logger.warning(f"README not found: {readme_path}, skipping update")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ SUCCESS" if success else "❌ FAILED"

    # Ler conteúdo atual
    content = readme_path.read_text()

    # Procurar linha de última atualização
    update_marker = "**Last Updated:**"

    if update_marker in content:
        # Substituir linha existente
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if update_marker in line:
                lines[i] = f"{update_marker} {timestamp} ({status})"
                break
        content = '\n'.join(lines)
    else:
        # Adicionar linha no topo (após título)
        lines = content.split('\n')
        # Procurar primeira linha vazia após título
        insert_idx = 1
        for i, line in enumerate(lines):
            if i > 0 and line.strip() == '':
                insert_idx = i
                break
        lines.insert(insert_idx, f"\n{update_marker} {timestamp} ({status})\n")
        content = '\n'.join(lines)

    readme_path.write_text(content)
    logger.info(f"✓ Updated README: {readme_path}")


def update_cross_dataset_readme(output_base: Path, success: bool):
    """
    Atualiza README do cross-dataset com timestamp.
    """
    readme_path = output_base / "cross_dataset" / "README.md"

    if not readme_path.exists():
        logger.warning(f"README not found: {readme_path}, skipping update")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ SUCCESS" if success else "❌ FAILED"

    content = readme_path.read_text()
    update_marker = "**Last Updated:**"

    if update_marker in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if update_marker in line:
                lines[i] = f"{update_marker} {timestamp} ({status})"
                break
        content = '\n'.join(lines)
    else:
        lines = content.split('\n')
        insert_idx = 1
        for i, line in enumerate(lines):
            if i > 0 and line.strip() == '':
                insert_idx = i
                break
        lines.insert(insert_idx, f"\n{update_marker} {timestamp} ({status})\n")
        content = '\n'.join(lines)

    readme_path.write_text(content)
    logger.info(f"✓ Updated README: {readme_path}")


def print_summary(results: dict):
    """
    Imprime sumário final com estatísticas de sucesso/falha.
    """
    logger.info("")
    logger.info("=" * 80)
    logger.info("EXECUTION SUMMARY")
    logger.info("=" * 80)

    total = len(results)
    successes = sum(1 for v in results.values() if v)
    failures = total - successes

    logger.info(f"Total tasks: {total}")
    logger.info(f"✓ Successes: {successes}")
    logger.info(f"✗ Failures: {failures}")
    logger.info("")

    for task, success in results.items():
        status = "✅" if success else "❌"
        logger.info(f"  {status} {task}")

    logger.info("=" * 80)

    if failures > 0:
        logger.warning(f"⚠️  {failures} task(s) failed, review logs above")
        return False
    else:
        logger.info("✅ All tasks completed successfully!")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate all comparison visualizations (by-dataset + cross-dataset)"
    )
    parser.add_argument(
        '--datasets',
        nargs='+',
        default=['afib_paroxysmal', 'malignantventricular', 'vtachyarrhythmias'],
        help='List of datasets to process'
    )
    parser.add_argument(
        '--output-base',
        type=str,
        default='results/comparisons',
        help='Base output directory'
    )
    parser.add_argument(
        '--skip-by-dataset',
        action='store_true',
        help='Skip by-dataset visualizations (only do cross-dataset)'
    )
    parser.add_argument(
        '--skip-cross-dataset',
        action='store_true',
        help='Skip cross-dataset visualizations (only do by-dataset)'
    )

    args = parser.parse_args()

    output_base = Path(args.output_base)
    results = {}

    logger.info("=" * 80)
    logger.info("COMPARISON REPORTS GENERATION - PHASE 2")
    logger.info("=" * 80)
    logger.info(f"Datasets: {', '.join(args.datasets)}")
    logger.info(f"Output base: {output_base}")
    logger.info(f"Skip by-dataset: {args.skip_by_dataset}")
    logger.info(f"Skip cross-dataset: {args.skip_cross_dataset}")
    logger.info("=" * 80)
    logger.info("")

    # 1. By-dataset visualizations
    if not args.skip_by_dataset:
        for dataset in args.datasets:
            logger.info(f"Processing dataset: {dataset}")
            logger.info("-" * 80)

            success = generate_by_dataset_visualizations(dataset, output_base)
            results[f"by_dataset_{dataset}"] = success

            # Atualizar README
            update_by_dataset_readme(dataset, output_base, success)

            logger.info("")

    # 2. Cross-dataset visualizations
    if not args.skip_cross_dataset:
        logger.info("Processing cross-dataset analysis")
        logger.info("-" * 80)

        success = generate_cross_dataset_visualizations(output_base)
        results["cross_dataset"] = success

        # Atualizar README
        update_cross_dataset_readme(output_base, success)

        logger.info("")

    # 3. Print summary
    all_success = print_summary(results)

    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
