#!/usr/bin/env python3
"""
Exhaustive Grid Search para detector ADWIN baseline.
Similar à abordagem R: testa todas as combinações possíveis em cada ficheiro,
depois encontra parâmetros globalmente ótimos.
"""

import argparse
import itertools
import json
import time
from pathlib import Path
from typing import Dict, List, Any

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.streaming_detector import run_stream_on_dataframe
from src.data_loader import load_dataset


def create_param_grid() -> Dict[str, List[Any]]:
    """Cria grid exhaustivo de parâmetros similiar ao approach R."""
    return {
        'delta': [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1],  # 11 valores
        'ma_window': [10, 25, 50, 75, 100, 150, 200, 250, 300],                          # 9 valores específicos
        'min_gap_samples': list(range(1000, 6000, 1000)),                               # 5 valores (1000,2000,3000,4000,5000)
    }
    # Total: 11 × 9 × 5 = 495 combinações


def evaluate_single_record(record_data: pd.DataFrame, params: Dict[str, Any],
                          sample_rate: int = 250, tolerance: int = 500) -> Dict[str, Any]:
    """Executa detector em um único record com parâmetros específicos."""
    start_time = time.time()

    try:
        # Configurar parâmetros do detector
        detector_params = {'delta': params['delta']}

        # Executar detecção usando a função existente
        events, metrics, detector_name = run_stream_on_dataframe(
            df=record_data,
            detector_name='adwin',
            sample_rate=sample_rate,
            tolerance=tolerance,
            detector_params=detector_params,
            ma_window=params['ma_window'],
            use_derivative=False,
            min_gap_samples=params['min_gap_samples']
        )

        # Calculate comprehensive metrics using new evaluation function
        from src.evaluation import calculate_comprehensive_metrics

        # Extract GT and detection timestamps
        gt_indices = record_data.index[record_data['regime_change'] == 1].tolist()
        gt_times = [idx / sample_rate for idx in gt_indices]
        det_times = [event.time_seconds for event in events]
        duration_seconds = len(record_data) / sample_rate

        # Calculate all comprehensive metrics
        comprehensive_metrics = calculate_comprehensive_metrics(
            gt=gt_times,
            det=det_times,
            tau=10.0,      # 10s acceptance window
            plateau=4.0,   # 4s optimal window
            duration=duration_seconds
        )

        result = {
            **params,
            # All comprehensive metrics
            **comprehensive_metrics,
            # Execution info
            'duration': time.time() - start_time,
            'n_detections': len(events),
            'n_ground_truth': len(gt_times)
        }

        return result

    except Exception as e:
        return {
            **params,
            'error': str(e),
            'duration': time.time() - start_time,
            'precision': 0.0,
            'recall': 0.0,
            'f1': 0.0
        }
def process_single_file_all_params(record_id: str, record_data: pd.DataFrame,
                                  param_combinations: List[Dict[str, Any]],
                                  sample_rate: int = 250, max_samples: int = None) -> List[Dict[str, Any]]:
    """Processa um ficheiro com todas as combinações de parâmetros."""

    # Limitar samples para teste rápido
    if max_samples and len(record_data) > max_samples:
        record_data = record_data.head(max_samples).copy()
        print(f"  {record_id}: Limited to {max_samples} samples for testing")

    print(f"Processing {record_id}: {len(record_data)} samples, {len(param_combinations)} param combinations")

    results = []
    for i, params in enumerate(param_combinations):
        if i % 5 == 0:  # Progress indicator (reduced frequency)
            print(f"  {record_id}: {i}/{len(param_combinations)} combinations")

        result = evaluate_single_record(record_data, params, sample_rate)
        result['record_id'] = record_id
        result['combination_id'] = i
        results.append(result)

    return results
def run_exhaustive_search(data_path: str, output_path: str, sample_rate: int = 250,
                         n_jobs: int = -1, max_files: int = None, max_samples: int = None) -> None:
    """Executa busca exaustiva em todos os ficheiros."""

    # Carregar dados
    print(f"Loading data from {data_path}")
    df, _ = load_dataset(data_path, sample_rate=sample_rate)

    if 'id' not in df.columns:
        raise ValueError("Dataset deve conter coluna 'id' para processamento por ficheiro")

    # Agrupar por ID
    unique_ids = df['id'].unique()
    if max_files:
        unique_ids = unique_ids[:max_files]

    print(f"Found {len(unique_ids)} unique record IDs")

    # Criar combinações de parâmetros
    param_grid = create_param_grid()
    param_combinations = [dict(zip(param_grid.keys(), vals))
                         for vals in itertools.product(*param_grid.values())]

    print(f"Testing {len(param_combinations)} parameter combinations per file")
    print(f"Total evaluations: {len(unique_ids)} files × {len(param_combinations)} params = {len(unique_ids) * len(param_combinations):,}")

    # Processar cada ficheiro com todas as combinações
    print("Starting exhaustive grid search...")
    start_time = time.time()

    if n_jobs == 1:
        # Sequential processing
        all_results = []
        for record_id in unique_ids:
            record_data = df[df['id'] == record_id].copy()
            file_results = process_single_file_all_params(record_id, record_data, param_combinations, sample_rate, max_samples)
            all_results.extend(file_results)
    else:
        # Parallel processing
        file_tasks = []
        for record_id in unique_ids:
            record_data = df[df['id'] == record_id].copy()
            file_tasks.append((record_id, record_data, param_combinations, sample_rate, max_samples))

        parallel_results = Parallel(n_jobs=n_jobs)(
            delayed(process_single_file_all_params)(rid, rdata, pcomb, sr, max_samp)
            for rid, rdata, pcomb, sr, max_samp in file_tasks
        )

        all_results = []
        for file_result in parallel_results:
            all_results.extend(file_result)

    total_time = time.time() - start_time
    print(f"Exhaustive search completed in {total_time:.1f}s")
    print(f"Processed {len(all_results):,} total evaluations")

    # Salvar resultados completos
    results_df = pd.DataFrame(all_results)

    # Criar diretório se necessário
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Salvar em múltiplos formatos
    results_df.to_csv(output_path, index=False)

    jsonl_path = output_path.replace('.csv', '.jsonl')
    with open(jsonl_path, 'w') as f:
        for result in all_results:
            f.write(json.dumps(result) + '\n')

    # Análise resumida
    analyze_results(results_df, output_path.replace('.csv', '_summary.json'))

    print("Results saved to:")
    print(f"  Full results: {output_path}")
    print(f"  JSONL: {jsonl_path}")


def analyze_results(results_df: pd.DataFrame, summary_path: str) -> None:
    """Analisa resultados e encontra melhores parâmetros globais."""

    # Remover erros - usar F3 ponderado como filtro
    valid_results = results_df[~results_df['f3_weighted'].isna() & (results_df['f3_weighted'] >= 0)]

    if valid_results.empty:
        print("WARNING: No valid results found!")
        return

    # Encontrar melhor configuração global usando F3 ponderado como métrica principal
    param_cols = ['delta', 'ma_window', 'min_gap_samples']

    # Aggregate comprehensive metrics with F3 weighted as primary
    agg_metrics = {
        'f1_classic': ['mean', 'std', 'count'],       # Classic F1
        'f1_weighted': ['mean', 'std', 'count'],      # F1 weighted
        'f3_classic': ['mean', 'std', 'count'],       # Classic F3
        'f3_weighted': ['mean', 'std', 'count'],      # F3 weighted (PRIMARY)
        'recall_4s': ['mean', 'std'],                 # Recall@4s
        'recall_10s': ['mean', 'std'],                # Recall@10s
        'precision_4s': ['mean', 'std'],              # Precision@4s
        'precision_10s': ['mean', 'std'],             # Precision@10s
        'edd_median_s': 'mean',                       # Expected Detection Delay
        'fp_per_min': 'mean',                         # False Positives per minute
        'duration': 'mean'
    }

    global_perf = valid_results.groupby(param_cols).agg(agg_metrics).round(4)

    # Flatten column names
    global_perf.columns = ['_'.join(col).strip() for col in global_perf.columns]
    global_perf = global_perf.reset_index()

    # Best global parameters based on F3 weighted (primary metric)
    best_global_f3weighted = global_perf.loc[global_perf['f3_weighted_mean'].idxmax()]

    # Also track best F1 weighted and classic for comparison
    best_global_f1weighted = global_perf.loc[global_perf['f1_weighted_mean'].idxmax()]
    best_global_classic = global_perf.loc[global_perf['f1_classic_mean'].idxmax()]

    # Per-file best using F3 weighted metric
    file_best_f3weighted = valid_results.loc[valid_results.groupby('record_id')['f3_weighted'].idxmax()]
    file_best_f1weighted = valid_results.loc[valid_results.groupby('record_id')['f1_weighted'].idxmax()]
    file_best_classic = valid_results.loc[valid_results.groupby('record_id')['f1_classic'].idxmax()]

    summary = {
        'total_evaluations': len(results_df),
        'valid_evaluations': len(valid_results),
        'unique_files': results_df['record_id'].nunique(),
        'unique_param_combinations': len(results_df[param_cols].drop_duplicates()),

        # F3 weighted based results (PRIMARY)
        'best_global_params_f3weighted': {
            'delta': best_global_f3weighted['delta'],
            'ma_window': int(best_global_f3weighted['ma_window']),
            'min_gap_samples': int(best_global_f3weighted['min_gap_samples'])
        },
        'best_global_performance_f3weighted': {
            'f3_weighted_mean': best_global_f3weighted['f3_weighted_mean'],
            'f3_weighted_std': best_global_f3weighted['f3_weighted_std'],
            'f1_weighted_mean': best_global_f3weighted['f1_weighted_mean'],
            'recall_4s_mean': best_global_f3weighted['recall_4s_mean'],
            'recall_10s_mean': best_global_f3weighted['recall_10s_mean'],
            'precision_4s_mean': best_global_f3weighted['precision_4s_mean'],
            'precision_10s_mean': best_global_f3weighted['precision_10s_mean'],
            'edd_median_s_mean': best_global_f3weighted['edd_median_s_mean'],
            'fp_per_min_mean': best_global_f3weighted['fp_per_min_mean'],
            'n_files': int(best_global_f3weighted['f3_weighted_count'])
        },

        # F1 weighted based results (secondary)
        'best_global_params_f1weighted': {
            'delta': best_global_f1weighted['delta'],
            'ma_window': int(best_global_f1weighted['ma_window']),
            'min_gap_samples': int(best_global_f1weighted['min_gap_samples'])
        },
        'best_global_performance_f1weighted': {
            'f1_weighted_mean': best_global_f1weighted['f1_weighted_mean'],
            'f1_weighted_std': best_global_f1weighted['f1_weighted_std'],
            'n_files': int(best_global_f1weighted['f1_weighted_count'])
        },

        # Classic F1 based results (for comparison)
        'best_global_params_classic': {
            'delta': best_global_classic['delta'],
            'ma_window': int(best_global_classic['ma_window']),
            'min_gap_samples': int(best_global_classic['min_gap_samples'])
        },
        'best_global_performance_classic': {
            'f1_classic_mean': best_global_classic['f1_classic_mean'],
            'f1_classic_std': best_global_classic['f1_classic_std'],
            'n_files': int(best_global_classic['f1_classic_count'])
        },

        # Per-file performance statistics
        'per_file_performance_f3weighted': {
            'f3_weighted_mean': file_best_f3weighted['f3_weighted'].mean(),
            'f3_weighted_std': file_best_f3weighted['f3_weighted'].std(),
            'f3_weighted_min': file_best_f3weighted['f3_weighted'].min(),
            'f3_weighted_max': file_best_f3weighted['f3_weighted'].max()
        },
        'per_file_performance_classic': {
            'f1_mean': file_best_classic['f1_classic'].mean(),
            'f1_std': file_best_classic['f1_classic'].std(),
            'f1_min': file_best_classic['f1_classic'].min(),
            'f1_max': file_best_classic['f1_classic'].max()
        }
    }

    # Salvar sumário
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n=== BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric) ===")
    print(f"  delta: {best_global_f3weighted['delta']}")
    print(f"  ma_window: {int(best_global_f3weighted['ma_window'])}")
    print(f"  min_gap_samples: {int(best_global_f3weighted['min_gap_samples'])}")
    print(f"  F3 weighted: {best_global_f3weighted['f3_weighted_mean']:.4f} ± {best_global_f3weighted['f3_weighted_std']:.4f}")
    print(f"  F3 classic:  {best_global_f3weighted['f3_classic_mean']:.4f} ± {best_global_f3weighted['f3_classic_std']:.4f}")
    print(f"  F1 weighted: {best_global_f3weighted['f1_weighted_mean']:.4f} ± {best_global_f3weighted['f1_weighted_std']:.4f}")
    print(f"  F1 classic:  {best_global_f3weighted['f1_classic_mean']:.4f} ± {best_global_f3weighted['f1_classic_std']:.4f}")
    print(f"  Recall@4s: {best_global_f3weighted['recall_4s_mean']:.4f}")
    print(f"  Recall@10s: {best_global_f3weighted['recall_10s_mean']:.4f}")
    print(f"  Precision@4s: {best_global_f3weighted['precision_4s_mean']:.4f}")
    print(f"  Precision@10s: {best_global_f3weighted['precision_10s_mean']:.4f}")
    print(f"  EDD median: {best_global_f3weighted['edd_median_s_mean']:.2f}s")
    print(f"  FP/min: {best_global_f3weighted['fp_per_min_mean']:.2f}")

    print("\n=== COMPARISON WITH OTHER METRICS ===")
    print(f"F1 Weighted best: delta={best_global_f1weighted['delta']}, ma_window={int(best_global_f1weighted['ma_window'])}, min_gap={int(best_global_f1weighted['min_gap_samples'])}")
    print(f"F1 Classic best:   delta={best_global_classic['delta']}, ma_window={int(best_global_classic['ma_window'])}, min_gap={int(best_global_classic['min_gap_samples'])}")

    print(f"\nSummary saved to: {summary_path}")
def main():
    parser = argparse.ArgumentParser(description='Exhaustive Grid Search for ADWIN baseline detector')
    parser.add_argument('--data', required=True, help='Path to tidy CSV with id column')
    parser.add_argument('--output', required=True, help='Output CSV path for results')
    parser.add_argument('--sample-rate', type=int, default=250, help='Sampling rate')
    parser.add_argument('--n-jobs', type=int, default=-1, help='Number of parallel jobs')
    parser.add_argument('--max-files', type=int, default=None, help='Limit number of files (for testing)')
    parser.add_argument('--max-samples', type=int, default=None, help='Limit samples per file (for testing)')

    args = parser.parse_args()

    run_exhaustive_search(
        data_path=args.data,
        output_path=args.output,
        sample_rate=args.sample_rate,
        n_jobs=args.n_jobs,
        max_files=args.max_files,
        max_samples=args.max_samples
    )
if __name__ == '__main__':
    main()
