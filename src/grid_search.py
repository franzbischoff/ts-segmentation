from __future__ import annotations
import itertools
import json
import os
from datetime import datetime, timezone

from .data_loader import load_dataset
from .streaming_detector import run_stream_on_dataframe

# Simple grid search over detector parameters & preprocessing choices.
# Usage (from project root):
#   python -m src.grid_search --detector adwin --force-regen

import argparse

def parse_args():
    ap = argparse.ArgumentParser(description='Grid search simples para detecção de mudanças')
    ap.add_argument('--detector', type=str, default='adwin')
    ap.add_argument('--data', type=str, default=None)
    ap.add_argument('--sample-rate', type=int, default=250)
    ap.add_argument('--tolerance', type=int, default=120)
    ap.add_argument('--force-regen', action='store_true')
    ap.add_argument('--segments', type=int, default=6)
    ap.add_argument('--segment-length', type=int, default=800)
    ap.add_argument('--out', type=str, default='results/grid_search_summary.json')
    ap.add_argument('--seed', type=int, default=42, help='Seed para regenerar dado sintético (se aplicável)')
    ap.add_argument('--no-regen', action='store_true', help='Não regenerar dataset sintético se já existir')
    return ap.parse_args()


def main():
    args = parse_args()

    # Parameter grid definitions (adjust as needed)
    if args.detector.lower() == 'adwin':
        detector_param_grid = {
            'delta': [0.005, 0.008, 0.01, 0.02]
        }
    elif args.detector.lower() in {'page_hinkley', 'ph'}:
        detector_param_grid = {
            'lambda_': [30, 40, 60],
            'delta': [0.005, 0.01],
            'alpha': [0.0001]
        }
    else:
        detector_param_grid = {}

    preprocess_grid = {
        'ma_window': [None, 20, 30],
        'use_derivative': [False, True],
        'min_gap_samples': [None, 60, 80]
    }

    # Build combinations
    detector_param_keys = list(detector_param_grid.keys())
    detector_param_values = list(detector_param_grid.values()) if detector_param_keys else [[]]
    if not detector_param_keys:
        detector_param_values = [[]]

    # Load dataset once
    df, _ = load_dataset(args.data, args.sample_rate, force_regenerate=(args.force_regen and not args.no_regen),
                         n_segments=args.segments, segment_length=args.segment_length)

    results = []
    total_runs = 0
    for det_vals in itertools.product(*detector_param_values):
        det_param_dict = dict(zip(detector_param_keys, det_vals)) if detector_param_keys else {}
        for ma_window in preprocess_grid['ma_window']:
            for use_derivative in preprocess_grid['use_derivative']:
                for min_gap in preprocess_grid['min_gap_samples']:
                    total_runs += 1
                    events, metrics, _ = run_stream_on_dataframe(
                        df=df,
                        detector_name=args.detector,
                        sample_rate=args.sample_rate,
                        tolerance=args.tolerance,
                        detector_params=det_param_dict,
                        ma_window=ma_window,
                        use_derivative=use_derivative,
                        min_gap_samples=min_gap
                    )
                    precision = metrics.get('precision', 0)
                    recall = metrics.get('recall', 0)
                    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
                    results.append({
                        'detector': args.detector,
                        'detector_params': det_param_dict,
                        'ma_window': ma_window,
                        'use_derivative': use_derivative,
                        'min_gap_samples': min_gap,
                        'metrics': metrics,
                        'f1': f1,
                        'events_count': len(events)
                    })
                    print(f"[GRID] det={args.detector} params={det_param_dict} ma={ma_window} der={use_derivative} gap={min_gap} -> f1={f1:.4f}")

    # Rank results
    results_sorted = sorted(results, key=lambda r: r['f1'], reverse=True)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    # Ranking detalhado com posição
    for rank, rec in enumerate(results_sorted, start=1):
        rec['rank'] = rank

    summary = {
        'timestamp_utc': datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
        'detector': args.detector,
        'total_runs': total_runs,
        'dataset_rows': len(df),
        'top5': results_sorted[:5],
        'all_results': results_sorted
    }
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    print(f"Resumo salvo em {args.out}")


if __name__ == '__main__':
    main()
