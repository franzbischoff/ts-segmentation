# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:37:50.394415 UTC
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
- lambda_option: 0.2
- two_side_option: False
- ma_window: 1
- min_gap_samples: 1000
- F3 WEIGHTED: 0.3530 ± 0.2404
- F3 CLASSIC: 0.3761 ± 0.2571
- F1 WEIGHTED: 0.1489 ± 0.1529
- F1 CLASSIC: 0.1599 ± 0.1650
- RECALL 4S: 0.6567 ± 0.3551
- RECALL 10S: 0.8165 ± 0.3396
- PRECISION 4S: 0.0672 ± 0.0746
- PRECISION 10S: 0.0987 ± 0.1186
- EDD MEDIAN S: 2.6266
- FP PER MIN: 8.0671
- nab_score_standard: -7.8241 ± 29.3604
- nab_score_low_fp: -17.3492 ± 58.6820
- nab_score_low_fn: -4.7689 ± 15.2530
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 24837.0000
- NAB Scores:
  - nab_score_standard: -7.8241 ± 29.3604
  - nab_score_low_fp: -17.3492 ± 58.6820
  - nab_score_low_fn: -4.7689 ± 15.2530

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.001, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.1771)
- F1 Classic best: drift_confidence=0.001, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.2254)
- F3 Classic best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.1, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.4187)
- Nab Standard best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=1, min_gap_samples=3000
- Nab Low Fp best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=100, min_gap_samples=5000
- Nab Low Fn best: drift_confidence=0.005, warning_confidence=0.001, lambda_option=0.2, two_side_option=False, ma_window=1, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|---|
| 0.005 | 0.001 | 0.2 | False | 1 | 1000 | 0.353 |
| 0.005 | 0.001 | 0.2 | True | 1 | 1000 | 0.353 |
| 0.005 | 0.005 | 0.2 | False | 1 | 1000 | 0.353 |
| 0.005 | 0.005 | 0.2 | True | 1 | 1000 | 0.353 |
| 0.005 | 0.01 | 0.2 | False | 1 | 1000 | 0.353 |
| 0.005 | 0.01 | 0.2 | True | 1 | 1000 | 0.353 |
| 0.005 | 0.05 | 0.2 | False | 1 | 1000 | 0.353 |
| 0.005 | 0.05 | 0.2 | True | 1 | 1000 | 0.353 |
| 0.005 | 0.001 | 0.1 | False | 1 | 1000 | 0.3526 |
| 0.005 | 0.001 | 0.1 | True | 1 | 1000 | 0.3526 |
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