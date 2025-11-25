# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:26:28.804453 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 2560
- **Total Evaluations**: 87040
- **Total Ground Truth Events**: 248320
- **Total Detections**: 295304
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.0001
- warning_confidence: 0.001
- lambda_option: 0.01
- two_side_option: False
- ma_window: 10
- min_gap_samples: 3000
- F3 WEIGHTED: 0.0204 ± 0.0720
- F3 CLASSIC: 0.0229 ± 0.0764
- F1 WEIGHTED: 0.0070 ± 0.0257
- F1 CLASSIC: 0.0077 ± 0.0267
- RECALL 4S: 0.0412 ± 0.1828
- RECALL 10S: 0.0559 ± 0.1988
- PRECISION 4S: 0.0035 ± 0.0145
- PRECISION 10S: 0.0043 ± 0.0151
- EDD MEDIAN S: 3.0527
- FP PER MIN: 0.7282
- nab_score_standard: -3.0485 ± 2.4678
- nab_score_low_fp: -3.4691 ± 2.6834
- nab_score_low_fn: -5.5736 ± 4.9646
- n_ground_truth_sum: 97.0000
- n_detections_sum: 214.0000
- NAB Scores:
  - nab_score_standard: -3.0485 ± 2.4678
  - nab_score_low_fp: -3.4691 ± 2.6834
  - nab_score_low_fn: -5.5736 ± 4.9646

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.0075)
- F1 Classic best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=3000 (score=0.0116)
- F3 Classic best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=3000 (score=0.0245)
- Nab Standard best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.05, two_side_option=False, ma_window=1, min_gap_samples=500
- Nab Low Fp best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.05, two_side_option=False, ma_window=1, min_gap_samples=500
- Nab Low Fn best: drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=10, min_gap_samples=3000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|---|
| 0.0001 | 0.001 | 0.01 | False | 10 | 3000 | 0.0204 |
| 0.0001 | 0.001 | 0.01 | True | 10 | 3000 | 0.0204 |
| 0.0001 | 0.005 | 0.01 | False | 10 | 3000 | 0.0204 |
| 0.0001 | 0.005 | 0.01 | True | 10 | 3000 | 0.0204 |
| 0.0001 | 0.01 | 0.01 | False | 10 | 3000 | 0.0204 |
| 0.0001 | 0.01 | 0.01 | True | 10 | 3000 | 0.0204 |
| 0.0001 | 0.05 | 0.01 | False | 10 | 3000 | 0.0204 |
| 0.0001 | 0.05 | 0.01 | True | 10 | 3000 | 0.0204 |
| 0.0005 | 0.001 | 0.01 | False | 10 | 3000 | 0.0204 |
| 0.0005 | 0.001 | 0.01 | True | 10 | 3000 | 0.0204 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|---|
| 0.0001 | 0.001 | 0.05 | False | 1 | 500 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 1 | 1000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 1 | 2000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 1 | 3000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 1 | 5000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 10 | 500 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 10 | 1000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 10 | 2000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 10 | 3000 | -2.8529 |
| 0.0001 | 0.001 | 0.05 | False | 10 | 5000 | -2.8529 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._