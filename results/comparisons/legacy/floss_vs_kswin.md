# Comparative Analysis: Change Point Detectors

**Date**: 2025-11-17
**Detectors**: floss, kswin

---

## 📊 Executive Summary

### 🏆 Winner by Category

| Category | Winner | Score | Advantage |
|----------|--------|-------|-----------|
| **Overall Performance (F3*)** | 🥇 **KSWIN** | 0.4135 | +15.4% vs FLOSS |
| **Detection Rate (Recall@10s)** | 🥇 **KSWIN** | 99.44% | +67.9% vs FLOSS |
| **Precision (Precision@10s)** | 🥇 **FLOSS** | 20.98% | +95.4% vs KSWIN |
| **Low False Alarms (FP/min)** | 🥇 **FLOSS** | 2.32 | 4.1× fewer than KSWIN |
| **NAB Standard Score** | 🥇 **FLOSS** | -3.07 | +41.6% vs KSWIN |
| **Detection Speed (EDD)** | 🥇 **FLOSS** | 2.66s | 8.0% faster than KSWIN |

### 🎯 Key Findings

**KSWIN Strengths:**
- ✅ **Superior detection rate**: Captures 99.44% of regime changes within 10s
- ✅ **Best F3* score**: 0.4135 (primary metric for recall-oriented tasks)
- ✅ **Robust performance**: Median F3* = 0.2323 across all configs

**FLOSS Strengths:**
- ✅ **Lower false alarm rate**: 2.32 FP/min (vs 9.43 for KSWIN)
- ✅ **Better precision**: 20.98% (vs 10.74% for KSWIN)
- ✅ **More consistent**: Lower variability in NAB scores (σ=8.6 vs 39.8)
- ✅ **Slightly faster**: 2.66s median detection delay

**Trade-offs:**
- ⚖️ **KSWIN**: High recall but noisy (many false positives)
- ⚖️ **FLOSS**: More selective but misses more events

### 💡 Recommendations

| Use Case | Recommended Detector | Configuration |
|----------|---------------------|---------------|
| **Clinical monitoring** (can't miss events) | KSWIN | ma=50, gap=1000 |
| **Automated alerts** (minimize false alarms) | FLOSS | gap=200 (default) |
| **Research/Analysis** (balanced) | KSWIN | ma=10, gap=2000 |
| **Real-time systems** (low latency) | FLOSS | gap=200 |

---

## 1. Best Configurations by Metric

Comparison of optimal parameter settings for each metric:

| metric       | floss                              | kswin                                |
|:-------------|:-----------------------------------|:-------------------------------------|
| f3_weighted  | 0.3582 (δ=N/A, ma=N/A, gap=200.0)  | 0.4135 (δ=N/A, ma=50.0, gap=1000.0)  |
| f3_classic   | 0.4299 (δ=N/A, ma=N/A, gap=200.0)  | 0.4948 (δ=N/A, ma=10.0, gap=2000.0)  |
| f1_weighted  | 0.2410 (δ=N/A, ma=N/A, gap=200.0)  | 0.1700 (δ=N/A, ma=1.0, gap=2000.0)   |
| f1_classic   | 0.2830 (δ=N/A, ma=N/A, gap=200.0)  | 0.2261 (δ=N/A, ma=10.0, gap=2000.0)  |
| nab_standard | -3.0741 (δ=N/A, ma=N/A, gap=200.0) | -5.2573 (δ=N/A, ma=50.0, gap=3000.0) |
| nab_low_fp   | -4.3115 (δ=N/A, ma=N/A, gap=200.0) | -5.6812 (δ=N/A, ma=1.0, gap=500.0)   |
| nab_low_fn   | -4.6250 (δ=N/A, ma=N/A, gap=200.0) | -3.4979 (δ=N/A, ma=10.0, gap=2000.0) |

## 2. Detector Rankings

Detectors ranked by performance on key metrics:

| metric        | rank_1          | rank_2          |
|:--------------|:----------------|:----------------|
| F3-Weighted   | kswin (0.4135)  | floss (0.3582)  |
| NAB Standard  | floss (-3.0741) | kswin (-5.2573) |
| Recall@10s    | kswin (0.9944)  | floss (0.5921)  |
| Precision@10s | floss (0.2098)  | kswin (0.1074)  |
| FP/min        | floss (2.3219)  | kswin (9.4279)  |
| EDD Median    | floss (2.6599)  | kswin (2.8931)  |

## 3. Statistical Comparison

Mean ± Std (Median) across all parameter combinations:

| metric             |   floss_mean |   floss_std |   floss_median |   kswin_mean |   kswin_std |   kswin_median |
|:-------------------|-------------:|------------:|---------------:|-------------:|------------:|---------------:|
| f3_weighted        |       0.112  |      0.1759 |         0      |       0.2511 |      0.2154 |         0.2323 |
| f1_weighted        |       0.0764 |      0.1343 |         0      |       0.1111 |      0.1267 |         0.073  |
| recall_10s         |       0.1998 |      0.2888 |         0      |       0.6631 |      0.4034 |         1      |
| precision_10s      |       0.0916 |      0.1787 |         0      |       0.0941 |      0.1257 |         0.0513 |
| fp_per_min         |       1.4367 |      1.5851 |         0.7123 |       7.3934 |      7.4557 |         4.7282 |
| edd_median_s       |       3.76   |      2.8511 |         3.28   |       3.7528 |      2.3752 |         3.314  |
| nab_score_standard |      -5.6706 |      8.6276 |        -3.22   |      -9.5235 |     39.7876 |        -3.21   |

## 4. Recommendations

### For Maximum Recall (Don't miss events)
- **Primary**: Best F3-weighted configuration
- **Alternative**: Best NAB Low FN configuration

### For Minimum False Positives (Reduce alarms)
- **Primary**: Best NAB Low FP configuration
- **Consider**: Higher min_gap_samples values

### For Balanced Performance
- **Primary**: Pareto-optimal solutions
- **Metric**: NAB Standard or F3-weighted

### For Ensemble Methods
Combine detectors using:
- **Voting**: Majority vote (2/3 or 3/5)
- **Weighted**: Weight by F3-weighted score
- **Cascade**: Fast detector → Precise detector

---

## Appendix: Interpretation Guide

**Metrics**:
- F3-weighted: Emphasizes recall with temporal weighting (primary metric)
- NAB Standard: Balanced anomaly detection score
- NAB Low FP: Penalizes false positives 2×
- NAB Low FN: Penalizes false negatives 2×
- Recall@10s: % events detected within 10 seconds
- FP/min: False positive rate
- EDD: Expected detection delay (median)

**Parameters**:
- δ (delta): Detector sensitivity threshold
- ma (ma_window): Moving average window size
- gap (min_gap_samples): Minimum spacing between detections

