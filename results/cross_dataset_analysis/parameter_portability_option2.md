# Parameter Portability Analysis (Option 2)

Generated: 2026-05-12T20:06:02.319269

## Executive Summary

This analysis tests **hyperparameter portability** by transferring the best parameters from one dataset to others, measuring real-world generalization.

### Methodology

1. Extract best hyperparameters from source dataset (from 2-fold CV)
2. Apply those exact parameters to target dataset (filter metrics_comprehensive_with_nab.csv)
3. Calculate cross-fold F3-weighted performance with transferred parameters
4. Compare with target's local best (optimized independently)
5. Compute transferability ratio = transferred_f3 / local_best_f3

**Interpretation**:
- Ratio ≥ 0.95 (≥95%): ✅ Excellent transfer (params are portable)
- Ratio ≥ 0.85 (≥85%): ✅ Good transfer
- Ratio ≥ 0.75 (≥75%): ⚠️  Acceptable transfer
- Ratio ≥ 0.60 (≥60%): ⚠️  Moderate transfer (consider re-tuning)
- Ratio < 0.60 (<60%): ❌ Poor transfer (re-tuning required)

---

## Summary by Detector

### ADWIN

**Overall Portability**:
- Average transferability ratio: **95.07%**
- Average performance drop: 0.0194 (4.8% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 2/6
  - ✅ Good (≥85%): 3/6
  - ⚠️  Acceptable (≥75%): 1/6
  - ⚠️  Moderate (≥60%): 0/6
  - ❌ Poor (<60%): 0/6

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| afib_p → malign | 0.2582 | 0.2451 | 105.34% | -0.0131 | ✅ Excellent transfer |
| afib_p → vtachy | 0.1857 | 0.1989 | 93.35% | 0.0132 | ✅ Good transfer |
| malign → afib_p | 0.3706 | 0.4231 | 87.59% | 0.0525 | ✅ Good transfer |
| malign → vtachy | 0.1872 | 0.1989 | 94.14% | 0.0117 | ✅ Good transfer |
| vtachy → afib_p | 0.3575 | 0.4231 | 84.49% | 0.0656 | ⚠️  Acceptable transfer |
| vtachy → malign | 0.2587 | 0.2451 | 105.53% | -0.0136 | ✅ Excellent transfer |

### FLOSS

**Overall Portability**:
- Average transferability ratio: **75.83%**
- Average performance drop: 0.1107 (27.7% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 2/6
  - ✅ Good (≥85%): 0/6
  - ⚠️  Acceptable (≥75%): 0/6
  - ⚠️  Moderate (≥60%): 3/6
  - ❌ Poor (<60%): 1/6

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| afib_p → malign | 0.2748 | 0.2810 | 97.81% | 0.0062 | ✅ Excellent transfer |
| afib_p → vtachy | 0.3642 | 0.5317 | 68.50% | 0.1675 | ⚠️  Moderate transfer |
| malign → afib_p | 0.4595 | 0.4790 | 95.93% | 0.0195 | ✅ Excellent transfer |
| malign → vtachy | 0.3397 | 0.5317 | 63.88% | 0.1920 | ⚠️  Moderate transfer |
| vtachy → afib_p | 0.2872 | 0.4790 | 59.96% | 0.1918 | ❌ Poor transfer |
| vtachy → malign | 0.1936 | 0.2810 | 68.90% | 0.0874 | ⚠️  Moderate transfer |

### HDDM_A

**Overall Portability**:
- Average transferability ratio: **64.99%**
- Average performance drop: 0.1173 (29.3% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 0/6
  - ✅ Good (≥85%): 1/6
  - ⚠️  Acceptable (≥75%): 2/6
  - ⚠️  Moderate (≥60%): 1/6
  - ❌ Poor (<60%): 2/6

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| afib_p → malign | 0.2394 | 0.3052 | 78.45% | 0.0658 | ⚠️  Acceptable transfer |
| afib_p → vtachy | 0.1731 | 0.2271 | 76.24% | 0.0540 | ⚠️  Acceptable transfer |
| malign → afib_p | 0.1394 | 0.3742 | 37.24% | 0.2348 | ❌ Poor transfer |
| malign → vtachy | 0.2142 | 0.2271 | 94.32% | 0.0129 | ✅ Good transfer |
| vtachy → afib_p | 0.1456 | 0.3742 | 38.92% | 0.2286 | ❌ Poor transfer |
| vtachy → malign | 0.1977 | 0.3052 | 64.79% | 0.1075 | ⚠️  Moderate transfer |

### HDDM_W

**Overall Portability**:
- Average transferability ratio: **45.76%**
- Average performance drop: 0.0625 (15.6% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 0/6
  - ✅ Good (≥85%): 1/6
  - ⚠️  Acceptable (≥75%): 0/6
  - ⚠️  Moderate (≥60%): 1/6
  - ❌ Poor (<60%): 4/6

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| afib_p → malign | 0.0079 | 0.0618 | 12.80% | 0.0539 | ❌ Poor transfer |
| afib_p → vtachy | 0.0000 | 0.0194 | 0.00% | 0.0194 | ❌ Poor transfer |
| malign → afib_p | 0.2667 | 0.3790 | 70.37% | 0.1123 | ⚠️  Moderate transfer |
| malign → vtachy | 0.0166 | 0.0194 | 85.79% | 0.0028 | ✅ Good transfer |
| vtachy → afib_p | 0.2258 | 0.3790 | 59.57% | 0.1532 | ❌ Poor transfer |
| vtachy → malign | 0.0285 | 0.0618 | 46.04% | 0.0333 | ❌ Poor transfer |

### KSWIN

**Overall Portability**:
- Average transferability ratio: **87.75%**
- Average performance drop: 0.0453 (11.3% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 2/6
  - ✅ Good (≥85%): 2/6
  - ⚠️  Acceptable (≥75%): 2/6
  - ⚠️  Moderate (≥60%): 0/6
  - ❌ Poor (<60%): 0/6

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| afib_p → malign | 0.2665 | 0.3115 | 85.56% | 0.0450 | ✅ Good transfer |
| afib_p → vtachy | 0.2112 | 0.2168 | 97.42% | 0.0056 | ✅ Excellent transfer |
| malign → afib_p | 0.3763 | 0.4326 | 86.98% | 0.0563 | ✅ Good transfer |
| malign → vtachy | 0.2206 | 0.2168 | 101.73% | -0.0038 | ✅ Excellent transfer |
| vtachy → afib_p | 0.3340 | 0.4326 | 77.22% | 0.0986 | ⚠️  Acceptable transfer |
| vtachy → malign | 0.2416 | 0.3115 | 77.56% | 0.0699 | ⚠️  Acceptable transfer |

### PAGE_HINKLEY

**Overall Portability**:
- Average transferability ratio: **54.32%**
- Average performance drop: 0.1784 (44.6% relative)
- Transfer quality distribution:
  - ✅ Excellent (≥95%): 0/4
  - ✅ Good (≥85%): 2/4
  - ⚠️  Acceptable (≥75%): 0/4
  - ⚠️  Moderate (≥60%): 0/4
  - ❌ Poor (<60%): 2/4

**Transfer Matrix**:

| Source → Target | Transferred Cross-Fold F3-weighted | Local Best Cross-Fold F3-weighted | Ratio | Drop | Status |
|-----------------|----------------|---------------|-------|------|--------|
| malign → afib_p | 0.0265 | 0.4107 | 6.44% | 0.3842 | ❌ Poor transfer |
| malign → vtachy | 0.2235 | 0.2573 | 86.86% | 0.0338 | ✅ Good transfer |
| vtachy → afib_p | 0.1496 | 0.4107 | 36.43% | 0.2611 | ❌ Poor transfer |
| vtachy → malign | 0.2430 | 0.2775 | 87.56% | 0.0345 | ✅ Good transfer |

---

## Best Source Datasets for Transfer

Which dataset's parameters transfer best to others?

### afib_paroxysmal
- Average transferability to other datasets: **71.55%**
- Number of transfers tested: 10

### malignantventricular
- Average transferability to other datasets: **75.94%**
- Number of transfers tested: 12

### vtachyarrhythmias
- Average transferability to other datasets: **67.25%**
- Number of transfers tested: 12

---

## Recommendations for Production

### Best Overall Portability: ADWIN
- Average transferability: 95.07%
- This detector's parameters transfer best across different ECG datasets
- **Recommendation**: Safe to use parameters from any dataset on new data

### Use Cases

**ADWIN**: ✅ Portable (avg 95.07%)
  - Can use parameters from training dataset on production data
  - Minimal re-tuning needed

**KSWIN**: ✅ Portable (avg 87.75%)
  - Can use parameters from training dataset on production data
  - Minimal re-tuning needed

**FLOSS**: ⚠️  Moderately portable (avg 75.83%)
  - Consider validation on small sample before full deployment
  - May benefit from light re-tuning

**HDDM_A**: ❌ Limited portability (avg 64.99%)
  - Re-tuning strongly recommended for new datasets
  - Use with caution in production without validation

**PAGE_HINKLEY**: ❌ Limited portability (avg 54.32%)
  - Re-tuning strongly recommended for new datasets
  - Use with caution in production without validation

**HDDM_W**: ❌ Limited portability (avg 45.76%)
  - Re-tuning strongly recommended for new datasets
  - Use with caution in production without validation

