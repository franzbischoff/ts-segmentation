# Unified Robustness Score (Option 3)

Generated: 2026-05-12T20:06:21.999926

## Executive Summary

This analysis combines both dimensions from Options 1 and 2 into a single **unified robustness metric**:

$$\text{Robustness Score} = 0.6 \times (1 - \text{2-fold gap}) + 0.4 \times (1 - \text{transfer variance})$$

**Score Range**: 0 to 1 (higher = more robust)

### Final Ranking

| Rank | Detector | Unified Score | Intra-Consistency | Inter-Generalization | Ceiling Cross-Fold F3-weighted | Transfer CV |
|------|----------|---------------|-------------------|----------------------|------------|------------|
| 1 | **floss** | 0.9761 | 0.9786 | 0.9723 | 0.4306 | 21.9% |
| 2 | **adwin** | 0.9710 | 0.9568 | 0.9923 | 0.2890 | 9.2% |
| 3 | **kswin** | 0.9690 | 0.9552 | 0.9898 | 0.3203 | 11.5% |
| 4 | **hddm_a** | 0.9507 | 0.9528 | 0.9476 | 0.3022 | 35.2% |
| 5 | **hddm_w** | 0.9425 | 0.9785 | 0.8884 | 0.1534 | 73.0% |
| 6 | **page_hinkley** | 0.9047 | 0.9473 | 0.8408 | 0.3152 | 73.5% |

---

## Detailed Analysis

### Top 3 Recommendations


**🥇 #1: floss**
- **Unified Score**: 0.9761
- **Intra-Dataset Consistency**: 0.9786 (stable across folds)
- **Inter-Dataset Generalization**: 0.9723 (stable across datasets)
- **Ceiling Performance (cross-fold F3-weighted)**: 0.4306
- **Transfer Variability**: 21.9% (CV across transfers)


**🥈 #2: adwin**
- **Unified Score**: 0.9710
- **Intra-Dataset Consistency**: 0.9568 (stable across folds)
- **Inter-Dataset Generalization**: 0.9923 (stable across datasets)
- **Ceiling Performance (cross-fold F3-weighted)**: 0.2890
- **Transfer Variability**: 9.2% (CV across transfers)


**🥉 #3: kswin**
- **Unified Score**: 0.9690
- **Intra-Dataset Consistency**: 0.9552 (stable across folds)
- **Inter-Dataset Generalization**: 0.9898 (stable across datasets)
- **Ceiling Performance (cross-fold F3-weighted)**: 0.3203
- **Transfer Variability**: 11.5% (CV across transfers)


---

## Interpretation Guide

### What Each Component Measures

**Intra-Dataset Consistency** (Weight 0.6):
- Measures stability between folds within the same dataset
- High value (≥0.95) = detector parameters are stable across data splits
- Low value (<0.70) = detector highly sensitive to training data distribution
- **Interpretation**: How much can you trust parameters to generalize to new data from same source?

**Inter-Dataset Generalization** (Weight 0.4):
- Measures stability of parameter transfers across different datasets
- High value (≥0.80) = detector works reliably across dataset types
- Low value (<0.50) = detector requires re-tuning for new datasets
- **Interpretation**: How portable are the parameters to new domains?

### Why These Weights?

- **0.6 for Intra**: Dominant weight because consistent parameters within domain are foundational
- **0.4 for Inter**: Secondary weight because transfer is less critical than baseline reliability

---

## Production Guidance by Score Range

- **🟢 Excellent** (0.85 - 1.0): Production-ready, minimal validation needed
- **🟡 Good** (0.75 - 0.84): Production-viable with standard validation
- **🟠 Acceptable** (0.60 - 0.74): Production-viable with enhanced monitoring
- **🔴 Poor** (0.0 - 0.59): Research use only, re-tuning required

---

## Comparison with Option 1 and Option 2

| Metric | Option 1 | Option 2 | Option 3 |
|--------|----------|----------|----------|
| **Focus** | Ceiling performance with local tuning | Parameter transfer across datasets | Combined robustness |
| **Best For** | Research, max performance | Production deployment | Holistic detector selection |
| **Questions Answered** | What's the best we can do if we retune? | Can we use params without retuning? | Which detector is most reliable overall? |
| **Winner Typically** | FLOSS (performance focused) | ADWIN (robustness focused) | FLOSS (highest unified score) |

---

## Dataset-Level Summary

This unified score is computed from macro-averages across all three datasets:
- **afib_paroxysmal**: Largest dataset (229 files)
- **malignantventricular**: Medium dataset (22 files)
- **vtachyarrhythmias**: Smallest dataset (34 files)

Detectors performing well on small datasets (vtachy) and hard datasets (malign) get higher robustness scores because they demonstrate consistency despite domain challenges.

---

## Recommendations

### For Research/Benchmarking
- **Use FLOSS** (Option 1: cross-fold F3-weighted ceiling=0.4306)
- Accept the tuning cost, get maximum performance

### For Production Deployment
- **Use detector ranked #1 in Option 3** (unified score)
- Provides best balance of ceiling + portability + stability

### For Heterogeneous Data
- **Ensemble approach**: Top 2 detectors from Option 3
- Voting or weighted combination improves overall reliability

### For Extreme Resource Constraints
- **Use ADWIN** (excellent portability, zero re-tuning cost)
- Accept lower ceiling for maximum convenience

---

## Technical Notes

- Variance normalization uses min-max scaling to 0-1 range
- Weights (0.6 / 0.4) are tunable but balanced towards practical deployment
- All metrics computed from aggregated results (no per-file recomputation)
- Score is deterministic and reproducible
