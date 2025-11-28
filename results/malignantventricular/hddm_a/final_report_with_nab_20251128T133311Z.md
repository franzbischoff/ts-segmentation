# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T13:33:11.781196 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 640
- **Total Evaluations**: 14080
- **Total Ground Truth Events**: 378880
- **Total Detections**: 5479812
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.0001
- warning_confidence: 0.001
- two_side_option: False
- ma_window: 100
- min_gap_samples: 2000
- F3 WEIGHTED: 0.2574 ± 0.1201
- F3 CLASSIC: 0.3388 ± 0.1485
- F1 WEIGHTED: 0.0993 ± 0.0662
- F1 CLASSIC: 0.1349 ± 0.1001
- RECALL 4S: 0.4626 ± 0.2181
- RECALL 10S: 0.8150 ± 0.2004
- PRECISION 4S: 0.0505 ± 0.0532
- PRECISION 10S: 0.0821 ± 0.0750
- EDD MEDIAN S: 4.4714
- FP PER MIN: 5.6039
- nab_score_standard: -20.6373 ± 15.3764
- nab_score_low_fp: -38.9994 ± 16.8284
- nab_score_low_fn: -24.3198 ± 35.5978
- n_ground_truth_sum: 592.0000
- n_detections_sum: 4751.0000
- NAB Scores:
  - nab_score_standard: -20.6373 ± 15.3764
  - nab_score_low_fp: -38.9994 ± 16.8284
  - nab_score_low_fn: -24.3198 ± 35.5978

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma_window=100, min_gap_samples=2000 (score=0.0993)
- F1 Classic best: drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma_window=100, min_gap_samples=2000 (score=0.1363)
- F3 Classic best: drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma_window=50, min_gap_samples=2000 (score=0.3458)
- Nab Standard best: drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma_window=100, min_gap_samples=2000
- Nab Low Fp best: drift_confidence=0.0005, warning_confidence=0.001, two_side_option=False, ma_window=100, min_gap_samples=5000
- Nab Low Fn best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma_window=50, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.0001 | 0.001 | False | 100 | 2000 | 0.2574 |
| 0.0001 | 0.005 | False | 100 | 2000 | 0.2574 |
| 0.0001 | 0.01 | False | 100 | 2000 | 0.2574 |
| 0.0001 | 0.05 | False | 100 | 2000 | 0.2574 |
| 0.001 | 0.001 | False | 50 | 1000 | 0.2551 |
| 0.001 | 0.005 | False | 50 | 1000 | 0.2551 |
| 0.001 | 0.01 | False | 50 | 1000 | 0.2551 |
| 0.001 | 0.05 | False | 50 | 1000 | 0.2551 |
| 0.005 | 0.001 | False | 50 | 1000 | 0.2539 |
| 0.005 | 0.005 | False | 50 | 1000 | 0.2539 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.0005 | 0.001 | False | 100 | 2000 | -20.6035 |
| 0.0005 | 0.005 | False | 100 | 2000 | -20.6035 |
| 0.0005 | 0.01 | False | 100 | 2000 | -20.6035 |
| 0.0005 | 0.05 | False | 100 | 2000 | -20.6035 |
| 0.0001 | 0.001 | False | 100 | 2000 | -20.6373 |
| 0.0001 | 0.005 | False | 100 | 2000 | -20.6373 |
| 0.0001 | 0.01 | False | 100 | 2000 | -20.6373 |
| 0.0001 | 0.05 | False | 100 | 2000 | -20.6373 |
| 0.001 | 0.001 | False | 100 | 2000 | -20.6749 |
| 0.001 | 0.005 | False | 100 | 2000 | -20.6749 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._