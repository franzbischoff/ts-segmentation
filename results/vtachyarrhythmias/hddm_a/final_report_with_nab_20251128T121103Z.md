# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T12:11:03.520757 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 640
- **Total Evaluations**: 21760
- **Total Ground Truth Events**: 62080
- **Total Detections**: 2137120
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.0001
- warning_confidence: 0.001
- two_side_option: True
- ma_window: 100
- min_gap_samples: 2000
- F3 WEIGHTED: 0.2229 ± 0.1309
- F3 CLASSIC: 0.2787 ± 0.1497
- F1 WEIGHTED: 0.0659 ± 0.0547
- F1 CLASSIC: 0.0823 ± 0.0649
- RECALL 4S: 0.4973 ± 0.3798
- RECALL 10S: 0.9902 ± 0.0572
- PRECISION 4S: 0.0218 ± 0.0221
- PRECISION 10S: 0.0443 ± 0.0375
- EDD MEDIAN S: 4.3358
- FP PER MIN: 7.0772
- nab_score_standard: -3.6238 ± 1.9110
- nab_score_low_fp: -9.1413 ± 2.1408
- nab_score_low_fn: -1.1298 ± 2.1110
- n_ground_truth_sum: 97.0000
- n_detections_sum: 2153.0000
- NAB Scores:
  - nab_score_standard: -3.6238 ± 1.9110
  - nab_score_low_fp: -9.1413 ± 2.1408
  - nab_score_low_fn: -1.1298 ± 2.1110

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma_window=100, min_gap_samples=3000 (score=0.0682)
- F1 Classic best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma_window=50, min_gap_samples=5000 (score=0.0961)
- F3 Classic best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma_window=100, min_gap_samples=3000 (score=0.2860)
- Nab Standard best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=True, ma_window=100, min_gap_samples=3000
- Nab Low Fp best: drift_confidence=0.001, warning_confidence=0.001, two_side_option=False, ma_window=50, min_gap_samples=5000
- Nab Low Fn best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma_window=50, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.0001 | 0.001 | True | 100 | 2000 | 0.2229 |
| 0.0001 | 0.005 | True | 100 | 2000 | 0.2229 |
| 0.0001 | 0.01 | True | 100 | 2000 | 0.2229 |
| 0.0001 | 0.05 | True | 100 | 2000 | 0.2229 |
| 0.001 | 0.001 | True | 50 | 2000 | 0.2226 |
| 0.001 | 0.005 | True | 50 | 2000 | 0.2226 |
| 0.001 | 0.01 | True | 50 | 2000 | 0.2226 |
| 0.001 | 0.05 | True | 50 | 2000 | 0.2226 |
| 0.0001 | 0.001 | False | 10 | 2000 | 0.2217 |
| 0.0001 | 0.005 | False | 10 | 2000 | 0.2217 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.0001 | 0.001 | True | 100 | 3000 | -2.8088 |
| 0.0001 | 0.005 | True | 100 | 3000 | -2.8088 |
| 0.0001 | 0.01 | True | 100 | 3000 | -2.8088 |
| 0.0001 | 0.05 | True | 100 | 3000 | -2.8088 |
| 0.005 | 0.001 | True | 100 | 3000 | -2.8092 |
| 0.005 | 0.005 | True | 100 | 3000 | -2.8092 |
| 0.005 | 0.01 | True | 100 | 3000 | -2.8092 |
| 0.005 | 0.05 | True | 100 | 3000 | -2.8092 |
| 0.0005 | 0.001 | True | 100 | 3000 | -2.8187 |
| 0.0005 | 0.005 | True | 100 | 3000 | -2.8187 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._