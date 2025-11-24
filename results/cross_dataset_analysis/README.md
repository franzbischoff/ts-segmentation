# Cross-Dataset Analysis: Final Report

**Date**: 2025-11-24
**Datasets**: `afib_paroxysmal` (229 files), `malignantventricular` (22 files), `vtachyarrhythmias` (34 files)
**Detectors**: ADWIN, Page-Hinkley, KSWIN, HDDM_A, HDDM_W, FLOSS

---

## 🚨 Executive Summary: The "Specialist Loophole"

Our analysis revealed a critical distinction between aggregation methods:

1.  **File-Weighted (Micro-Average)**: Heavily biased towards the largest dataset (`afib_paroxysmal` = 80% weight).
2.  **True Macro-Average**: Gives equal weight (1/3) to each dataset.

**Critical Finding**: The current True Macro-Average calculation allows a **"Specialist Loophole"**.
- Detectors like **ADWIN** and **Page-Hinkley** achieve high "Macro" scores by performing well on *one* dataset and failing (returning NaN) on the others.
- **FLOSS** and **KSWIN** are **True Generalists** (100% coverage across all datasets).

---

## 🏆 Final Rankings

### 1. True Generalists (Recommended)
*Detectors that perform consistently across ALL datasets (100% coverage).*

| Rank | Detector | Macro Score | File-Weighted | Robustness (Std) | Status |
|------|----------|-------------|---------------|------------------|--------|
| **1** 🥇 | **FLOSS** | **0.3958** | **0.4491** | 0.0972 | ✅ **Champion** |
| **2** 🥈 | **KSWIN** | **0.2976** | 0.3773 | 0.1015 | ✅ Very Robust |
| **3** 🥉 | **HDDM_A** | **0.2584** | 0.3273 | **0.0593** | ✅ Most Stable |
| 4 | HDDM_W | 0.1252 | 0.2843 | 0.1552 | ❌ Poor Performance |

### 2. Specialists (Use with Caution)
*Detectors where top configurations appear in only 1 dataset (Specialist Loophole).*

| Detector | Macro Score (n=1) | Real Generalist Score (n=3) | Drop |
|----------|-------------------|-----------------------------|------|
| **Page-Hinkley** | 0.3885 | 0.2625 | -32% |
| **ADWIN** | 0.3408 | 0.2835 | -17% |

> **Note**: While ADWIN and Page-Hinkley *can* generalize (they have configs with n=3), their performance drops significantly when forced to do so. Their "top" ranking in some metrics is an artifact of overfitting to the easiest dataset.

---

## 📊 Detailed Analysis by Detector

### 🥇 FLOSS (The Universal Choice)
- **Performance**: #1 in BOTH File-Weighted and True Macro rankings.
- **Coverage**: 100% (25,920/25,920 configs work on all datasets).
- **Best Config**: `window=125`, `thresh=0.55`, `landmark=5.0`, `gap=1000`.
- **Recommendation**: **Use for Production**.

### 🥈 KSWIN (The Reliable Alternative)
- **Performance**: Solid #2 among generalists.
- **Coverage**: 100% (1,280/1,280 configs).
- **Best Config**: `alpha=0.01`, `window=500`, `stat=20`, `ma=100`.
- **Recommendation**: Good alternative if FLOSS is too computationally expensive.

### 🥉 HDDM_A (The Stability King)
- **Performance**: Lower average score, but **lowest standard deviation** (0.059).
- **Coverage**: 100%.
- **Recommendation**: Use when consistency is more important than peak sensitivity.

### ⚠️ ADWIN & Page-Hinkley (The Specialists)
- **Behavior**: Top configurations are highly tuned to `afib_paroxysmal`.
- **Risk**: High risk of failure on different data distributions (e.g., `vtachyarrhythmias`).
- **Recommendation**: Avoid for general-purpose pipelines unless retrained/tuned per dataset.

---

## 💡 Key Technical Insights

1.  **Universal Parameter**: `min_gap_samples = 1000` (4 seconds) is optimal for ALL detectors across ALL datasets.
2.  **Aggregation Matters**: "File-Weighted" hides poor performance on small datasets. "True Macro" exposes it (if coverage is checked).
3.  **Matrix Profile vs. Drift**: FLOSS (Matrix Profile) significantly outperforms traditional Drift Detection (ADWIN/PH/HDDM) on this ECG segmentation task.

---

## 📁 Directory Structure

- `file_weighted_rankings.csv`: Micro-average results (biased to afib).
- `true_macro_average_rankings.csv`: Macro-average results (equal weight).
- `ANALYSIS_RANKING_DISCREPANCIES.md`: Detailed report on the "Specialist Loophole".
- `AGGREGATION_METHODS_COMPARISON.md`: Methodology comparison.
