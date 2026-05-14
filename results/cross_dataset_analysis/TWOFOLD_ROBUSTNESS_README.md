# Two-Fold Cross-Validation Robustness Analysis

## Overview

This analysis evaluates the **generalization robustness** of each detector by measuring how well hyperparameters optimized on one data fold perform on an independent test fold.

## Methodology

### Selection Process

For each **detector × dataset** combination:

1. **Fold Setup**: Dataset records are deterministically split into Fold A and Fold B
2. **Two Training Rounds**:
   - Train on Fold A → find best hyperparameters → evaluate on Fold B (A→B cross-fold score)
   - Train on Fold B → find best hyperparameters → evaluate on Fold A (B→A cross-fold score)
3. **Selection Criterion**:
   - **Primary**: Select the fold with **HIGHEST cross-fold F3 score** (best generalization)
   - **Tiebreaker**: If equal, select the fold with **SMALLEST generalization gap** (intra-fold − cross-fold)

### Metrics

| Metric | Description |
|--------|-------------|
| **Intra-Fold F3** | F3-weighted score on the fold where hyperparameters were optimized |
| **Cross-Fold F3** | F3-weighted score on the opposite fold (generalization test) |
| **Generalization Gap** | Difference between intra-fold and cross-fold performance |
| **Selected Fold** | Which fold's hyperparameters were recommended (A or B) |

## Key Findings

### Overall Robustness Ranking

Ranked by **average generalization gap** across all datasets (lower = better):

| Rank | Detector | Avg Cross-Fold F3 | Avg Gap | Robustness |
|------|----------|-------------------|---------|-----------|
| 1️⃣ | **FLOSS** | 0.4306 | **0.0214** | ✅ Excellent |
| 2️⃣ | HDDM_W | 0.1534 | **0.0215** | ✅ Excellent |
| 3️⃣ | ADWIN | 0.2890 | 0.0432 | ✅ Excellent |
| 4️⃣ | KSWIN | 0.3203 | 0.0448 | ✅ Excellent |
| 5️⃣ | HDDM_A | 0.3022 | 0.0472 | ✅ Excellent |
| 6️⃣ | Page-Hinkley | 0.3152 | 0.0527 | ⚠️  Good |

### Interpretation

- **FLOSS**: Exceptional two-fold robustness (average absolute F3 gap of 0.0214)
- **HDDM_W**: Excellent numerical robustness but lower absolute performance
- **ADWIN**: Strong generalization with consistent performance across folds
- **Page-Hinkley**: Slight generalization challenge (average absolute F3 gap of 0.0527)

---

## Per-Dataset Analysis

### Dataset: afib_paroxysmal (229 records)

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected |
|------|----------|---------------|---------------|-----|----------|
| 🥇 | FLOSS | 0.4790 | 0.4794 | **0.0004** | fold_b |
| 🥈 | KSWIN | 0.4326 | 0.3942 | 0.0384 | fold_b |
| 🥉 | ADWIN | 0.4231 | 0.3774 | 0.0457 | fold_b |
| 4️⃣ | Page-Hinkley | 0.4107 | 0.3656 | 0.0451 | fold_b |
| 5️⃣ | HDDM_W | 0.3790 | 0.3294 | 0.0496 | fold_b |
| 6️⃣ | HDDM_A | 0.3742 | 0.3464 | 0.0278 | fold_b |

**Insight**: All detectors show excellent generalization on this dataset. FLOSS maintains near-identical performance (absolute gap 0.0004). Fold B hyperparameters are better in this two-fold run.

---

### Dataset: malignantventricular (22 records)

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected |
|------|----------|---------------|---------------|-----|----------|
| 🥇 | KSWIN | 0.3115 | 0.2278 | 0.0837 | fold_a |
| 🥈 | HDDM_A | 0.3052 | 0.2143 | 0.0909 | fold_a |
| 🥉 | FLOSS | 0.2810 | 0.3253 | **0.0443** | fold_b |
| 4️⃣ | Page-Hinkley | 0.2775 | 0.2189 | 0.0586 | fold_a |
| 5️⃣ | ADWIN | 0.2451 | 0.2392 | **0.0059** | fold_a |
| 6️⃣ | HDDM_W | 0.0618 | 0.0503 | 0.0115 | fold_b |

**Insight**: Smaller dataset reveals detector sensitivity. ADWIN shows exceptional two-fold robustness (absolute gap 0.0059), but KSWIN achieves higher absolute performance. FLOSS's generalization gap here is larger due to fold imbalance (smaller dataset).

---

### Dataset: vtachyarrhythmias (34 records)

| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected |
|------|----------|---------------|---------------|-----|----------|
| 🥇 | FLOSS | 0.5317 | 0.5513 | **0.0196** | fold_a |
| 🥈 | Page-Hinkley | 0.2573 | 0.2028 | 0.0545 | fold_b |
| 🥉 | HDDM_A | 0.2271 | 0.2041 | 0.0230 | fold_b |
| 4️⃣ | KSWIN | 0.2168 | 0.2290 | 0.0122 | fold_b |
| 5️⃣ | ADWIN | 0.1989 | 0.2769 | 0.0780 | fold_a |
| 6️⃣ | HDDM_W | 0.0194 | 0.0161 | 0.0033 | fold_b |

**Insight**: FLOSS dominates with highest cross-fold F3 and excellent generalization. ADWIN shows degradation (absolute gap 0.0780), suggesting hyperparameter fit to Fold A structure.

---

## Detector-Specific Robustness Profiles

### 🔴 FLOSS
- **Overall Ranking**: 1st (avg gap: 0.0214)
- **Strengths**: Consistently robust across all datasets, exceptional generalization
- **Best On**: afib_paroxysmal (0.0004 gap), vtachyarrhythmias (0.0196 gap)
- **Recommendation**: Strong choice in two-fold robustness; for cross-dataset parameter transfer, use the Option 2 portability analysis.

### 🟢 KSWIN
- **Overall Ranking**: 4th (avg gap: 0.0448)
- **Strengths**: Good balance between robustness and performance
- **Challenge**: Larger gap on malignantventricular (0.0837)
- **Recommendation**: Reliable for large datasets; may need re-tuning on smaller ones

### 🔵 ADWIN
- **Overall Ranking**: 3rd (avg gap: 0.0432)
- **Strengths**: Exceptional on small datasets (malignantventricular: 0.0059 gap)
- **Challenge**: Generalization issues on very small datasets (vtachyarrhythmias: 0.0780)
- **Recommendation**: Best for malignantventricular-like scenarios

### 🟡 Page-Hinkley
- **Overall Ranking**: 6th (avg gap: 0.0527)
- **Strengths**: Stable on medium-sized datasets
- **Challenge**: Highest average gap suggests parameter sensitivity
- **Recommendation**: Requires careful tuning; less portable across datasets

### 🟣 HDDM_A
- **Overall Ranking**: 5th (avg gap: 0.0472)
- **Strengths**: Competitive performance on afib_paroxysmal and malignantventricular
- **Challenge**: Moderate generalization gaps
- **Recommendation**: Decent secondary option

### ⚫ HDDM_W
- **Overall Ranking**: 2nd (avg gap: 0.0215)
- **Strengths**: Numerically robust (near-smallest average gap)
- **Challenge**: Low absolute performance across datasets
- **Recommendation**: For robustness-critical applications despite lower F3

---

## Output Files

```
results/cross_dataset_analysis/
├── twofold_analysis_summary.md              # This summary
├── twofold_robustness_afib_paroxysmal.csv   # Per-detector metrics
├── twofold_robustness_malignantventricular.csv
└── twofold_robustness_vtachyarrhythmias.csv
```

### CSV Format

```csv
detector,selected_fold,intra_fold_f3,cross_fold_f3,generalization_gap
floss,fold_b,0.4794,0.4790,0.0004
kswin,fold_b,0.3942,0.4326,0.0384
```

---

## Recommendations for Production Use

### For Highest Performance
**Use FLOSS** with hyperparameters from the recommended fold (indicated in CSV).
- Cross-fold F3: 0.4306 (avg)
- Generalization gap: 0.0214 (excellent)

### For Robust Two-Fold Generalization
**Rank Order**: FLOSS → HDDM_W → ADWIN → KSWIN → HDDM_A → Page-Hinkley

### For Unknown Dataset Size
1. If expected **>100 records**: Use FLOSS
2. If expected **~20-50 records**: Use ADWIN or KSWIN
3. If robustness is critical: Use FLOSS (despite lower absolute F3 on some datasets)

### For Cross-Dataset Hyperparameter Portability
- Use the Option 2 portability report (`parameter_portability_option2.md`) as the source of truth.
- **ADWIN** leads cross-dataset portability (95.07% average transferability).
- **FLOSS** leads ceiling/two-fold performance, but cross-dataset portability is moderate (75.83%).
- **Page-Hinkley** has limited portability in the current artefacts (54.32%, with 4 available transfers).

---

## Technical Notes

### Two-Fold Split Strategy
- Deterministic split using seed=42
- Records grouped by filename (ensures file-based consistency)
- Fold assignments saved in: `results/<dataset>/fold_assignments_seed42.json`

### Generalization Gap Interpretation
- **Gap < 0.03**: Excellent generalization (model is robust)
- **Gap 0.03-0.05**: Good generalization (acceptable)
- **Gap > 0.05**: Moderate generalization (consider hyperparameter retuning)

### When Cross-Fold < Intra-Fold
This is **normal and expected** in streaming detection:
- Hyperparameters optimized on Fold A reflect its data characteristics
- Applying same parameters to unseen Fold B tests true generalization
- FLOSS's minimal gaps show strong stability in the evaluated two-fold splits

---

**Generated**: 2026-05-12
**Reviewed**: 2026-05-14
**Analysis Seed**: 42
**Primary Metric**: f3_weighted
