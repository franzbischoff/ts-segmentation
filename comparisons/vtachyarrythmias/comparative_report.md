# Comparative Analysis: Change Point Detectors

**Date**: 2025-11-13
**Detectors**: adwin, page_hinkley, kswin, hddm_a, hddm_w, floss

---

## 1. Best Configurations by Metric

Comparison of optimal parameter settings for each metric:

| metric             | adwin                              | page_hinkley                                             | kswin                                                              | hddm_a                                                                                              | hddm_w                                                                                                                 | floss                                                                        |
|:-------------------|:-----------------------------------|:---------------------------------------------------------|:-------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|
| f3_weighted        | 0.2367 (δ=0.025, ma=250, gap=2000) | 0.2295 (lambda_=10, δ=0.005, α=0.9999, ma=200, gap=2000) | 0.2409 (α=0.05, window_size=500, stat_size=50, ma=100, gap=2000)   | 0.2229 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=100, gap=2000)  | 0.0204 (drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=10, gap=3000) | 0.3604 (window_size=75, regime_threshold=0.45, regime_landmark=2.5, gap=200) |
| f1_weighted        | 0.0884 (δ=0.005, ma=10, gap=4000)  | 0.0711 (lambda_=30, δ=0.02, α=0.9999, ma=200, gap=4000)  | 0.0783 (α=0.001, window_size=500, stat_size=30, ma=10, gap=3000)   | 0.0682 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=100, gap=3000)  | 0.0075 (drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=1, gap=2000)   | 0.2583 (window_size=50, regime_threshold=0.3, regime_landmark=4, gap=200)    |
| nab_score_standard | -1.8779 (δ=0.005, ma=10, gap=4000) | -2.4641 (lambda_=30, δ=0.02, α=0.9999, ma=200, gap=4000) | -2.2784 (α=0.005, window_size=500, stat_size=50, ma=100, gap=5000) | -2.8088 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=100, gap=3000) | -2.8529 (drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.05, two_side_option=False, ma=1, gap=500)  | -1.1043 (window_size=50, regime_threshold=0.4, regime_landmark=3, gap=200)   |
| nab_score_low_fp   | -3.1494 (δ=0.005, ma=10, gap=4000) | -5.1397 (lambda_=30, δ=0.02, α=0.9999, ma=200, gap=4000) | -2.8529 (α=0.001, window_size=50, stat_size=50, ma=1, gap=500)     | -5.0587 (drift_confidence=0.001, warning_confidence=0.001, two_side_option=False, ma=50, gap=5000)  | -2.8529 (drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.05, two_side_option=False, ma=1, gap=500)  | -1.7147 (window_size=50, regime_threshold=0.4, regime_landmark=3, gap=1000)  |
| nab_score_low_fn   | -1.0829 (δ=0.1, ma=150, gap=2000)  | -1.0051 (lambda_=80, δ=0.04, α=0.9999, ma=50, gap=2000)  | -0.8889 (α=0.001, window_size=500, stat_size=50, ma=10, gap=2000)  | -1.1061 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=50, gap=2000) | -5.5735 (drift_confidence=0.001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=10, gap=3000) | -1.1648 (window_size=25, regime_threshold=0.8, regime_landmark=4, gap=200)   |
| recall_10s         | 0.9967 (δ=0.05, ma=200, gap=1000)  | 1.0000 (lambda_=10, δ=0.005, α=0.99, ma=10, gap=500)     | 1.0000 (α=0.001, window_size=50, stat_size=20, ma=1, gap=500)      | 1.0000 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=1, gap=500)    | 0.0794 (drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=1, gap=500)   | 0.8315 (window_size=275, regime_threshold=0.9, regime_landmark=3, gap=200)   |
| precision_10s      | 0.0792 (δ=0.005, ma=10, gap=4000)  | 0.0608 (lambda_=30, δ=0.04, α=0.99, ma=200, gap=4000)    | 0.0637 (α=0.005, window_size=500, stat_size=50, ma=100, gap=5000)  | 0.0562 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=50, gap=5000)  | 0.0100 (drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=1, gap=3000)  | 0.3549 (window_size=100, regime_threshold=0.15, regime_landmark=2, gap=1000) |
| fp_per_min         | 1.5881 (δ=0.005, ma=10, gap=5000)  | 3.4294 (lambda_=50, δ=0.005, α=0.99, ma=200, gap=4000)   | 0.0000 (α=0.001, window_size=50, stat_size=50, ma=1, gap=500)      | 2.8537 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=50, gap=5000)  | 0.0416 (drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma=1, gap=500)    | 0.1006 (window_size=125, regime_threshold=0.1, regime_landmark=4, gap=5000)  |
| edd_median_s       | 1.8394 (δ=0.005, ma=100, gap=1000) | 1.0839 (lambda_=80, δ=0.005, α=0.99, ma=50, gap=500)     | 0.7958 (α=0.01, window_size=50, stat_size=30, ma=100, gap=500)     | 1.0221 (drift_confidence=0.0005, warning_confidence=0.001, two_side_option=True, ma=100, gap=500)   | 0.7840 (drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma=100, gap=500)  | 0.0400 (window_size=25, regime_threshold=0.05, regime_landmark=3, gap=200)   |

## 2. Detector Rankings

Detectors ranked by performance on key metrics:

| metric        | rank_1          | rank_2          | rank_3                | rank_4                 | rank_5                | rank_6           |
|:--------------|:----------------|:----------------|:----------------------|:-----------------------|:----------------------|:-----------------|
| F3-Weighted   | floss (0.3604)  | kswin (0.2409)  | adwin (0.2367)        | page_hinkley (0.2295)  | hddm_a (0.2229)       | hddm_w (0.0204)  |
| NAB Standard  | floss (-1.1043) | adwin (-1.8779) | kswin (-2.2784)       | page_hinkley (-2.4641) | hddm_a (-2.8088)      | hddm_w (-2.8529) |
| Recall@10s    | hddm_a (0.9902) | kswin (0.9804)  | page_hinkley (0.9660) | adwin (0.9575)         | floss (0.5825)        | hddm_w (0.0559)  |
| Precision@10s | floss (0.1499)  | kswin (0.0477)  | page_hinkley (0.0450) | adwin (0.0444)         | hddm_a (0.0443)       | hddm_w (0.0043)  |
| FP/min        | hddm_w (0.7282) | floss (1.3003)  | kswin (6.3386)        | page_hinkley (6.6992)  | adwin (6.7720)        | hddm_a (7.0772)  |
| EDD Median    | floss (2.1996)  | hddm_w (3.0527) | adwin (3.4119)        | kswin (3.6699)         | page_hinkley (3.9130) | hddm_a (4.3358)  |

## 3. Performance & Robustness Analysis

Analysis of peak performance and parameter sensitivity.
- **Best**: The single highest score achieved.
- **Top-10 Mean**: Average of the top 10 configurations (indicates stability of the peak).
- **Param Tolerance**: Geometric mean of the normalized valid range for each parameter. Indicates how much you can vary parameters (0% to 100% of tested range) while maintaining >90% performance.

| Metric        | Detector     |    Best |   Top-10 Mean | Param Tolerance (%)   |   Total Configs |
|:--------------|:-------------|--------:|--------------:|:----------------------|----------------:|
| F3-Weighted   | adwin        |  0.2367 |        0.2288 | 89.3%                 |             495 |
| F3-Weighted   | page_hinkley |  0.2295 |        0.229  | 6.3%                  |             384 |
| F3-Weighted   | kswin        |  0.2409 |        0.2365 | 74.0%                 |            1280 |
| F3-Weighted   | hddm_a       |  0.2229 |        0.2225 | 68.7%                 |             640 |
| F3-Weighted   | hddm_w       |  0.0204 |        0.0204 | 0.0%                  |            2560 |
| F3-Weighted   | floss        |  0.3604 |        0.3523 | 38.7%                 |           25920 |
| F1-Weighted   | adwin        |  0.0884 |        0.0824 | 41.0%                 |             495 |
| F1-Weighted   | page_hinkley |  0.0711 |        0.0694 | 89.4%                 |             384 |
| F1-Weighted   | kswin        |  0.0783 |        0.0743 | 92.2%                 |            1280 |
| F1-Weighted   | hddm_a       |  0.0682 |        0.0681 | 68.7%                 |             640 |
| F1-Weighted   | hddm_w       |  0.0075 |        0.0075 | 2.9%                  |            2560 |
| F1-Weighted   | floss        |  0.2583 |        0.2497 | 52.1%                 |           25920 |
| NAB Standard  | adwin        | -1.8779 |       -2.0596 | 21.7%                 |             495 |
| NAB Standard  | page_hinkley | -2.4641 |       -2.4896 | 0.4%                  |             384 |
| NAB Standard  | kswin        | -2.2784 |       -2.3741 | 68.3%                 |            1280 |
| NAB Standard  | hddm_a       | -2.8088 |       -2.811  | 81.6%                 |             640 |
| NAB Standard  | hddm_w       | -2.8529 |       -2.8529 | 100.0%                |            2560 |
| NAB Standard  | floss        | -1.1043 |       -1.1685 | 26.5%                 |           25920 |
| NAB Low FP    | adwin        | -3.1494 |       -3.5324 | 0.0%                  |             495 |
| NAB Low FP    | page_hinkley | -5.1397 |       -5.1594 | 6.0%                  |             384 |
| NAB Low FP    | kswin        | -2.8529 |       -2.8529 | 58.7%                 |            1280 |
| NAB Low FP    | hddm_a       | -5.0587 |       -5.0609 | 3.2%                  |             640 |
| NAB Low FP    | hddm_w       | -2.8529 |       -2.8529 | 100.0%                |            2560 |
| NAB Low FP    | floss        | -1.7147 |       -1.7484 | 57.6%                 |           25920 |
| NAB Low FN    | adwin        | -1.0829 |       -1.1147 | 0.9%                  |             495 |
| NAB Low FN    | page_hinkley | -1.0051 |       -1.0338 | 6.0%                  |             384 |
| NAB Low FN    | kswin        | -0.8889 |       -0.9365 | 0.3%                  |            1280 |
| NAB Low FN    | hddm_a       | -1.1061 |       -1.1179 | 3.2%                  |             640 |
| NAB Low FN    | hddm_w       | -5.5735 |       -5.5735 | 100.0%                |            2560 |
| NAB Low FN    | floss        | -1.1648 |       -1.4457 | 0.0%                  |           25920 |
| Recall@10s    | adwin        |  0.9967 |        0.9964 | 60.0%                 |             495 |
| Recall@10s    | page_hinkley |  1      |        1      | 84.4%                 |             384 |
| Recall@10s    | kswin        |  1      |        1      | 88.9%                 |            1280 |
| Recall@10s    | hddm_a       |  1      |        1      | 76.0%                 |             640 |
| Recall@10s    | hddm_w       |  0.0794 |        0.0794 | 0.3%                  |            2560 |
| Recall@10s    | floss        |  0.8315 |        0.8189 | 34.2%                 |           25920 |
| Precision@10s | adwin        |  0.0792 |        0.0675 | 0.0%                  |             495 |
| Precision@10s | page_hinkley |  0.0608 |        0.0608 | 0.4%                  |             384 |
| Precision@10s | kswin        |  0.0637 |        0.0619 | 83.0%                 |            1280 |
| Precision@10s | hddm_a       |  0.0562 |        0.0562 | 81.6%                 |             640 |
| Precision@10s | hddm_w       |  0.01   |        0.01   | 0.0%                  |            2560 |
| Precision@10s | floss        |  0.3549 |        0.3336 | 0.0%                  |           25920 |
| FP/min        | adwin        |  1.5881 |        1.7494 | 0.0%                  |             495 |
| FP/min        | page_hinkley |  3.4294 |        3.4307 | 6.3%                  |             384 |
| FP/min        | kswin        |  0      |        0      | 58.7%                 |            1280 |
| FP/min        | hddm_a       |  2.8537 |        2.8537 | 3.2%                  |             640 |
| FP/min        | hddm_w       |  0.0416 |        0.0416 | 5.5%                  |            2560 |
| FP/min        | floss        |  0.1006 |        0.1006 | 46.6%                 |           25920 |
| EDD Median    | adwin        |  1.8394 |        1.9862 | 0.9%                  |             495 |
| EDD Median    | page_hinkley |  1.0839 |        1.1287 | 4.3%                  |             384 |
| EDD Median    | kswin        |  0.7958 |        0.8937 | 4.1%                  |            1040 |
| EDD Median    | hddm_a       |  1.0221 |        1.0647 | 1.7%                  |             640 |
| EDD Median    | hddm_w       |  0.784  |        0.8016 | 0.0%                  |             640 |
| EDD Median    | floss        |  0.04   |        0.04   | 1.8%                  |           24000 |

## 4. Trade-off Analysis (Constrained Optimization)

Performance in specific scenarios (e.g., 'What is the best Precision I can get if I need Recall > 0.8?').

| Scenario              | Target        | Detector     | Score                 |
|:----------------------|:--------------|:-------------|:----------------------|
| High Recall (>0.8)    | Max Precision | adwin        | 0.0572                |
| High Recall (>0.8)    | Max Precision | page_hinkley | 0.0452                |
| High Recall (>0.8)    | Max Precision | kswin        | 0.0611                |
| High Recall (>0.8)    | Max Precision | hddm_a       | 0.0516                |
| High Recall (>0.8)    | Max Precision | hddm_w       | N/A (No config found) |
| High Recall (>0.8)    | Max Precision | floss        | 0.0727                |
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

