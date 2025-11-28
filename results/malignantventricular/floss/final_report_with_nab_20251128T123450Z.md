# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T12:34:50.189873 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 25920
- **Total Evaluations**: 570240
- **Total Ground Truth Events**: 15344640
- **Total Detections**: 29204019
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- window_size: 125.0
- regime_threshold: 0.7
- regime_landmark: 5.5
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.3076 ± 0.1382
- F3 CLASSIC: 0.3654 ± 0.1634
- F1 WEIGHTED: 0.1556 ± 0.0856
- F1 CLASSIC: 0.1885 ± 0.1042
- RECALL 4S: 0.3936 ± 0.1637
- RECALL 10S: 0.5903 ± 0.1914
- PRECISION 4S: 0.0811 ± 0.0737
- PRECISION 10S: 0.1404 ± 0.1260
- EDD MEDIAN S: 3.7230
- FP PER MIN: 2.1701
- nab_score_standard: -15.4105 ± 24.1286
- nab_score_low_fp: -22.5814 ± 23.6423
- nab_score_low_fn: -28.5070 ± 52.9853
- n_ground_truth_sum: 592.0000
- n_detections_sum: 1942.0000
- NAB Scores:
  - nab_score_standard: -15.4105 ± 24.1286
  - nab_score_low_fp: -22.5814 ± 23.6423
  - nab_score_low_fn: -28.5070 ± 52.9853

## Comparison With Other Metrics
- F1 Weighted best: window_size=75.0, regime_threshold=0.6, regime_landmark=6.0, min_gap_samples=500.0 (score=0.1996)
- F1 Classic best: window_size=25.0, regime_threshold=0.8, regime_landmark=8.0, min_gap_samples=1000.0 (score=0.2792)
- F3 Classic best: window_size=75.0, regime_threshold=0.75, regime_landmark=9.0, min_gap_samples=1000.0 (score=0.3782)
- Nab Standard best: window_size=25.0, regime_threshold=0.9, regime_landmark=7.5, min_gap_samples=1000.0
- Nab Low Fp best: window_size=25.0, regime_threshold=0.8, regime_landmark=7.0, min_gap_samples=2000.0
- Nab Low Fn best: window_size=75.0, regime_threshold=0.9, regime_landmark=6.5, min_gap_samples=500.0

## Top 10 (F3-weighted)
| window_size | regime_threshold | regime_landmark | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|
| 125 | 0.7 | 5.5 | 1000 | 0.3076 |
| 175 | 0.6 | 4.5 | 500 | 0.3051 |
| 125 | 0.7 | 5.5 | 500 | 0.3031 |
| 100 | 0.65 | 5.0 | 500 | 0.3021 |
| 175 | 0.65 | 5.5 | 1000 | 0.302 |
| 175 | 0.6 | 4.5 | 1000 | 0.3017 |
| 125 | 0.75 | 5.5 | 1000 | 0.3011 |
| 175 | 0.55 | 4.5 | 500 | 0.3006 |
| 175 | 0.65 | 5.5 | 500 | 0.3006 |
| 100 | 0.7 | 5.0 | 500 | 0.3003 |
## Top 10 (NAB Standard)
| window_size | regime_threshold | regime_landmark | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|
| 25 | 0.9 | 7.5 | 1000 | -14.9051 |
| 25 | 0.9 | 8.0 | 1000 | -14.9709 |
| 25 | 0.9 | 8.5 | 1000 | -15.06 |
| 25 | 0.9 | 7.0 | 1000 | -15.143 |
| 25 | 0.85 | 5.5 | 1000 | -15.1567 |
| 25 | 0.85 | 6.5 | 1000 | -15.3594 |
| 125 | 0.7 | 5.5 | 1000 | -15.4105 |
| 25 | 0.85 | 6.0 | 1000 | -15.4144 |
| 25 | 0.85 | 7.0 | 1000 | -15.4341 |
| 25 | 0.9 | 8.0 | 2000 | -15.4658 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._