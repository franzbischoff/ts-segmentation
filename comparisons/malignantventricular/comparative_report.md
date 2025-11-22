# Comparative Analysis: Change Point Detectors

**Date**: 2025-11-13
**Detectors**: adwin, page_hinkley, kswin, hddm_a, hddm_w, floss

---

## 1. Best Configurations by Metric

Comparison of optimal parameter settings for each metric:

| metric             | adwin                                | page_hinkley                                        | kswin                                                 | hddm_a                                                                                                | hddm_w                                                                                                      | floss                                               |
|:-------------------|:-------------------------------------|:----------------------------------------------------|:------------------------------------------------------|:------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:----------------------------------------------------|
| f3_weighted        | 0.2641 (δ=0.1, ma=150, gap=2000)     | 0.2559 (λ=80, δ=0.04, α=0.9999, ma=200, gap=1000)   | 0.2699 (α=0.01, win=500, stat=20, ma=100, gap=1000)   | 0.2574 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=100, gap=2000)   | 0.0560 (drift_confidence=0.0005, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=1, gap=1000)   | 0.3076 (win=125, reg_th=0.7, reg_lm=5.5, gap=1000)  |
| f1_weighted        | 0.0995 (δ=0.005, ma=10, gap=1000)    | 0.1002 (λ=80, δ=0.04, α=0.99, ma=200, gap=2000)     | 0.1010 (α=0.01, win=200, stat=30, ma=1, gap=5000)     | 0.0993 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=100, gap=2000)   | 0.0511 (drift_confidence=0.0005, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=1, gap=1000)   | 0.1996 (win=75, reg_th=0.6, reg_lm=6, gap=500)      |
| nab_score_standard | -18.9256 (δ=0.02, ma=75, gap=2000)   | -20.0441 (λ=10, δ=0.04, α=0.99, ma=200, gap=2000)   | -19.7894 (α=0.05, win=500, stat=30, ma=10, gap=2000)  | -20.6035 (drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma=100, gap=2000) | -26.9091 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=50, gap=500) | -14.9051 (win=25, reg_th=0.9, reg_lm=7.5, gap=1000) |
| nab_score_low_fp   | -29.1142 (δ=0.01, ma=25, gap=4000)   | -30.5204 (λ=10, δ=0.04, α=0.9999, ma=200, gap=4000) | -26.9091 (α=0.001, win=50, stat=50, ma=1, gap=500)    | -30.8173 (drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma=100, gap=5000) | -26.9091 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=50, gap=500) | -18.5892 (win=25, reg_th=0.8, reg_lm=7, gap=2000)   |
| nab_score_low_fn   | -21.5056 (δ=0.015, ma=150, gap=2000) | -22.1834 (λ=10, δ=0.04, α=0.99, ma=50, gap=2000)    | -21.4315 (α=0.001, win=500, stat=100, ma=1, gap=2000) | -21.4144 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=50, gap=2000)   | -53.5660 (drift_confidence=0.0005, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=1, gap=2000) | -24.8010 (win=75, reg_th=0.9, reg_lm=6.5, gap=500)  |
| recall_10s         | 0.9723 (δ=0.08, ma=300, gap=1000)    | 0.9896 (λ=30, δ=0.005, α=0.99, ma=10, gap=500)      | 0.9997 (α=0.001, win=50, stat=30, ma=100, gap=500)    | 0.9997 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=10, gap=500)      | 0.0852 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=1, gap=500)    | 0.7442 (win=225, reg_th=0.9, reg_lm=7, gap=200)     |
| precision_10s      | 0.1014 (δ=0.01, ma=10, gap=2000)     | 0.0984 (λ=80, δ=0.005, α=0.9999, ma=200, gap=4000)  | 0.0966 (α=0.01, win=200, stat=50, ma=100, gap=5000)   | 0.0897 (drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma=100, gap=5000)   | 0.1839 (drift_confidence=0.0005, warning_confidence=0.001, λ=0.01, two_side_option=False, ma=1, gap=2000)   | 0.5400 (win=25, reg_th=0.45, reg_lm=4.5, gap=5000)  |
| fp_per_min         | 1.6065 (δ=0.005, ma=10, gap=5000)    | 2.7052 (λ=80, δ=0.04, α=0.99, ma=200, gap=4000)     | 0.0000 (α=0.001, win=50, stat=50, ma=1, gap=500)      | 2.4182 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma=100, gap=5000)   | 0.0104 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.1, two_side_option=False, ma=1, gap=2000)    | 0.0208 (win=25, reg_th=0.3, reg_lm=5.5, gap=5000)   |
| edd_median_s       | 2.3254 (δ=0.08, ma=300, gap=1000)    | 1.1203 (λ=80, δ=0.01, α=0.99, ma=10, gap=500)       | 0.8437 (α=0.001, win=50, stat=30, ma=100, gap=500)    | 1.0633 (drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma=50, gap=500)      | 0.0040 (drift_confidence=0.0001, warning_confidence=0.001, λ=0.2, two_side_option=False, ma=100, gap=3000)  | 1.0027 (win=375, reg_th=0.2, reg_lm=3.5, gap=5000)  |

## 2. Detector Rankings

Detectors ranked by performance on key metrics:

| metric        | rank_1                | rank_2           | rank_3                | rank_4                  | rank_5                | rank_6                |
|:--------------|:----------------------|:-----------------|:----------------------|:------------------------|:----------------------|:----------------------|
| F3-Weighted   | floss (0.3076)        | kswin (0.2699)   | adwin (0.2641)        | hddm_a (0.2574)         | page_hinkley (0.2559) | hddm_w (0.0560)       |
| NAB Standard  | floss (-14.9051)      | adwin (-18.9256) | kswin (-19.7894)      | page_hinkley (-20.0441) | hddm_a (-20.6035)     | hddm_w (-26.9091)     |
| Recall@10s    | kswin (0.9531)        | adwin (0.8974)   | page_hinkley (0.8427) | hddm_a (0.8150)         | floss (0.5903)        | hddm_w (0.0852)       |
| Precision@10s | hddm_w (0.1762)       | floss (0.1404)   | hddm_a (0.0821)       | adwin (0.0797)          | kswin (0.0632)        | page_hinkley (0.0627) |
| FP/min        | hddm_w (0.4013)       | floss (2.1701)   | hddm_a (5.6039)       | adwin (6.3429)          | page_hinkley (9.1714) | kswin (9.5130)        |
| EDD Median    | page_hinkley (2.6899) | kswin (2.9456)   | hddm_w (3.2237)       | floss (3.7230)          | adwin (4.3835)        | hddm_a (4.4714)       |

## 3. Performance & Robustness Analysis

Analysis of peak performance and parameter sensitivity.

**Note**: Robustness and Top-N summaries are computed using the best-performing parameter configurations only
(by default the top 10 configurations), rather than averaging across the full grid. This avoids bias from
large grids that include many poor parameter choices. You can change the Top-N or use a top-percent selection
when running the script (see --robust-top-n / --robust-top-percent).

- **Best**: The single highest score achieved.
- **Top-10 Mean**: Average of the top 10 configurations (indicates stability of the peak).
- **Param Tolerance**: Geometric mean of the normalized valid range for each parameter. Indicates how much you can vary parameters (0% to 100% of tested range) while maintaining >90% performance.

| Metric        | Detector     |     Best |   Top-10 Mean | Param Tolerance (%)   |   Total Configs |
|:--------------|:-------------|---------:|--------------:|:----------------------|----------------:|
| F3-Weighted   | adwin        |   0.2641 |        0.2606 | 63.0%                 |             495 |
| F3-Weighted   | page_hinkley |   0.2559 |        0.2556 | 77.8%                 |             384 |
| F3-Weighted   | kswin        |   0.2699 |        0.2682 | 74.0%                 |            1280 |
| F3-Weighted   | hddm_a       |   0.2574 |        0.2558 | 68.7%                 |             640 |
| F3-Weighted   | hddm_w       |   0.056  |        0.056  | 2.5%                  |            2560 |
| F3-Weighted   | floss        |   0.3076 |        0.3024 | 59.0%                 |           25920 |
| F1-Weighted   | adwin        |   0.0995 |        0.0978 | 100.0%                |             495 |
| F1-Weighted   | page_hinkley |   0.1002 |        0.0993 | 97.0%                 |             384 |
| F1-Weighted   | kswin        |   0.101  |        0.0969 | 92.2%                 |            1280 |
| F1-Weighted   | hddm_a       |   0.0993 |        0.0973 | 3.1%                  |             640 |
| F1-Weighted   | hddm_w       |   0.0511 |        0.051  | 64.4%                 |            2560 |
| F1-Weighted   | floss        |   0.1996 |        0.1967 | 69.0%                 |           25920 |
| NAB Standard  | adwin        | -18.9256 |      -19.6085 | 60.0%                 |             495 |
| NAB Standard  | page_hinkley | -20.0441 |      -20.1818 | 89.4%                 |             384 |
| NAB Standard  | kswin        | -19.7894 |      -20.1191 | 92.2%                 |            1280 |
| NAB Standard  | hddm_a       | -20.6035 |      -20.6313 | 90.4%                 |             640 |
| NAB Standard  | hddm_w       | -26.9091 |      -26.9091 | 100.0%                |            2560 |
| NAB Standard  | floss        | -14.9051 |      -15.232  | 47.1%                 |           25920 |
| NAB Low FP    | adwin        | -29.1142 |      -29.3556 | 90.9%                 |             495 |
| NAB Low FP    | page_hinkley | -30.5204 |      -30.5829 | 6.3%                  |             384 |
| NAB Low FP    | kswin        | -26.9091 |      -26.9091 | 58.7%                 |            1280 |
| NAB Low FP    | hddm_a       | -30.8173 |      -30.897  | 81.6%                 |             640 |
| NAB Low FP    | hddm_w       | -26.9091 |      -26.9091 | 100.0%                |            2560 |
| NAB Low FP    | floss        | -18.5892 |      -18.9136 | 36.4%                 |           25920 |
| NAB Low FN    | adwin        | -21.5056 |      -21.8035 | 57.9%                 |             495 |
| NAB Low FN    | page_hinkley | -22.1834 |      -22.3242 | 77.8%                 |             384 |
| NAB Low FN    | kswin        | -21.4315 |      -21.5384 | 74.0%                 |            1280 |
| NAB Low FN    | hddm_a       | -21.4144 |      -21.556  | 68.7%                 |             640 |
| NAB Low FN    | hddm_w       | -53.566  |      -53.566  | 100.0%                |            2560 |
| NAB Low FN    | floss        | -24.801  |      -25.1524 | 39.2%                 |           25920 |
| Recall@10s    | adwin        |   0.9723 |        0.9708 | 57.9%                 |             495 |
| Recall@10s    | page_hinkley |   0.9896 |        0.9895 | 49.6%                 |             384 |
| Recall@10s    | kswin        |   0.9997 |        0.9997 | 80.3%                 |            1280 |
| Recall@10s    | hddm_a       |   0.9997 |        0.9997 | 76.0%                 |             640 |
| Recall@10s    | hddm_w       |   0.0852 |        0.0852 | 3.1%                  |            2560 |
| Recall@10s    | floss        |   0.7442 |        0.741  | 31.9%                 |           25920 |
| Precision@10s | adwin        |   0.1014 |        0.0989 | 61.5%                 |             495 |
| Precision@10s | page_hinkley |   0.0984 |        0.0982 | 6.3%                  |             384 |
| Precision@10s | kswin        |   0.0966 |        0.0955 | 85.0%                 |            1280 |
| Precision@10s | hddm_a       |   0.0897 |        0.0894 | 90.4%                 |             640 |
| Precision@10s | hddm_w       |   0.1839 |        0.1839 | 4.7%                  |            2560 |
| Precision@10s | floss        |   0.54   |        0.5308 | 44.8%                 |           25920 |
| FP/min        | adwin        |   1.6065 |        1.7021 | 0.0%                  |             495 |
| FP/min        | page_hinkley |   2.7052 |        2.7208 | 0.4%                  |             384 |
| FP/min        | kswin        |   0      |        0      | 58.7%                 |            1280 |
| FP/min        | hddm_a       |   2.4182 |        2.4216 | 2.7%                  |             640 |
| FP/min        | hddm_w       |   0.0104 |        0.0104 | 81.1%                 |            2560 |
| FP/min        | floss        |   0.0208 |        0.0213 | 34.7%                 |           25920 |
| EDD Median    | adwin        |   2.3254 |        2.459  | 0.9%                  |             495 |
| EDD Median    | page_hinkley |   1.1203 |        1.1295 | 0.4%                  |             384 |
| EDD Median    | kswin        |   0.8437 |        0.8745 | 5.1%                  |            1040 |
| EDD Median    | hddm_a       |   1.0633 |        1.0703 | 3.2%                  |             640 |
| EDD Median    | hddm_w       |   0.004  |        0.004  | 0.0%                  |            1872 |
| EDD Median    | floss        |   1.0027 |        1.2078 | 0.0%                  |           22920 |

## 4. Trade-off Analysis (Constrained Optimization)

Performance in specific scenarios (e.g., 'What is the best Precision I can get if I need Recall > 0.8?').

| Scenario              | Target        | Detector     | Score                 |
|:----------------------|:--------------|:-------------|:----------------------|
| High Recall (>0.8)    | Max Precision | adwin        | 0.0882                |
| High Recall (>0.8)    | Max Precision | page_hinkley | 0.0806                |
| High Recall (>0.8)    | Max Precision | kswin        | 0.0847                |
| High Recall (>0.8)    | Max Precision | hddm_a       | 0.0830                |
| High Recall (>0.8)    | Max Precision | hddm_w       | N/A (No config found) |
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

