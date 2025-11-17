from __future__ import annotations
import argparse
from typing import List
import pandas as pd
import json
import os
from datetime import datetime, timezone

from .data_loader import load_dataset
from .detectors import build_detector
from .evaluation import DetectionEvent, evaluate_detections, evaluate_detections_comprehensive
import numpy as np


def run_stream_on_dataframe(df, detector_name: str, sample_rate: int, tolerance: int = 50,
                            detector_params: dict | None = None, ma_window: int | None = None,
                            use_derivative: bool = False, min_gap_samples: int | None = None):
    """Core logic operating on an already loaded dataframe."""
    detector = build_detector(detector_name, **(detector_params or {}))

    events: List[DetectionEvent] = []

    signal = df['ecg'].values.astype(float)
    if ma_window and ma_window > 1:
        kernel = np.ones(ma_window) / ma_window
        signal = np.convolve(signal, kernel, mode='same')
    if use_derivative:
        # simple first difference, pad with zero at start
        diff = np.zeros_like(signal)
        diff[1:] = np.diff(signal)
        signal = diff

    # Streaming loop
    last_detection_idx = -10**12
    for idx, row in enumerate(df.itertuples()):
        value = float(signal[idx])
        detected = detector.add_element(value)
        if detected:
            if min_gap_samples is not None and (row.sample_index - last_detection_idx) < min_gap_samples:
                continue
            last_detection_idx = row.sample_index
            events.append(DetectionEvent(detector=detector.name,
                                         sample_index=row.sample_index,
                                         time_seconds=row.sample_index / sample_rate))

    # Use comprehensive evaluation that includes both classic and F1* metrics
    metrics = evaluate_detections_comprehensive(
        events, df, sample_rate,
        tolerance=tolerance,
        signal_duration_samples=len(df)
    )

    # Output results
    return events, metrics, detector.name


def run_stream(data_path: str | None, detector_name: str, sample_rate: int, batch: int = 1, tolerance: int = 50,
               force_regenerate: bool = False, n_segments: int = 5, segment_length: int = 1000, detector_params: dict | None = None,
               ma_window: int | None = None, use_derivative: bool = False, min_gap_samples: int | None = None,
               log_json: bool = True, log_dir: str = 'results'):
    df, sample_rate = load_dataset(data_path, sample_rate, force_regenerate=force_regenerate,
                                   n_segments=n_segments, segment_length=segment_length)
    events, metrics, detector_name_resolved = run_stream_on_dataframe(df, detector_name, sample_rate, tolerance=tolerance,
                                                                      detector_params=detector_params, ma_window=ma_window,
                                                                      use_derivative=use_derivative, min_gap_samples=min_gap_samples)

    print("=== RESULTADOS DETECÇÃO ===")
    print(f"Detector: {detector_name_resolved}")
    print(f"Total amostras: {len(df)}")
    print(f"Mudanças verdade (gt): {int(df['regime_change'].sum())}")
    print(f"Detecções: {len(events)}")
    print("-- Métricas --")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("-- Detecções (primeiras 20) --")
    for ev in events[:20]:
        print(f"sample_index={ev.sample_index} time_s={ev.time_seconds:.3f}")

    # CSV de saída de eventos
    out_events_path = 'data/detections_' + detector_name_resolved + '.csv'
    pd.DataFrame([e.__dict__ for e in events]).to_csv(out_events_path, index=False)
    print(f"Eventos exportados em: {out_events_path}")

    # Logging JSON
    if log_json:
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        log_path = os.path.join(log_dir, f'run_{detector_name_resolved}_{ts}.json')
        payload = {
            'timestamp_utc': ts,
            'detector': detector_name_resolved,
            'detector_params': detector_params or {},
            'sample_rate': sample_rate,
            'tolerance': tolerance,
            'ma_window': ma_window,
            'use_derivative': use_derivative,
            'min_gap_samples': min_gap_samples,
            'data_path': data_path,
            'synthetic': data_path is None,
            'n_segments': n_segments,
            'segment_length': segment_length,
            'force_regenerate': force_regenerate,
            'metrics': metrics,
            'events_count': len(events),
            'events_preview': [e.__dict__ for e in events[:10]],
            'events_csv': out_events_path,
            'f1_classic': metrics.get('f1_classic', 0),
            'f1_star': metrics.get('f1star_f1_star', 0)
        }
        with open(log_path, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"Log JSON: {log_path}")

    return events, metrics


def parse_args():
    ap = argparse.ArgumentParser(description="Streaming regime change detection baseline")
    ap.add_argument('--data', type=str, default=None, help='Caminho para CSV com sinal ECG')
    ap.add_argument('--detector', type=str, default='page_hinkley', help='Detector: page_hinkley|adwin|kswin|hddm_a|hddm_w')
    ap.add_argument('--sample-rate', type=int, default=250, help='Frequência de amostragem (Hz)')
    ap.add_argument('--tolerance', type=int, default=50, help='Tolerância em samples para casar detecção com ground-truth')
    ap.add_argument('--force-regen', action='store_true', help='Força regenerar sinal sintético (se sem data)')
    ap.add_argument('--segments', type=int, default=5, help='Número de segmentos sintéticos')
    ap.add_argument('--segment-length', type=int, default=1000, help='Tamanho de cada segmento sintético')
    ap.add_argument('--param', action='append', default=[], help='Parâmetro do detector no formato chave=valor (ex: --param lambda_=80 --param delta=0.01)')
    ap.add_argument('--ma-window', type=int, default=None, help='Tamanho janela média móvel para suavizar')
    ap.add_argument('--derivative', action='store_true', help='Usar derivada primeira do sinal (diferença)')
    ap.add_argument('--min-gap-samples', type=int, default=None, help='Número mínimo de samples entre detecções consecutivas (pós-processamento)')
    ap.add_argument('--log-json-dir', type=str, default='results', help='Diretório para salvar logs JSON')
    ap.add_argument('--no-json-log', action='store_true', help='Desativa logging JSON')
    return ap.parse_args()


if __name__ == '__main__':
    args = parse_args()
    # Parse detector params
    det_params = {}
    for p in args.param:
        if '=' not in p:
            raise SystemExit(f'Parâmetro inválido: {p}. Use chave=valor')
        k, v = p.split('=', 1)
        # tentar converter numérico
        try:
            if '.' in v or 'e' in v.lower():
                v_conv = float(v)
            else:
                v_conv = int(v)
            det_params[k] = v_conv
        except ValueError:
            det_params[k] = v

    run_stream(args.data, args.detector, args.sample_rate, tolerance=args.tolerance,
               force_regenerate=args.force_regen, n_segments=args.segments, segment_length=args.segment_length,
               detector_params=det_params, ma_window=args.ma_window, use_derivative=args.derivative,
               min_gap_samples=args.min_gap_samples, log_json=not args.no_json_log,
               log_dir=args.log_json_dir)
