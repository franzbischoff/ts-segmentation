# Two-Fold Cross-Validation Analysis Summary

Generated: 2026-05-12T19:06:10.622220

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
| floss | 0.4306 | 0.0214 | ✅ Excellent |
| hddm_w | 0.1534 | 0.0215 | ✅ Excellent |
| adwin | 0.2890 | 0.0432 | ✅ Excellent |
| kswin | 0.3203 | 0.0448 | ✅ Excellent |
| hddm_a | 0.3022 | 0.0472 | ✅ Excellent |
| page_hinkley | 0.3152 | 0.0527 | ⚠️  Good |

---

## Per-Dataset Analysis

### afib_paroxysmal

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | floss | 0.4790 | 0.4794 | 0.0004 | fold_b |
| 2 | kswin | 0.4326 | 0.3942 | 0.0384 | fold_b |
| 3 | adwin | 0.4231 | 0.3774 | 0.0457 | fold_b |
| 4 | page_hinkley | 0.4107 | 0.3656 | 0.0451 | fold_b |
| 5 | hddm_w | 0.3790 | 0.3294 | 0.0496 | fold_b |
| 6 | hddm_a | 0.3742 | 0.3464 | 0.0278 | fold_b |

### malignantventricular

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | kswin | 0.3115 | 0.2278 | 0.0837 | fold_a |
| 2 | hddm_a | 0.3052 | 0.2143 | 0.0909 | fold_a |
| 3 | floss | 0.2810 | 0.3253 | 0.0443 | fold_b |
| 4 | page_hinkley | 0.2775 | 0.2189 | 0.0586 | fold_a |
| 5 | adwin | 0.2451 | 0.2392 | 0.0059 | fold_a |
| 6 | hddm_w | 0.0618 | 0.0503 | 0.0115 | fold_b |

### vtachyarrhythmias

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |
|------|----------|---------------|---------------|-----|---------------|
| 1 | floss | 0.5317 | 0.5513 | 0.0196 | fold_a |
| 2 | page_hinkley | 0.2573 | 0.2028 | 0.0545 | fold_b |
| 3 | hddm_a | 0.2271 | 0.2041 | 0.0230 | fold_b |
| 4 | kswin | 0.2168 | 0.2290 | 0.0122 | fold_b |
| 5 | adwin | 0.1989 | 0.2769 | 0.0780 | fold_a |
| 6 | hddm_w | 0.0194 | 0.0161 | 0.0033 | fold_b |

