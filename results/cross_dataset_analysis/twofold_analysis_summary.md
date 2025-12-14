# Two-Fold Cross-Validation Analysis Summary

Generated: 2025-12-14T19:26:57.204324

## Executive Summary

This analysis evaluates detector robustness by measuring how well hyperparameters
optimized in one data fold generalize to the opposite fold.

### Selection Methodology

For each detector×dataset:
1. Train on Fold A, evaluate on Fold A and Fold B → get cross-fold score A→B
2. Train on Fold B, evaluate on Fold B and Fold A → get cross-fold score B→A
3. **Select the fold with HIGHEST cross-fold score** (best generalization)
4. If tied, select the fold with **SMALLEST generalization gap**

---

## Robustness Ranking

| Detector | Avg Cross-Fold F3 | Avg Gap | Robustness |
|----------|-------------------|---------|------------|
| floss | 0.4285 | 0.0211 | ✅ Excellent |
| hddm_w | 0.1527 | 0.0212 | ✅ Excellent |
| adwin | 0.2879 | 0.0424 | ✅ Excellent |
| kswin | 0.3176 | 0.0442 | ✅ Excellent |
| hddm_a | 0.2997 | 0.0460 | ✅ Excellent |
| page_hinkley | 0.3132 | 0.0516 | ⚠️  Good |

---

## Per-Dataset Analysis

### afib_paroxysmal

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | floss | 0.4768 | 0.4770 | 0.0002 | fold_b |
| 2 | kswin | 0.4305 | 0.3929 | 0.0376 | fold_b |
| 3 | adwin | 0.4221 | 0.3768 | 0.0453 | fold_b |
| 4 | page_hinkley | 0.4103 | 0.3654 | 0.0449 | fold_b |
| 5 | hddm_w | 0.3772 | 0.3282 | 0.0490 | fold_b |
| 6 | hddm_a | 0.3725 | 0.3451 | 0.0274 | fold_b |

### malignantventricular

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | kswin | 0.3080 | 0.2266 | 0.0814 | fold_a |
| 2 | hddm_a | 0.3019 | 0.2129 | 0.0890 | fold_a |
| 3 | floss | 0.2788 | 0.3234 | 0.0446 | fold_b |
| 4 | page_hinkley | 0.2737 | 0.2177 | 0.0560 | fold_a |
| 5 | adwin | 0.2435 | 0.2389 | 0.0046 | fold_a |
| 6 | hddm_w | 0.0617 | 0.0503 | 0.0114 | fold_b |

### vtachyarrhythmias

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | floss | 0.5299 | 0.5483 | 0.0184 | fold_a |
| 2 | page_hinkley | 0.2557 | 0.2019 | 0.0538 | fold_b |
| 3 | hddm_a | 0.2248 | 0.2032 | 0.0216 | fold_b |
| 4 | kswin | 0.2142 | 0.2278 | 0.0136 | fold_b |
| 5 | adwin | 0.1980 | 0.2753 | 0.0773 | fold_a |
| 6 | hddm_w | 0.0193 | 0.0161 | 0.0032 | fold_b |

