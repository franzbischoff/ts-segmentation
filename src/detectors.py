from __future__ import annotations
from typing import Dict, Any

from skmultiflow.drift_detection import PageHinkley, ADWIN, DDM


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
    raise ValueError(f"Detector '{name}' não suportado.")
