# Cross-Dataset Generalization Analysis (Option 1)

Generated: 2026-05-12T19:06:10.629019

## Executive Summary

This analysis shows the **performance ceiling** of each detector when properly tuned per dataset, using **cross-fold F3 scores** (generalization metric from 2-fold validation).

### Key Concept

- Each detector was optimized **independently** on each dataset (using 2-fold CV)
- We use the **cross-fold F3 score** (performance on opposite fold) as the metric
- Cross-fold scores are more realistic than intra-fold (test on unseen data)
- This shows: **"What's the best each detector can do when properly tuned?"**

**Different from Option 2**: This does NOT test parameter portability. Each dataset uses its own best parameters.

---

## Overall Ranking (by Mean Cross-Fold F3)

| Rank | Detector | Mean F3 | Median F3 | Std Dev | Min | Max | CV% | Avg Gap |
|------|----------|---------|-----------|---------|-----|-----|-----|----------|
| 🥇 | floss | 0.4306 | 0.4790 | 0.1322 | 0.2810 | 0.5317 | 30.7% | 0.0214 |
| 🥈 | kswin | 0.3203 | 0.3115 | 0.1082 | 0.2168 | 0.4326 | 33.8% | 0.0448 |
| 🥉 | page_hinkley | 0.3152 | 0.2775 | 0.0833 | 0.2573 | 0.4107 | 26.4% | 0.0527 |
| 4 | hddm_a | 0.3022 | 0.3052 | 0.0736 | 0.2271 | 0.3742 | 24.4% | 0.0472 |
| 5 | adwin | 0.2890 | 0.2451 | 0.1184 | 0.1989 | 0.4231 | 41.0% | 0.0432 |
| 6 | hddm_w | 0.1534 | 0.0618 | 0.1965 | 0.0194 | 0.3790 | 128.1% | 0.0215 |

**Interpretation**:
- **Mean F3**: Average performance ceiling across 3 datasets (higher = better)
- **Std Dev**: Consistency across datasets (lower = more stable)
- **CV%**: Coefficient of variation (lower = more reliable)
- **Avg Gap**: Average generalization gap from 2-fold (lower = more robust)

---

## Consistency Analysis

### By Coefficient of Variation (CV%)

Lower CV% = more consistent performance across different datasets

| Rank | Detector | CV% | Interpretation |
|------|----------|-----|----------------|
| 1 | hddm_a | 24.4% | Good |
| 2 | page_hinkley | 26.4% | Good |
| 3 | floss | 30.7% | Moderate |
| 4 | kswin | 33.8% | Moderate |
| 5 | adwin | 41.0% | Variable |
| 6 | hddm_w | 128.1% | Variable |

---

## Detailed Breakdown by Detector

### ADWIN

**Summary Statistics**:
- Mean Cross-Fold F3: **0.2890**
- Median: 0.2451
- Std Dev: 0.1184
- Range: [0.1989, 0.4231]
- CV%: 41.0%
- Avg Generalization Gap: 0.0432

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4231 | 0.3774 | 0.0457 |
| malignantventricular | 0.2451 | 0.2392 | 0.0059 |
| vtachyarrhythmias | 0.1989 | 0.2769 | 0.0780 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4231)
- Weakest on: vtachyarrhythmias (F3=0.1989)
- Performance variation: 53.0% between best and worst dataset

### FLOSS

**Summary Statistics**:
- Mean Cross-Fold F3: **0.4306**
- Median: 0.4790
- Std Dev: 0.1322
- Range: [0.2810, 0.5317]
- CV%: 30.7%
- Avg Generalization Gap: 0.0214

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4790 | 0.4794 | 0.0004 |
| malignantventricular | 0.2810 | 0.3253 | 0.0443 |
| vtachyarrhythmias | 0.5317 | 0.5513 | 0.0196 |

**Insights**:
- Best on: **vtachyarrhythmias** (F3=0.5317)
- Weakest on: malignantventricular (F3=0.2810)
- Performance variation: 47.2% between best and worst dataset

### HDDM_A

**Summary Statistics**:
- Mean Cross-Fold F3: **0.3022**
- Median: 0.3052
- Std Dev: 0.0736
- Range: [0.2271, 0.3742]
- CV%: 24.4%
- Avg Generalization Gap: 0.0472

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.3742 | 0.3464 | 0.0278 |
| malignantventricular | 0.3052 | 0.2143 | 0.0909 |
| vtachyarrhythmias | 0.2271 | 0.2041 | 0.0230 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.3742)
- Weakest on: vtachyarrhythmias (F3=0.2271)
- Performance variation: 39.3% between best and worst dataset

### HDDM_W

**Summary Statistics**:
- Mean Cross-Fold F3: **0.1534**
- Median: 0.0618
- Std Dev: 0.1965
- Range: [0.0194, 0.3790]
- CV%: 128.1%
- Avg Generalization Gap: 0.0215

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.3790 | 0.3294 | 0.0496 |
| malignantventricular | 0.0618 | 0.0503 | 0.0115 |
| vtachyarrhythmias | 0.0194 | 0.0161 | 0.0033 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.3790)
- Weakest on: vtachyarrhythmias (F3=0.0194)
- Performance variation: 94.9% between best and worst dataset

### KSWIN

**Summary Statistics**:
- Mean Cross-Fold F3: **0.3203**
- Median: 0.3115
- Std Dev: 0.1082
- Range: [0.2168, 0.4326]
- CV%: 33.8%
- Avg Generalization Gap: 0.0448

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4326 | 0.3942 | 0.0384 |
| malignantventricular | 0.3115 | 0.2278 | 0.0837 |
| vtachyarrhythmias | 0.2168 | 0.2290 | 0.0122 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4326)
- Weakest on: vtachyarrhythmias (F3=0.2168)
- Performance variation: 49.9% between best and worst dataset

### PAGE_HINKLEY

**Summary Statistics**:
- Mean Cross-Fold F3: **0.3152**
- Median: 0.2775
- Std Dev: 0.0833
- Range: [0.2573, 0.4107]
- CV%: 26.4%
- Avg Generalization Gap: 0.0527

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4107 | 0.3656 | 0.0451 |
| malignantventricular | 0.2775 | 0.2189 | 0.0586 |
| vtachyarrhythmias | 0.2573 | 0.2028 | 0.0545 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4107)
- Weakest on: vtachyarrhythmias (F3=0.2573)
- Performance variation: 37.4% between best and worst dataset

---

## Key Findings

1. **Highest Average Performance**: FLOSS (mean F3=0.4306)
   - This detector achieves the best performance when properly tuned per dataset

2. **Most Consistent**: HDDM_A (CV=24.4%)
   - This detector shows most stable performance across different datasets

3. **Trade-off**: Best performance (floss) vs best consistency (hddm_a)

4. **Best Generalization**: FLOSS (avg gap=0.0214)
   - Smallest average gap between intra-fold and cross-fold scores

---

## Recommendations

### When to Use Each Detector

**FLOSS**:
- ✅ **Recommended**: Excellent average performance (F3=0.4306)
- ⚠️  Variable across datasets (CV=30.7%)
- Best use case: vtachyarrhythmias

**KSWIN**:
- ⚠️  Good option: Solid performance (F3=0.3203)
- ⚠️  Variable across datasets (CV=33.8%)
- Best use case: afib_paroxysmal

**PAGE_HINKLEY**:
- ⚠️  Good option: Solid performance (F3=0.3152)
- ⚠️  Variable across datasets (CV=26.4%)
- Best use case: afib_paroxysmal

**HDDM_A**:
- ⚠️  Good option: Solid performance (F3=0.3022)
- ✅ Consistent across datasets (CV=24.4%)
- Best use case: afib_paroxysmal

**ADWIN**:
- 🔻 Consider alternatives: Lower performance (F3=0.2890)
- ⚠️  Variable across datasets (CV=41.0%)
- Best use case: afib_paroxysmal

**HDDM_W**:
- 🔻 Consider alternatives: Lower performance (F3=0.1534)
- ⚠️  Variable across datasets (CV=128.1%)
- Best use case: afib_paroxysmal

---

## Methodology Notes

1. **Cross-Fold F3**: Performance on opposite fold from 2-fold cross-validation
2. **Independent Tuning**: Each detector was optimized separately per dataset
3. **No Parameter Transfer**: This analysis does NOT test portability
4. **Represents Ceiling**: Shows best achievable with proper tuning

**Next Steps**: See Option 2 analysis for parameter portability testing.

