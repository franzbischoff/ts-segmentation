from __future__ import annotations
from typing import Dict, Any

from skmultiflow.drift_detection import PageHinkley, ADWIN, DDM, EDDM, KSWIN, HDDM_A, HDDM_W


class DriftDetectorWrapper:
    """Unified wrapper returning a simple interface.

    Methods:
      add_element(value) -> bool: returns True if change detected at this new value.
    """
    def __init__(self, detector, name: str):
        self.detector = detector
        self.name = name

    def add_element(self, value: float) -> bool:
        self.detector.add_element(value)
        if hasattr(self.detector, 'detected_change'):
            return bool(self.detector.detected_change())
        # PageHinkley uses detected_change() method as well
        return False


def build_detector(name: str, **kwargs) -> DriftDetectorWrapper:
    name_lower = name.lower()
    if name_lower in {"page_hinkley", "ph"}:
        delta = kwargs.get('delta', 0.005)
        lam = kwargs.get('lambda_', 50)  # PageHinkley param is 'lambda_' in lib
        alpha = kwargs.get('alpha', 1 - 0.9999)
        detector = PageHinkley(delta=delta, threshold=lam, alpha=alpha)
        return DriftDetectorWrapper(detector, 'page_hinkley')
    if name_lower in {"adwin"}:
        delta = kwargs.get('delta', 0.002)
        detector = ADWIN(delta=delta)
        return DriftDetectorWrapper(detector, 'adwin')
    if name_lower in {"ddm"}:
        detector = DDM()
        return DriftDetectorWrapper(detector, 'ddm')
    if name_lower in {"eddm"}:
        detector = EDDM()
        return DriftDetectorWrapper(detector, 'eddm')
    if name_lower in {"kswin"}:
        alpha = kwargs.get('alpha', 0.005)
        window_size = kwargs.get('window_size', 100)
        stat_size = kwargs.get('stat_size', 30)
        detector = KSWIN(alpha=alpha, window_size=window_size, stat_size=stat_size)
        return DriftDetectorWrapper(detector, 'kswin')
    if name_lower in {"hddm_a", "hddm-a"}:
        drift_confidence = kwargs.get('drift_confidence', 0.001)
        warning_confidence = kwargs.get('warning_confidence', 0.005)
        two_side_option = kwargs.get('two_side_option', True)
        detector = HDDM_A(drift_confidence=drift_confidence,
                         warning_confidence=warning_confidence,
                         two_side_option=two_side_option)
        return DriftDetectorWrapper(detector, 'hddm_a')
    if name_lower in {"hddm_w", "hddm-w"}:
        drift_confidence = kwargs.get('drift_confidence', 0.001)
        warning_confidence = kwargs.get('warning_confidence', 0.005)
        lambda_option = kwargs.get('lambda_option', 0.05)
        two_side_option = kwargs.get('two_side_option', True)
        detector = HDDM_W(drift_confidence=drift_confidence,
                         warning_confidence=warning_confidence,
                         lambda_option=lambda_option,
                         two_side_option=two_side_option)
        return DriftDetectorWrapper(detector, 'hddm_w')
    raise ValueError(f"Detector '{name}' não suportado.")
