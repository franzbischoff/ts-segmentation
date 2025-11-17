# Comparative Analysis: Change Point Detectors

**Date**: 2025-11-13
**Detectors**: adwin, page_hinkley, kswin, hddm_a, hddm_w

---

## 1. Best Configurations by Metric

Comparison of optimal parameter settings for each metric:

| metric       | adwin                                  | page_hinkley                            | kswin                                | hddm_a                            | hddm_w                            |
|:-------------|:---------------------------------------|:----------------------------------------|:-------------------------------------|:----------------------------------|:----------------------------------|
| f3_weighted  | 0.3994 (δ=0.005, ma=300.0, gap=1000.0) | 0.3885 (δ=0.04, ma=50.0, gap=1000.0)    | 0.4135 (δ=N/A, ma=50.0, gap=1000.0)  | 0.3588 (δ=N/A, ma=1, gap=1000)    | 0.3530 (δ=N/A, ma=1, gap=1000)    |
| f3_classic   | 0.4882 (δ=0.1, ma=300.0, gap=2000.0)   | 0.4770 (δ=0.02, ma=10.0, gap=2000.0)    | 0.4948 (δ=N/A, ma=10.0, gap=2000.0)  | 0.4379 (δ=N/A, ma=1, gap=2000)    | 0.4187 (δ=N/A, ma=1, gap=2000)    |
| f1_weighted  | 0.1682 (δ=0.005, ma=10.0, gap=1000.0)  | 0.1626 (δ=0.001, ma=50.0, gap=2000.0)   | 0.1700 (δ=N/A, ma=1.0, gap=2000.0)   | 0.1593 (δ=N/A, ma=1, gap=2000)    | 0.1771 (δ=N/A, ma=1, gap=2000)    |
| f1_classic   | 0.2239 (δ=0.015, ma=300.0, gap=2000.0) | 0.2168 (δ=0.04, ma=50.0, gap=2000.0)    | 0.2261 (δ=N/A, ma=10.0, gap=2000.0)  | 0.2147 (δ=N/A, ma=1, gap=2000)    | 0.2254 (δ=N/A, ma=1, gap=2000)    |
| nab_standard | -4.2820 (δ=0.05, ma=10.0, gap=2000.0)  | -5.2182 (δ=0.02, ma=50.0, gap=4000.0)   | -5.2573 (δ=N/A, ma=50.0, gap=3000.0) | -5.1989 (δ=N/A, ma=1, gap=3000)   | -4.4566 (δ=N/A, ma=1, gap=3000)   |
| nab_low_fp   | -7.0183 (δ=0.005, ma=10.0, gap=5000.0) | -5.7889 (δ=0.005, ma=200.0, gap=4000.0) | -5.6812 (δ=N/A, ma=1.0, gap=500.0)   | -6.9956 (δ=N/A, ma=100, gap=5000) | -6.0791 (δ=N/A, ma=100, gap=5000) |
| nab_low_fn   | -3.3841 (δ=0.08, ma=100.0, gap=2000.0) | -3.7376 (δ=0.001, ma=10.0, gap=2000.0)  | -3.4979 (δ=N/A, ma=10.0, gap=2000.0) | -4.3235 (δ=N/A, ma=1, gap=2000)   | -4.1400 (δ=N/A, ma=1, gap=2000)   |

## 2. Detector Rankings

Detectors ranked by performance on key metrics:

| metric        | rank_1          | rank_2           | rank_3                | rank_4                 | rank_5          |
|:--------------|:----------------|:-----------------|:----------------------|:-----------------------|:----------------|
| F3-Weighted   | kswin (0.4135)  | adwin (0.3994)   | page_hinkley (0.3885) | hddm_a (0.3588)        | hddm_w (0.3530) |
| NAB Standard  | adwin (-4.2820) | hddm_w (-4.4566) | hddm_a (-5.1989)      | page_hinkley (-5.2182) | kswin (-5.2573) |
| Recall@10s    | kswin (0.9944)  | adwin (0.9777)   | page_hinkley (0.9540) | hddm_a (0.8878)        | hddm_w (0.8165) |
| Precision@10s | hddm_a (0.1136) | kswin (0.1074)   | adwin (0.1020)        | page_hinkley (0.1002)  | hddm_w (0.0987) |
| FP/min        | hddm_w (8.0671) | hddm_a (9.1468)  | kswin (9.4279)        | page_hinkley (9.7266)  | adwin (10.0009) |
| EDD Median    | hddm_w (2.6266) | adwin (2.6366)   | page_hinkley (2.8280) | hddm_a (2.8506)        | kswin (2.8931)  |

## 3. Statistical Comparison

Mean ± Std (Median) across all parameter combinations:

| metric             |   adwin_mean |   adwin_std |   adwin_median |   page_hinkley_mean |   page_hinkley_std |   page_hinkley_median |   kswin_mean |   kswin_std |   kswin_median |   hddm_a_mean |   hddm_a_std |   hddm_a_median |   hddm_w_mean |   hddm_w_std |   hddm_w_median |
|:-------------------|-------------:|------------:|---------------:|--------------------:|-------------------:|----------------------:|-------------:|------------:|---------------:|--------------:|-------------:|----------------:|--------------:|-------------:|----------------:|
| f3_weighted        |       0.293  |      0.1965 |         0.2703 |              0.1714 |             0.1979 |                0.1086 |       0.2511 |      0.2154 |         0.2323 |        0.2012 |       0.1848 |          0.1803 |        0.1845 |       0.1994 |          0.1414 |
| f1_weighted        |       0.139  |      0.1288 |         0.1026 |              0.0944 |             0.1278 |                0.0469 |       0.1111 |      0.1267 |         0.073  |        0.111  |       0.1207 |          0.0784 |        0.1058 |       0.1339 |          0.0588 |
| recall_10s         |       0.7206 |      0.3111 |         0.8333 |              0.3821 |             0.3874 |                0.3333 |       0.6631 |      0.4034 |         1      |        0.4596 |       0.3665 |          0.5    |        0.3991 |       0.3816 |          0.3333 |
| precision_10s      |       0.1258 |      0.1368 |         0.0778 |              0.1052 |             0.1671 |                0.0385 |       0.0941 |      0.1257 |         0.0513 |        0.1236 |       0.1624 |          0.0658 |        0.1163 |       0.1656 |          0.05   |
| fp_per_min         |       6.7161 |      5.5151 |         4.4129 |              3.2901 |             4.4615 |                1.9544 |       7.3934 |      7.4557 |         4.7282 |        3.8478 |       4.2019 |          2.5501 |        2.9315 |       3.5684 |          1.9475 |
| edd_median_s       |       4.0709 |      2.4342 |         3.82   |              4.2445 |             2.4554 |                4.11   |       3.7528 |      2.3752 |         3.314  |        4.3004 |       2.4842 |          4.192  |        4.3732 |       2.4863 |          4.31   |
| nab_score_standard |      -6.8066 |     19.3313 |        -2.99   |             -6.6646 |            20.1877 |               -3.1928 |      -9.5235 |     39.7876 |        -3.21   |       -6.7139 |      17.7674 |         -3.1366 |       -5.8339 |      18.2349 |         -2.8773 |

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

