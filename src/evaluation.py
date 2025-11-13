from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional
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


def temporal_weight_function(delta: float, plateau: float = 4.0, tau: float = 10.0) -> float:
    """
    Temporal weight function w(δ) for latency-weighted F1*.

    Args:
        delta: Delay in seconds (detection_time - gt_time)
        plateau: Time threshold for maximum weight (default 4s)
        tau: Maximum acceptable delay (default 10s)

    Returns:
        Weight value between 0.0 and 1.0
    """
    if delta < 0:
        return 0.0  # Detection before event is FP (not TP)
    if delta <= plateau:
        return 1.0  # 0-4s: maximum weight
    if delta <= tau:
        return 1.0 - (delta - plateau) / (tau - plateau)  # Linear decay 4-10s
    return 0.0  # >10s: doesn't count as success


def latency_weighted_f1(
    gt: List[float],
    det: List[float],
    tau: float = 10.0,
    plateau: float = 4.0,
    rho: float = 4.0,
    count_extra_within_rho_as_fp: bool = False,
    duration: Optional[float] = None
) -> Dict[str, float]:
    """
    Compute F1* score weighted by detection latency for streaming change point detection.

    Args:
        gt: Ground truth timestamps (seconds), should be sorted
        det: Detection timestamps (seconds), should be sorted
        tau: Maximum acceptable delay (seconds)
        plateau: Optimal delay threshold (seconds)
        rho: Deduplication window (seconds)
        count_extra_within_rho_as_fp: If True, extra detections within rho count as FP
        duration: Total signal duration for FP rate calculation

    Returns:
        Dictionary with metrics: precision_star, recall_star, f1_star, tp, fp, fn,
        tp_weight_sum, recall_4s, edd_median, edd_p95, fp_per_min
    """
    # Ensure inputs are sorted
    gt = sorted(gt)
    det = sorted(det)

    if not gt:  # No ground truth events
        return {
            'precision_star': 0.0 if det else 0.0,
            'recall_star': 0.0,
            'f1_star': 0.0,
            'tp': 0,
            'fp': len(det),
            'fn': 0,
            'tp_weight_sum': 0.0,
            'recall_4s': 0.0,
            'edd_median': np.nan,
            'edd_p95': np.nan,
            'fp_per_min': len(det) / (duration / 60.0) if duration else np.nan
        }

    if not det:  # No detections
        return {
            'precision_star': 0.0,
            'recall_star': 0.0,
            'f1_star': 0.0,
            'tp': 0,
            'fp': 0,
            'fn': len(gt),
            'tp_weight_sum': 0.0,
            'recall_4s': 0.0,
            'edd_median': np.nan,
            'edd_p95': np.nan,
            'fp_per_min': 0.0
        }

    # Initialize tracking variables
    gt_matched = [False] * len(gt)
    tp_weights = []
    delays = []
    fp_count = 0

    # New algorithm: Process GT chronologically, handle overlapping ignore windows
    det_processed = [False] * len(det)
    current_ignore_until = -float('inf')  # Track until when we should ignore detections

    for gi, gt_time in enumerate(gt):
        # Skip this GT if we're still in an ignore window from previous GT
        if gt_time < current_ignore_until:
            continue

        # Find first valid detection for this GT (after gt_time, not yet processed)
        first_detection = None
        first_detection_idx = None

        for j, det_time in enumerate(det):
            if (det_time >= gt_time and
                det_time <= gt_time + tau and
                not det_processed[j]):
                first_detection = det_time
                first_detection_idx = j
                break

        if first_detection is not None:
            # Process this detection as TP
            delta = first_detection - gt_time
            weight = temporal_weight_function(delta, plateau, tau)

            tp_weights.append(weight)
            delays.append(delta)
            gt_matched[gi] = True
            det_processed[first_detection_idx] = True

            # Set ignore window: ignore detections until gt_time + tau
            # BUT only if there's no other GT in this interval
            ignore_until = gt_time + tau

            # Check if there are other GTs within the ignore window
            next_gt_in_window = None
            for next_gi in range(gi + 1, len(gt)):
                if gt[next_gi] <= ignore_until:
                    next_gt_in_window = gt[next_gi]
                    break

            if next_gt_in_window is not None:
                # There's another GT in the ignore window - only ignore until that GT
                current_ignore_until = next_gt_in_window
            else:
                # No GT in ignore window - ignore until full tau
                current_ignore_until = ignore_until

            # Mark additional detections in current ignore window
            for j, det_time in enumerate(det):
                if (det_time > first_detection and
                    det_time < current_ignore_until and
                    not det_processed[j]):
                    det_processed[j] = True
                    if count_extra_within_rho_as_fp:
                        fp_count += 1
        # If no detection found for this GT, it remains unmatched (FN)

    # Count unprocessed detections as FP
    for j, processed in enumerate(det_processed):
        if not processed:
            fp_count += 1    # Count unmatched GT events as FN
    fn_count = sum(1 for matched in gt_matched if not matched)
    tp_count = len(tp_weights)
    tp_weight_sum = sum(tp_weights)

    # Calculate primary metrics
    # For precision_star: we consider TP count (not weight) + FP count in denominator
    # but weight the numerator. This makes precision_star = weight_ratio when no FPs
    precision_star = tp_weight_sum / (tp_count + fp_count) if (tp_count + fp_count) > 0 else 0.0
    recall_star = tp_weight_sum / len(gt) if len(gt) > 0 else 0.0
    f1_star = (2 * precision_star * recall_star / (precision_star + recall_star)
               if (precision_star + recall_star) > 0 else 0.0)

    # Calculate auxiliary metrics
    recall_4s_weights = [1.0 if d <= plateau else 0.0 for d in delays]
    recall_4s = sum(recall_4s_weights) / len(gt) if len(gt) > 0 else 0.0

    edd_median = np.median(delays) if delays else np.nan
    edd_p95 = np.percentile(delays, 95) if delays else np.nan
    fp_per_min = fp_count / (duration / 60.0) if duration else np.nan

    return {
        'precision_star': precision_star,
        'recall_star': recall_star,
        'f1_star': f1_star,
        'tp': tp_count,
        'fp': fp_count,
        'fn': fn_count,
        'tp_weight_sum': tp_weight_sum,
        'recall_4s': recall_4s,
        'edd_median': edd_median,
        'edd_p95': edd_p95,
        'fp_per_min': fp_per_min
    }


def evaluate_detections_comprehensive(
    events: List[DetectionEvent],
    df: pd.DataFrame,
    sample_rate: int,
    tolerance: int = 50,
    signal_duration_samples: Optional[int] = None
) -> Dict[str, float]:
    """
    Comprehensive evaluation combining both classic and latency-weighted F1* metrics.

    Args:
        events: List of detection events
        df: DataFrame with ground truth regime_change markers
        sample_rate: Sampling rate in Hz
        tolerance: Classic tolerance in samples
        signal_duration_samples: Total signal length for FP rate calculation

    Returns:
        Dictionary with both classic metrics and F1* metrics
    """
    # Get classic metrics
    classic_metrics = evaluate_detections(events, df, sample_rate, tolerance)

    if not events:
        # No detections case
        f1_star_metrics = latency_weighted_f1([], [])
        # Add signal duration info
        if signal_duration_samples:
            f1_star_metrics['fp_per_min'] = 0.0

        # Combine results with prefix
        result = {}
        for k, v in classic_metrics.items():
            result[f'classic_{k}'] = v
        for k, v in f1_star_metrics.items():
            result[f'f1star_{k}'] = v

        return result

    # Extract timestamps for F1* calculation
    gt_times = []
    if len(df) > 0:
        gt_indices = df.index[df['regime_change'] == 1].tolist()
        gt_times = [idx / sample_rate for idx in gt_indices]

    det_times = [event.time_seconds for event in events]

    # Calculate signal duration in seconds
    duration_seconds = None
    if signal_duration_samples is not None:
        duration_seconds = signal_duration_samples / sample_rate
    elif len(df) > 0:
        duration_seconds = len(df) / sample_rate

    # Convert tolerance from samples to seconds for F1*
    tau_seconds = tolerance / sample_rate
    plateau_seconds = min(4.0, tau_seconds * 0.4)  # 40% of tolerance or 4s, whichever is smaller
    rho_seconds = min(4.0, tau_seconds * 0.5)      # 50% of tolerance or 4s for deduplication

    # Calculate F1* metrics
    f1_star_metrics = latency_weighted_f1(
        gt=gt_times,
        det=det_times,
        tau=tau_seconds,
        plateau=plateau_seconds,
        rho=rho_seconds,
        duration=duration_seconds
    )

    # Combine results with prefixes to avoid naming conflicts
    result = {}
    for k, v in classic_metrics.items():
        result[f'classic_{k}'] = v
    for k, v in f1_star_metrics.items():
        result[f'f1star_{k}'] = v

    # Add some convenience metrics
    result['f1_classic'] = (2 * classic_metrics['precision'] * classic_metrics['recall'] /
                           (classic_metrics['precision'] + classic_metrics['recall'])
                           if (classic_metrics['precision'] + classic_metrics['recall']) > 0 else 0.0)

    return result


def calculate_comprehensive_metrics(
    gt: List[float],
    det: List[float],
    tau: float = 10.0,
    plateau: float = 4.0,
    duration: Optional[float] = None
) -> Dict[str, float]:
    """
    Calculate all comprehensive metrics as requested:
    - F1-score (classic and weighted)
    - F3-score (classic and weighted)
    - Recall@4s, Recall@10s, Precision@4s, Precision@10s
    - EDD and FP/min

    Args:
        gt: Ground truth timestamps (seconds)
        det: Detection timestamps (seconds)
        tau: Maximum acceptable delay (10s)
        plateau: Optimal delay threshold (4s)
        duration: Total signal duration for FP rate
    """
    # Use corrected latency_weighted_f1 with count_extra_within_rho_as_fp=False
    weighted_results = latency_weighted_f1(
        gt=gt, det=det, tau=tau, plateau=plateau,
        count_extra_within_rho_as_fp=False, duration=duration
    )

    # Calculate classic metrics (binary TP/FP/FN without weights)
    classic_tp = weighted_results['tp']
    classic_fp = weighted_results['fp']
    classic_fn = weighted_results['fn']

    classic_precision = classic_tp / (classic_tp + classic_fp) if (classic_tp + classic_fp) > 0 else 0.0
    classic_recall = classic_tp / (classic_tp + classic_fn) if (classic_tp + classic_fn) > 0 else 0.0

    # F1 scores
    f1_classic = (2 * classic_precision * classic_recall /
                  (classic_precision + classic_recall)) if (classic_precision + classic_recall) > 0 else 0.0
    f1_weighted = weighted_results['f1_star']

    # F3 scores (beta=3 emphasizes recall)
    beta = 3.0
    f3_classic = ((1 + beta**2) * classic_precision * classic_recall /
                  (beta**2 * classic_precision + classic_recall)) if (beta**2 * classic_precision + classic_recall) > 0 else 0.0

    precision_star = weighted_results['precision_star']
    recall_star = weighted_results['recall_star']
    f3_weighted = ((1 + beta**2) * precision_star * recall_star /
                   (beta**2 * precision_star + recall_star)) if (beta**2 * precision_star + recall_star) > 0 else 0.0

    # Calculate Recall@τ and Precision@τ for both 4s and 10s
    # For this, we need to recompute with different tau values

    # Recall@4s and Precision@4s
    results_4s = latency_weighted_f1(gt=gt, det=det, tau=4.0, plateau=4.0,
                                     count_extra_within_rho_as_fp=False, duration=duration)
    recall_4s = results_4s['tp'] / len(gt) if len(gt) > 0 else 0.0
    precision_4s = results_4s['tp'] / (results_4s['tp'] + results_4s['fp']) if (results_4s['tp'] + results_4s['fp']) > 0 else 0.0

    # Recall@10s and Precision@10s
    results_10s = latency_weighted_f1(gt=gt, det=det, tau=10.0, plateau=10.0,
                                      count_extra_within_rho_as_fp=False, duration=duration)
    recall_10s = results_10s['tp'] / len(gt) if len(gt) > 0 else 0.0
    precision_10s = results_10s['tp'] / (results_10s['tp'] + results_10s['fp']) if (results_10s['tp'] + results_10s['fp']) > 0 else 0.0

    # Calculate NAB scores with different application profiles
    # Use tau as window width for NAB (events within tau seconds are in the window)
    nab_standard = calculate_nab_score(
        gt_times=gt,
        det_times=det,
        window_width=tau,
        cost_matrix=NABCostMatrix.standard(),
        signal_duration=duration if duration else max(gt[-1], det[-1]) if gt and det else 100.0,
        probation_percent=0.15
    ) if gt else {'nab_score': 0.0, 'tp': 0, 'fp': len(det), 'fn': 0}

    nab_low_fp = calculate_nab_score(
        gt_times=gt,
        det_times=det,
        window_width=tau,
        cost_matrix=NABCostMatrix.reward_low_fp(),
        signal_duration=duration if duration else max(gt[-1], det[-1]) if gt and det else 100.0,
        probation_percent=0.15
    ) if gt else {'nab_score': 0.0, 'tp': 0, 'fp': len(det), 'fn': 0}

    nab_low_fn = calculate_nab_score(
        gt_times=gt,
        det_times=det,
        window_width=tau,
        cost_matrix=NABCostMatrix.reward_low_fn(),
        signal_duration=duration if duration else max(gt[-1], det[-1]) if gt and det else 100.0,
        probation_percent=0.15
    ) if gt else {'nab_score': 0.0, 'tp': 0, 'fp': len(det), 'fn': 0}

    return {
        # F-scores
        'f1_classic': f1_classic,
        'f1_weighted': f1_weighted,
        'f3_classic': f3_classic,
        'f3_weighted': f3_weighted,

        # Recall and Precision at thresholds
        'recall_4s': recall_4s,
        'recall_10s': recall_10s,
        'precision_4s': precision_4s,
        'precision_10s': precision_10s,

        # Expected Detection Delay and False Positive rate
        'edd_median_s': weighted_results['edd_median'],
        'edd_p95_s': weighted_results['edd_p95'],
        'fp_per_min': weighted_results['fp_per_min'],

        # NAB scores (Numenta Anomaly Benchmark)
        'nab_score_standard': nab_standard['nab_score'],
        'nab_score_low_fp': nab_low_fp['nab_score'],
        'nab_score_low_fn': nab_low_fn['nab_score'],

        # Raw counts for reference
        'tp': classic_tp,
        'fp': classic_fp,
        'fn': classic_fn,
        'tp_weight_sum': weighted_results['tp_weight_sum']
    }


# ============================================================================
# Numenta Anomaly Benchmark (NAB) Scoring Functions
# ============================================================================

def sigmoid(x: float) -> float:
    """Standard sigmoid function."""
    return 1.0 / (1.0 + np.exp(-x))


def nab_scaled_sigmoid(relative_position_in_window: float) -> float:
    """
    Return a scaled sigmoid function given a relative position within a labeled window.

    This is the NAB scoring function that assigns scores based on how early/late
    a detection occurs relative to an anomaly window.

    The function is computed as follows:
    - A relative position of -1.0 is the far left edge of the anomaly window and
      corresponds to S = 2*sigmoid(5) - 1.0 = 0.98661. This is the earliest detection
      to be counted as a true positive (maximum score).

    - A relative position of -0.5 is halfway into the anomaly window and
      corresponds to S = 2*sigmoid(0.5*5) - 1.0 = 0.84828.

    - A relative position of 0.0 consists of the right edge of the window and
      corresponds to S = 2*sigmoid(0) - 1 = 0.0.

    - Relative positions > 0 correspond to false positives increasingly far away
      from the right edge of the window. A relative position of 1.0 is past the
      right edge of the window and corresponds to a score of 2*sigmoid(-5) - 1.0 = -0.98661.

    Args:
        relative_position_in_window: A relative position within or after a window.
            -1.0 = left edge (start) of window
             0.0 = right edge (end) of window
            >0.0 = after window (false positive territory)

    Returns:
        Score value between -1.0 and ~1.0
    """
    if relative_position_in_window > 3.0:
        # FP well behind window
        return -1.0
    else:
        return 2.0 * sigmoid(-5.0 * relative_position_in_window) - 1.0


@dataclass
class NABAnomalyPoint:
    """Represents a single point in NAB scoring."""
    timestamp: float
    anomaly_score: float
    sweep_score: float
    window_name: Optional[str]


@dataclass
class NABCostMatrix:
    """
    NAB cost matrix for different application profiles.

    Three standard profiles defined by NAB:
    1. Standard: Balanced (tp=1.0, fp=0.11, fn=1.0)
    2. Reward Low FP: Heavily penalize false positives (tp=1.0, fp=0.22, fn=1.0)
    3. Reward Low FN: Heavily penalize false negatives (tp=1.0, fp=0.055, fn=2.0)
    """
    tp_weight: float = 1.0
    fp_weight: float = 0.11
    fn_weight: float = 1.0

    @classmethod
    def standard(cls) -> 'NABCostMatrix':
        """Standard balanced profile."""
        return cls(tp_weight=1.0, fp_weight=0.11, fn_weight=1.0)

    @classmethod
    def reward_low_fp(cls) -> 'NABCostMatrix':
        """Profile that rewards low false positive rate."""
        return cls(tp_weight=1.0, fp_weight=0.22, fn_weight=1.0)

    @classmethod
    def reward_low_fn(cls) -> 'NABCostMatrix':
        """Profile that rewards low false negative rate."""
        return cls(tp_weight=1.0, fp_weight=0.055, fn_weight=2.0)


def calculate_nab_score(
    gt_times: List[float],
    det_times: List[float],
    window_width: float,
    cost_matrix: NABCostMatrix,
    signal_duration: float,
    probation_percent: float = 0.15
) -> Dict[str, float]:
    """
    Calculate NAB (Numenta Anomaly Benchmark) score for streaming anomaly detection.

    The NAB scoring rewards early detection within anomaly windows and penalizes
    late detection and false positives. The score uses a sigmoid function to
    weight detections based on their position within the anomaly window.

    Args:
        gt_times: Ground truth event timestamps (seconds)
        det_times: Detection timestamps (seconds)
        window_width: Width of anomaly window after each GT event (seconds)
        cost_matrix: Cost matrix defining weights for TP, FP, FN
        signal_duration: Total signal duration (seconds)
        probation_percent: Fraction of signal at start to exclude from scoring

    Returns:
        Dictionary with NAB metrics:
        - nab_score: Final NAB score (normalized)
        - nab_score_raw: Raw score before normalization
        - tp: True positive count
        - fp: False positive count
        - fn: False negative count
        - tn: True negative count
    """
    if not gt_times:
        # No ground truth - only FP penalties
        return {
            'nab_score': -cost_matrix.fp_weight * len(det_times),
            'nab_score_raw': -cost_matrix.fp_weight * len(det_times),
            'tp': 0,
            'fp': len(det_times),
            'fn': 0,
            'tn': 0
        }

    # Sort inputs
    gt_times = sorted(gt_times)
    det_times = sorted(det_times)

    # Calculate probationary period (data at start that doesn't count toward score)
    probation_length = min(
        signal_duration * probation_percent,
        probation_percent * 5000.0  # NAB caps probation at this many seconds
    )

    # Create windows: each GT event has a window of [gt_time, gt_time + window_width]
    windows = [(gt, gt + window_width) for gt in gt_times]

    # Maximum TP score (score at left edge of window)
    max_tp = nab_scaled_sigmoid(-1.0)

    # Track which detections and windows have been matched
    det_matched = [False] * len(det_times)
    window_best_score = {}  # window_name -> best score seen so far

    # Initialize FN penalty for each window
    for i, (win_start, win_end) in enumerate(windows):
        window_name = f"window_{i}"
        window_best_score[window_name] = -cost_matrix.fn_weight

    # Process each detection
    fp_score = 0.0
    prev_window_end = -float('inf')

    for det_idx, det_time in enumerate(det_times):
        # Skip if in probationary period
        if det_time < probation_length:
            continue

        # Find which window (if any) this detection falls into or after
        in_window = False
        window_name = None

        for i, (win_start, win_end) in enumerate(windows):
            if win_start <= det_time <= win_end:
                # Detection inside window - potential TP
                window_name = f"window_{i}"
                in_window = True

                # Calculate position within window
                # -1.0 at start, 0.0 at end
                position_in_window = -1.0 + (det_time - win_start) / window_width
                unweighted_score = nab_scaled_sigmoid(position_in_window)
                weighted_score = unweighted_score * cost_matrix.tp_weight / max_tp

                # Only update if this is better than what we've seen for this window
                if weighted_score > window_best_score[window_name]:
                    window_best_score[window_name] = weighted_score

                det_matched[det_idx] = True
                break

        if not in_window:
            # Detection outside any window - FP
            # Calculate how far from nearest previous window
            if prev_window_end > -float('inf'):
                # There was a previous window
                # Calculate relative position past the window
                # Find the window width of that previous window
                prev_width = window_width  # assuming all windows same width
                position_past_window = (det_time - prev_window_end) / prev_width
                unweighted_score = nab_scaled_sigmoid(position_past_window)
            else:
                # No previous window - far from any anomaly
                unweighted_score = -1.0

            weighted_score = unweighted_score * cost_matrix.fp_weight
            fp_score += weighted_score
            det_matched[det_idx] = True

        # Update prev_window_end for FP scoring
        for win_start, win_end in windows:
            if win_end < det_time and win_end > prev_window_end:
                prev_window_end = win_end

    # Calculate final score
    total_score = fp_score + sum(window_best_score.values())

    # Count TP, FP, FN
    tp = sum(1 for score in window_best_score.values() if score > -cost_matrix.fn_weight)
    fn = sum(1 for score in window_best_score.values() if score <= -cost_matrix.fn_weight)
    fp = sum(1 for matched in det_matched if matched and det_matched[det_matched.index(matched)])
    fp = len([d for d in det_times if d >= probation_length]) - tp  # Simplified FP count
    tn = 0  # NAB doesn't explicitly count TN

    return {
        'nab_score': total_score,
        'nab_score_raw': total_score,
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'tn': tn
    }
