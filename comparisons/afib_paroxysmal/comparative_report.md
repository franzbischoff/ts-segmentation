# Comparative Analysis: Change Point Detectors

**Date**: 2025-11-13
**Detectors**: adwin, page_hinkley, kswin, hddm_a, hddm_w, floss

---

## 1. Best Configurations by Metric

Comparison of optimal parameter settings for each metric:

| metric             | adwin                              | page_hinkley                                      | kswin                                                | hddm_a                                                                                               | hddm_w                                                                                                      | floss                                              |
|:-------------------|:-----------------------------------|:--------------------------------------------------|:-----------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:---------------------------------------------------|
| f3_weighted        | 0.3994 (δ=0.005, ma=300, gap=1000) | 0.3885 (λ=1, δ=0.04, α=0.9999, ma=50, gap=1000)   | 0.4135 (α=0.005, win=500, stat=50, ma=50, gap=1000)  | 0.3588 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma=1, gap=1000)      | 0.3530 (drift_confidence=0.005, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=1000)     | 0.3109 (win=25, reg_th=0.9, reg_lm=2, gap=200)     |
| f1_weighted        | 0.1682 (δ=0.005, ma=10, gap=1000)  | 0.1626 (λ=1, δ=0.001, α=0.9999, ma=50, gap=2000)  | 0.1700 (α=0.005, win=500, stat=100, ma=1, gap=2000)  | 0.1593 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma=1, gap=2000)      | 0.1771 (drift_confidence=0.001, warning_confidence=0.001, λ=0.1, two_side_option=False, ma=1, gap=2000)     | 0.1934 (win=25, reg_th=0.75, reg_lm=2.5, gap=200)  |
| nab_score_standard | -4.2820 (δ=0.05, ma=10, gap=2000)  | -5.2182 (λ=1, δ=0.02, α=0.9999, ma=50, gap=4000)  | -5.2573 (α=0.005, win=200, stat=20, ma=50, gap=3000) | -5.1989 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=False, ma=1, gap=3000)    | -4.4566 (drift_confidence=0.005, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=3000)    | -4.0775 (win=25, reg_th=0.75, reg_lm=2.5, gap=200) |
| nab_score_low_fp   | -7.0183 (δ=0.005, ma=10, gap=5000) | -5.7889 (λ=80, δ=0.005, α=0.99, ma=200, gap=4000) | -5.6812 (α=0.001, win=50, stat=50, ma=1, gap=500)    | -6.9956 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=100, gap=5000) | -6.0791 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=100, gap=5000) | -5.3072 (win=25, reg_th=0.65, reg_lm=2, gap=5000)  |
| nab_score_low_fn   | -3.3841 (δ=0.08, ma=100, gap=2000) | -3.7376 (λ=1, δ=0.001, α=0.9999, ma=10, gap=2000) | -3.4979 (α=0.01, win=500, stat=50, ma=10, gap=2000)  | -4.3235 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma=1, gap=2000)     | -4.1400 (drift_confidence=0.005, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=2000)    | -5.8571 (win=25, reg_th=0.85, reg_lm=2, gap=200)   |
| recall_10s         | 0.9952 (δ=0.1, ma=250, gap=500)    | 0.9995 (λ=1, δ=0.001, α=0.99, ma=10, gap=500)     | 1.0000 (α=0.001, win=100, stat=50, ma=100, gap=500)  | 0.9058 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma=1, gap=500)       | 0.8254 (drift_confidence=0.005, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=500)      | 0.7075 (win=275, reg_th=0.9, reg_lm=2.5, gap=200)  |
| precision_10s      | 0.1636 (δ=0.005, ma=10, gap=3000)  | 0.1614 (λ=30, δ=0.005, α=0.9999, ma=10, gap=2000) | 0.1543 (α=0.01, win=500, stat=50, ma=10, gap=5000)   | 0.1628 (drift_confidence=0.0005, warning_confidence=0.001, two_side_option=True, ma=1, gap=3000)     | 0.1763 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=5000)    | 0.2350 (win=25, reg_th=0.65, reg_lm=2, gap=5000)   |
| fp_per_min         | 2.0089 (δ=0.005, ma=10, gap=5000)  | 0.1211 (λ=80, δ=0.04, α=0.99, ma=200, gap=4000)   | 0.0000 (α=0.001, win=50, stat=50, ma=1, gap=500)     | 1.2292 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=100, gap=5000)  | 0.6305 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=100, gap=5000)  | 0.2559 (win=25, reg_th=0.2, reg_lm=4, gap=200)     |
| edd_median_s       | 1.2944 (δ=0.1, ma=250, gap=500)    | 1.2617 (λ=1, δ=0.005, α=0.9999, ma=10, gap=500)   | 0.9525 (α=0.05, win=200, stat=100, ma=1, gap=500)    | 2.0157 (drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma=1, gap=500)       | 1.6686 (drift_confidence=0.005, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=1, gap=500)      | 0.0280 (win=150, reg_th=0.05, reg_lm=5, gap=200)   |

## 2. Detector Rankings

Detectors ranked by performance on key metrics:

| metric        | rank_1          | rank_2          | rank_3                | rank_4           | rank_5                 | rank_6          |
|:--------------|:----------------|:----------------|:----------------------|:-----------------|:-----------------------|:----------------|
| F3-Weighted   | kswin (0.4135)  | adwin (0.3994)  | page_hinkley (0.3885) | hddm_a (0.3588)  | hddm_w (0.3530)        | floss (0.3109)  |
| NAB Standard  | floss (-4.0775) | adwin (-4.2820) | hddm_w (-4.4566)      | hddm_a (-5.1989) | page_hinkley (-5.2182) | kswin (-5.2573) |
| Recall@10s    | kswin (0.9944)  | adwin (0.9777)  | page_hinkley (0.9540) | hddm_a (0.8878)  | hddm_w (0.8165)        | floss (0.5374)  |
| Precision@10s | floss (0.1764)  | hddm_a (0.1136) | kswin (0.1074)        | adwin (0.1020)   | page_hinkley (0.1002)  | hddm_w (0.0987) |
| FP/min        | floss (2.8002)  | hddm_w (8.0671) | hddm_a (9.1468)       | kswin (9.4279)   | page_hinkley (9.7266)  | adwin (10.0009) |
| EDD Median    | hddm_w (2.6266) | adwin (2.6366)  | page_hinkley (2.8280) | hddm_a (2.8506)  | kswin (2.8931)         | floss (3.0225)  |

## 3. Performance & Robustness Analysis

Analysis of peak performance and parameter sensitivity.

**Note**: Robustness and Top-N summaries are computed using the best-performing parameter configurations only
(by default the top 10 configurations), rather than averaging across the full grid. This avoids bias from
large grids that include many poor parameter choices. You can change the Top-N or use a top-percent selection
when running the script (see --robust-top-n / --robust-top-percent).

- **Best**: The single highest score achieved.
- **Top-10 Mean**: Average of the top 10 configurations (indicates stability of the peak).
- **Param Tolerance**: Geometric mean of the normalized valid range for each parameter. Indicates how much you can vary parameters (0% to 100% of tested range) while maintaining >90% performance.

| Metric        | Detector     |    Best |   Top-10 Mean | Param Tolerance (%)   |   Total Configs |
|:--------------|:-------------|--------:|--------------:|:----------------------|----------------:|
| F3-Weighted   | adwin        |  0.3994 |        0.3984 | 60.6%                 |             594 |
| F3-Weighted   | page_hinkley |  0.3885 |        0.3875 | 50.4%                 |             600 |
| F3-Weighted   | kswin        |  0.4135 |        0.4129 | 74.0%                 |            1280 |
| F3-Weighted   | hddm_a       |  0.3588 |        0.3502 | 2.1%                  |             640 |
| F3-Weighted   | hddm_w       |  0.353  |        0.3529 | 46.6%                 |            2560 |
| F3-Weighted   | floss        |  0.3109 |        0.3033 | 11.2%                 |           25920 |
| F1-Weighted   | adwin        |  0.1682 |        0.1665 | 76.3%                 |             594 |
| F1-Weighted   | page_hinkley |  0.1626 |        0.1601 | 69.1%                 |             600 |
| F1-Weighted   | kswin        |  0.17   |        0.1687 | 74.0%                 |            1280 |
| F1-Weighted   | hddm_a       |  0.1593 |        0.1582 | 36.9%                 |             640 |
| F1-Weighted   | hddm_w       |  0.1771 |        0.1755 | 2.8%                  |            2560 |
| F1-Weighted   | floss        |  0.1934 |        0.186  | 11.2%                 |           25920 |
| NAB Standard  | adwin        | -4.282  |       -4.3246 | 41.0%                 |             594 |
| NAB Standard  | page_hinkley | -5.2182 |       -5.2536 | 100.0%                |             600 |
| NAB Standard  | kswin        | -5.2573 |       -5.2844 | 100.0%                |            1280 |
| NAB Standard  | hddm_a       | -5.1989 |       -5.2102 | 90.4%                 |             640 |
| NAB Standard  | hddm_w       | -4.4566 |       -4.4717 | 80.1%                 |            2560 |
| NAB Standard  | floss        | -4.0775 |       -4.1813 | 12.7%                 |           25920 |
| NAB Low FP    | adwin        | -7.0183 |       -7.1097 | 51.7%                 |             594 |
| NAB Low FP    | page_hinkley | -5.7889 |       -5.8007 | 5.8%                  |             600 |
| NAB Low FP    | kswin        | -5.6812 |       -5.6812 | 58.7%                 |            1280 |
| NAB Low FP    | hddm_a       | -6.9956 |       -7.047  | 79.7%                 |             640 |
| NAB Low FP    | hddm_w       | -6.0791 |       -6.0984 | 93.6%                 |            2560 |
| NAB Low FP    | floss        | -5.3072 |       -5.3883 | 100.0%                |           25920 |
| NAB Low FN    | adwin        | -3.3841 |       -3.4959 | 1.0%                  |             594 |
| NAB Low FN    | page_hinkley | -3.7376 |       -3.7934 | 0.3%                  |             600 |
| NAB Low FN    | kswin        | -3.4979 |       -3.5436 | 6.3%                  |            1280 |
| NAB Low FN    | hddm_a       | -4.3235 |       -4.561  | 0.0%                  |             640 |
| NAB Low FN    | hddm_w       | -4.14   |       -4.1704 | 0.0%                  |            2560 |
| NAB Low FN    | floss        | -5.8571 |       -6.0748 | 18.2%                 |           25920 |
| Recall@10s    | adwin        |  0.9952 |        0.9902 | 68.1%                 |             594 |
| Recall@10s    | page_hinkley |  0.9995 |        0.9988 | 54.7%                 |             600 |
| Recall@10s    | kswin        |  1      |        1      | 80.3%                 |            1280 |
| Recall@10s    | hddm_a       |  0.9058 |        0.8913 | 0.1%                  |             640 |
| Recall@10s    | hddm_w       |  0.8254 |        0.8245 | 36.5%                 |            2560 |
| Recall@10s    | floss        |  0.7075 |        0.6944 | 20.7%                 |           25920 |
| Precision@10s | adwin        |  0.1636 |        0.1595 | 87.4%                 |             594 |
| Precision@10s | page_hinkley |  0.1614 |        0.1506 | 88.1%                 |             600 |
| Precision@10s | kswin        |  0.1543 |        0.1514 | 92.2%                 |            1280 |
| Precision@10s | hddm_a       |  0.1628 |        0.162  | 2.9%                  |             640 |
| Precision@10s | hddm_w       |  0.1763 |        0.176  | 5.8%                  |            2560 |
| Precision@10s | floss        |  0.235  |        0.2282 | 1.4%                  |           25920 |
| FP/min        | adwin        |  2.0089 |        2.0873 | 0.0%                  |             594 |
| FP/min        | page_hinkley |  0.1211 |        0.1308 | 0.0%                  |             600 |
| FP/min        | kswin        |  0      |        0      | 58.7%                 |            1280 |
| FP/min        | hddm_a       |  1.2292 |        1.2647 | 1.7%                  |             640 |
| FP/min        | hddm_w       |  0.6305 |        0.6409 | 0.2%                  |            2560 |
| FP/min        | floss        |  0.2559 |        0.2564 | 100.0%                |           25920 |
| EDD Median    | adwin        |  1.2944 |        1.3338 | 0.9%                  |             594 |
| EDD Median    | page_hinkley |  1.2617 |        1.292  | 0.0%                  |             600 |
| EDD Median    | kswin        |  0.9525 |        0.9688 | 5.1%                  |            1040 |
| EDD Median    | hddm_a       |  2.0157 |        2.0708 | 0.1%                  |             640 |
| EDD Median    | hddm_w       |  1.6686 |        1.7089 | 0.0%                  |            2560 |
| EDD Median    | floss        |  0.028  |        0.028  | 50.9%                 |           22494 |

## 4. Trade-off Analysis (Constrained Optimization)

Performance in specific scenarios (e.g., 'What is the best Precision I can get if I need Recall > 0.8?').

| Scenario              | Target        | Detector     | Score                 |
|:----------------------|:--------------|:-------------|:----------------------|
| High Recall (>0.8)    | Max Precision | adwin        | 0.1528                |
| High Recall (>0.8)    | Max Precision | page_hinkley | 0.1401                |
| High Recall (>0.8)    | Max Precision | kswin        | 0.1461                |
| High Recall (>0.8)    | Max Precision | hddm_a       | 0.1468                |
| High Recall (>0.8)    | Max Precision | hddm_w       | 0.1082                |
| High Recall (>0.8)    | Max Precision | floss        | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | adwin        | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | page_hinkley | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | kswin        | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | hddm_a       | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | hddm_w       | N/A (No config found) |
| High Precision (>0.8) | Max Recall    | floss        | N/A (No config found) |
| High F1 (>0.8)        | Min Delay (s) | adwin        | N/A                   |
| High F1 (>0.8)        | Min Delay (s) | page_hinkley | N/A                   |
| High F1 (>0.8)        | Min Delay (s) | kswin        | N/A                   |
| High F1 (>0.8)        | Min Delay (s) | hddm_a       | N/A                   |
| High F1 (>0.8)        | Min Delay (s) | hddm_w       | N/A                   |
| High F1 (>0.8)        | Min Delay (s) | floss        | N/A                   |

## 5. Recommendations

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

