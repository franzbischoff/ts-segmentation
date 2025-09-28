#!/usr/bin/env python3
"""
Exhaustive Grid Search para detector ADWIN baseline.
Similar à abordagedef run_exhaustive_search(data_path: str, output_path: str, sample_rate: int = 250,
                         n_jobs: int = -1, max_files: int = None, max_samples: int = None) -> None:R: testa todas as combinações possíveis em cada ficheiro,
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
        'ma_window': list(range(25, 200, 25)),                                            # 7 valores (25,50,75,100,125,150,175)
        'min_gap_samples': list(range(1000, 6000, 1000)),                               # 5 valores (1000,2000,3000,4000,5000)
    }
    # Total: 11 × 7 × 5 = 385 combinações (versão completa)


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

        # Extrair métricas do resultado
        precision = metrics.get('precision', 0.0)
        recall = metrics.get('recall', 0.0)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        result = {
            **params,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'duration': time.time() - start_time,
            'n_detections': len(events),
            'n_ground_truth': len(record_data[record_data['regime_change'] == 1])
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

    # Remover erros
    valid_results = results_df[~results_df['f1'].isna() & (results_df['f1'] > 0)]

    if valid_results.empty:
        print("WARNING: No valid results found!")
        return

    # Encontrar melhor configuração global (média de F1 por combinação)
    param_cols = ['delta', 'ma_window', 'min_gap_samples']
    global_perf = valid_results.groupby(param_cols).agg({
        'f1': ['mean', 'std', 'count'],
        'precision': ['mean', 'std'],
        'recall': ['mean', 'std'],
        'duration': 'mean'
    }).round(4)

    # Flatten column names
    global_perf.columns = ['_'.join(col).strip() for col in global_perf.columns]
    global_perf = global_perf.reset_index()

    # Best global parameters
    best_global = global_perf.loc[global_perf['f1_mean'].idxmax()]

    # Per-file best (para comparação)
    file_best = valid_results.loc[valid_results.groupby('record_id')['f1'].idxmax()]

    summary = {
        'total_evaluations': len(results_df),
        'valid_evaluations': len(valid_results),
        'unique_files': results_df['record_id'].nunique(),
        'unique_param_combinations': len(results_df[param_cols].drop_duplicates()),

        'best_global_params': {
            'delta': best_global['delta'],
            'ma_window': int(best_global['ma_window']),
            'min_gap_samples': int(best_global['min_gap_samples'])
        },
        'best_global_performance': {
            'f1_mean': best_global['f1_mean'],
            'f1_std': best_global['f1_std'],
            'precision_mean': best_global['precision_mean'],
            'recall_mean': best_global['recall_mean'],
            'n_files': int(best_global['f1_count'])
        },

        'per_file_performance_stats': {
            'f1_mean': file_best['f1'].mean(),
            'f1_std': file_best['f1'].std(),
            'f1_min': file_best['f1'].min(),
            'f1_max': file_best['f1'].max()
        }
    }

    # Salvar sumário
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print("\nBEST GLOBAL PARAMETERS:")
    print(f"  delta: {best_global['delta']}")
    print(f"  ma_window: {int(best_global['ma_window'])}")
    print(f"  min_gap_samples: {int(best_global['min_gap_samples'])}")
    print(f"  F1 mean: {best_global['f1_mean']:.4f} ± {best_global['f1_std']:.4f}")
    print(f"Summary saved to: {summary_path}")


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
