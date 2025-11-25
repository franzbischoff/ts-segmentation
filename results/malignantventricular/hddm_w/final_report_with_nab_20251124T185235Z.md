# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:52:35.438380 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 2560
- **Total Evaluations**: 56320
- **Total Ground Truth Events**: 1515520
- **Total Detections**: 134784
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.0001
- warning_confidence: 0.001
- lambda_option: 0.01
- two_side_option: False
- ma_window: 1
- min_gap_samples: 1000
- F3 WEIGHTED: 0.0560 ± 0.1017
- F3 CLASSIC: 0.0585 ± 0.1049
- F1 WEIGHTED: 0.0510 ± 0.0812
- F1 CLASSIC: 0.0530 ± 0.0826
- RECALL 4S: 0.0443 ± 0.1250
- RECALL 10S: 0.0852 ± 0.1794
- PRECISION 4S: 0.0479 ± 0.1293
- PRECISION 10S: 0.1762 ± 0.3192
- EDD MEDIAN S: 3.2237
- FP PER MIN: 0.4013
- nab_score_standard: -27.6046 ± 35.5387
- nab_score_low_fp: -28.7023 ± 35.9001
- nab_score_low_fn: -53.7375 ± 71.4250
- n_ground_truth_sum: 592.0000
- n_detections_sum: 336.0000
- NAB Scores:
  - nab_score_standard: -27.6046 ± 35.5387
  - nab_score_low_fp: -28.7023 ± 35.9001
  - nab_score_low_fn: -53.7375 ± 71.4250

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=1000 (score=0.0511)
- F1 Classic best: drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.0605)
- F3 Classic best: drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=2000 (score=0.0649)
- Nab Standard best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=50, min_gap_samples=500
- Nab Low Fp best: drift_confidence=0.0001, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=50, min_gap_samples=500
- Nab Low Fn best: drift_confidence=0.0005, warning_confidence=0.001, lambda_option=0.01, two_side_option=False, ma_window=1, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|---|
| 0.0001 | 0.001 | 0.01 | False | 1 | 1000 | 0.056 |
| 0.0001 | 0.001 | 0.01 | True | 1 | 1000 | 0.056 |
| 0.0001 | 0.005 | 0.01 | False | 1 | 1000 | 0.056 |
| 0.0001 | 0.005 | 0.01 | True | 1 | 1000 | 0.056 |
| 0.0001 | 0.01 | 0.01 | False | 1 | 1000 | 0.056 |
| 0.0001 | 0.01 | 0.01 | True | 1 | 1000 | 0.056 |
| 0.0001 | 0.05 | 0.01 | False | 1 | 1000 | 0.056 |
| 0.0001 | 0.05 | 0.01 | True | 1 | 1000 | 0.056 |
| 0.0005 | 0.001 | 0.01 | False | 1 | 1000 | 0.056 |
| 0.0005 | 0.001 | 0.01 | True | 1 | 1000 | 0.056 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | lambda_option | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|---|
| 0.0001 | 0.001 | 0.01 | False | 50 | 500 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 50 | 1000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 50 | 2000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 50 | 3000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 50 | 5000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 100 | 500 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 100 | 1000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 100 | 2000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 100 | 3000 | -26.9091 |
| 0.0001 | 0.001 | 0.01 | False | 100 | 5000 | -26.9091 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._