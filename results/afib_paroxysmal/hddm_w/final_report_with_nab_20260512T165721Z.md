# Comparative Report — Temporary Snapshot
Generated: 2026-05-12T16:57:21.906745 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 2560
- **Total Evaluations**: 586240
- **Total Ground Truth Events**: 3330560
- **Total Detections**: 24458200
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.005
- warning_confidence: 0.001
- lambda_option: 0.1
- two_side_option: False
- ma_window: 1
- min_gap_samples: 1000
- F3 WEIGHTED: 0.3541 ± 0.2337
- F3 CLASSIC: 0.3842 ± 0.2546
- F1 WEIGHTED: 0.1561 ± 0.1539
- F1 CLASSIC: 0.1697 ± 0.1690
- RECALL 4S: 0.6150 ± 0.3459
- RECALL 10S: 0.8080 ± 0.3377
- PRECISION 4S: 0.0694 ± 0.0833
- PRECISION 10S: 0.1082 ± 0.1291
- EDD MEDIAN S: 2.6745
- FP PER MIN: 7.4312
- nab_score_standard: -7.5594 ± 28.7631
- nab_score_low_fp: -16.6066 ± 57.5063
- nab_score_low_fn: -4.8481 ± 14.9810
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 23530.0000
- NAB Scores:
  - nab_score_standard: -7.5594 ± 28.7631
  - nab_score_low_fp: -16.6066 ± 57.5063
  - nab_score_low_fn: -4.8481 ± 14.9810

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.001, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.1839)
- F1 Classic best: drift_confidence=0.001, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.2254)
- F3 Classic best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.4187)
- Nab Standard best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=1, min_gap_samples=3000
- Nab Low Fp best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=100, min_gap_samples=5000
- Nab Low Fn best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=1, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|---|
| 0.005 | 0.001 | 0.1 | False | 1 | 1000 | 0.3541 |
| 0.005 | 0.001 | 0.1 | True | 1 | 1000 | 0.3541 |
| 0.005 | 0.001 | 0.2 | False | 1 | 1000 | 0.3541 |
| 0.005 | 0.001 | 0.2 | True | 1 | 1000 | 0.3541 |
| 0.005 | 0.005 | 0.1 | False | 1 | 1000 | 0.3541 |
| 0.005 | 0.005 | 0.1 | True | 1 | 1000 | 0.3541 |
| 0.005 | 0.005 | 0.2 | False | 1 | 1000 | 0.3541 |
| 0.005 | 0.005 | 0.2 | True | 1 | 1000 | 0.3541 |
| 0.005 | 0.01 | 0.1 | False | 1 | 1000 | 0.3541 |
| 0.005 | 0.01 | 0.1 | True | 1 | 1000 | 0.3541 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|---|
| 0.005 | 0.001 | 0.2 | False | 1 | 3000 | -4.4566 |
| 0.005 | 0.001 | 0.2 | True | 1 | 3000 | -4.4566 |
| 0.005 | 0.005 | 0.2 | False | 1 | 3000 | -4.4566 |
| 0.005 | 0.005 | 0.2 | True | 1 | 3000 | -4.4566 |
| 0.005 | 0.01 | 0.2 | False | 1 | 3000 | -4.4566 |
| 0.005 | 0.01 | 0.2 | True | 1 | 3000 | -4.4566 |
| 0.005 | 0.05 | 0.2 | False | 1 | 3000 | -4.4566 |
| 0.005 | 0.05 | 0.2 | True | 1 | 3000 | -4.4566 |
| 0.001 | 0.001 | 0.2 | False | 1 | 3000 | -4.5323 |
| 0.001 | 0.001 | 0.2 | True | 1 | 3000 | -4.5323 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._