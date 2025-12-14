# Cross-Dataset Generalization Analysis (Option 1)

Generated: 2025-12-14T21:22:47.559156

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
| 🥇 | floss | 0.4285 | 0.4768 | 0.1323 | 0.2788 | 0.5299 | 30.9% | 0.0211 |
| 🥈 | kswin | 0.3176 | 0.3080 | 0.1085 | 0.2142 | 0.4305 | 34.2% | 0.0442 |
| 🥉 | page_hinkley | 0.3132 | 0.2737 | 0.0845 | 0.2557 | 0.4103 | 27.0% | 0.0516 |
| 4 | hddm_a | 0.2997 | 0.3019 | 0.0739 | 0.2248 | 0.3725 | 24.6% | 0.0460 |
| 5 | adwin | 0.2879 | 0.2435 | 0.1185 | 0.1980 | 0.4221 | 41.1% | 0.0424 |
| 6 | hddm_w | 0.1527 | 0.0617 | 0.1955 | 0.0193 | 0.3772 | 128.0% | 0.0212 |

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
| 1 | hddm_a | 24.6% | Good |
| 2 | page_hinkley | 27.0% | Good |
| 3 | floss | 30.9% | Moderate |
| 4 | kswin | 34.2% | Moderate |
| 5 | adwin | 41.1% | Variable |
| 6 | hddm_w | 128.0% | Variable |

---

## Detailed Breakdown by Detector

### ADWIN

**Summary Statistics**:
- Mean Cross-Fold F3: **0.2879**
- Median: 0.2435
- Std Dev: 0.1185
- Range: [0.1980, 0.4221]
- CV%: 41.1%
- Avg Generalization Gap: 0.0424

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4221 | 0.3768 | 0.0453 |
| malignantventricular | 0.2435 | 0.2389 | 0.0046 |
| vtachyarrhythmias | 0.1980 | 0.2753 | 0.0773 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4221)
- Weakest on: vtachyarrhythmias (F3=0.1980)
- Performance variation: 53.1% between best and worst dataset

### FLOSS

**Summary Statistics**:
- Mean Cross-Fold F3: **0.4285**
- Median: 0.4768
- Std Dev: 0.1323
- Range: [0.2788, 0.5299]
- CV%: 30.9%
- Avg Generalization Gap: 0.0211

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4768 | 0.4770 | 0.0002 |
| malignantventricular | 0.2788 | 0.3234 | 0.0446 |
| vtachyarrhythmias | 0.5299 | 0.5483 | 0.0184 |

**Insights**:
- Best on: **vtachyarrhythmias** (F3=0.5299)
- Weakest on: malignantventricular (F3=0.2788)
- Performance variation: 47.4% between best and worst dataset

### HDDM_A

**Summary Statistics**:
- Mean Cross-Fold F3: **0.2997**
- Median: 0.3019
- Std Dev: 0.0739
- Range: [0.2248, 0.3725]
- CV%: 24.6%
- Avg Generalization Gap: 0.0460

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.3725 | 0.3451 | 0.0274 |
| malignantventricular | 0.3019 | 0.2129 | 0.0890 |
| vtachyarrhythmias | 0.2248 | 0.2032 | 0.0216 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.3725)
- Weakest on: vtachyarrhythmias (F3=0.2248)
- Performance variation: 39.7% between best and worst dataset

### HDDM_W

**Summary Statistics**:
- Mean Cross-Fold F3: **0.1527**
- Median: 0.0617
- Std Dev: 0.1955
- Range: [0.0193, 0.3772]
- CV%: 128.0%
- Avg Generalization Gap: 0.0212

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.3772 | 0.3282 | 0.0490 |
| malignantventricular | 0.0617 | 0.0503 | 0.0114 |
| vtachyarrhythmias | 0.0193 | 0.0161 | 0.0032 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.3772)
- Weakest on: vtachyarrhythmias (F3=0.0193)
- Performance variation: 94.9% between best and worst dataset

### KSWIN

**Summary Statistics**:
- Mean Cross-Fold F3: **0.3176**
- Median: 0.3080
- Std Dev: 0.1085
- Range: [0.2142, 0.4305]
- CV%: 34.2%
- Avg Generalization Gap: 0.0442

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4305 | 0.3929 | 0.0376 |
| malignantventricular | 0.3080 | 0.2266 | 0.0814 |
| vtachyarrhythmias | 0.2142 | 0.2278 | 0.0136 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4305)
- Weakest on: vtachyarrhythmias (F3=0.2142)
- Performance variation: 50.2% between best and worst dataset

### PAGE_HINKLEY

**Summary Statistics**:
- Mean Cross-Fold F3: **0.3132**
- Median: 0.2737
- Std Dev: 0.0845
- Range: [0.2557, 0.4103]
- CV%: 27.0%
- Avg Generalization Gap: 0.0516

**Per-Dataset Performance**:

| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |
|---------|---------------|---------------|-----|
| afib_paroxysmal | 0.4103 | 0.3654 | 0.0449 |
| malignantventricular | 0.2737 | 0.2177 | 0.0560 |
| vtachyarrhythmias | 0.2557 | 0.2019 | 0.0538 |

**Insights**:
- Best on: **afib_paroxysmal** (F3=0.4103)
- Weakest on: vtachyarrhythmias (F3=0.2557)
- Performance variation: 37.7% between best and worst dataset

---

## Key Findings

1. **Highest Average Performance**: FLOSS (mean F3=0.4285)
   - This detector achieves the best performance when properly tuned per dataset

2. **Most Consistent**: HDDM_A (CV=24.6%)
   - This detector shows most stable performance across different datasets

3. **Trade-off**: Best performance (floss) vs best consistency (hddm_a)

4. **Best Generalization**: FLOSS (avg gap=0.0211)
   - Smallest average gap between intra-fold and cross-fold scores

---

## Recommendations

### When to Use Each Detector

**FLOSS**:
- ✅ **Recommended**: Excellent average performance (F3=0.4285)
- ⚠️  Variable across datasets (CV=30.9%)
- Best use case: vtachyarrhythmias

**KSWIN**:
- ⚠️  Good option: Solid performance (F3=0.3176)
- ⚠️  Variable across datasets (CV=34.2%)
- Best use case: afib_paroxysmal

**PAGE_HINKLEY**:
- ⚠️  Good option: Solid performance (F3=0.3132)
- ⚠️  Variable across datasets (CV=27.0%)
- Best use case: afib_paroxysmal

**HDDM_A**:
- 🔻 Consider alternatives: Lower performance (F3=0.2997)
- ✅ Consistent across datasets (CV=24.6%)
- Best use case: afib_paroxysmal

**ADWIN**:
- 🔻 Consider alternatives: Lower performance (F3=0.2879)
- ⚠️  Variable across datasets (CV=41.1%)
- Best use case: afib_paroxysmal

**HDDM_W**:
- 🔻 Consider alternatives: Lower performance (F3=0.1527)
- ⚠️  Variable across datasets (CV=128.0%)
- Best use case: afib_paroxysmal

---

## Methodology Notes

1. **Cross-Fold F3**: Performance on opposite fold from 2-fold cross-validation
2. **Independent Tuning**: Each detector was optimized separately per dataset
3. **No Parameter Transfer**: This analysis does NOT test portability
4. **Represents Ceiling**: Shows best achievable with proper tuning

**Next Steps**: See Option 2 analysis for parameter portability testing.

