from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import numpy as np
import pandas as pd

@dataclass
class DetectionEvent:
    detector: str
    sample_index: int
    time_seconds: float


def evaluate_detections(events: List[DetectionEvent], df: pd.DataFrame, sample_rate: int, tolerance: int = 50) -> Dict[str, float]:
    """Evaluate detections vs ground-truth regime_change markers.

    tolerance: number of samples allowed between detection and true change start to count as TP.
    """
    if not events:
        return {"tp": 0, "fp": 0, "fn": int(df['regime_change'].sum()), "recall": 0.0, "precision": 0.0, "mean_delay_samples": float('nan')}

    gt_indices = df.index[df['regime_change'] == 1].tolist()
    detections = sorted(events, key=lambda e: e.sample_index)

    tp = 0
    fp = 0
    delays = []
    matched_gt = set()
    for ev in detections:
        # find nearest future or current gt not yet matched within tolerance window
        candidates = [g for g in gt_indices if g not in matched_gt and 0 <= ev.sample_index - g <= tolerance]
        if candidates:
            # choose closest (smallest delay)
            best = min(candidates, key=lambda g: ev.sample_index - g)
            delay = ev.sample_index - best
            delays.append(delay)
            matched_gt.add(best)
            tp += 1
        else:
            fp += 1
    fn = len(gt_indices) - len(matched_gt)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    mean_delay = float(np.mean(delays)) if delays else float('nan')
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "mean_delay_samples": mean_delay,
        "mean_delay_seconds": mean_delay / sample_rate if not np.isnan(mean_delay) else float('nan')
    }
