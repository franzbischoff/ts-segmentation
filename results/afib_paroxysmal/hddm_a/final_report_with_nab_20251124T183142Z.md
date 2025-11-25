# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:31:42.505172 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 640
- **Total Evaluations**: 146560
- **Total Ground Truth Events**: 832640
- **Total Detections**: 8064700
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- drift_confidence: 0.005
- warning_confidence: 0.001
- two_side_option: True
- ma_window: 1
- min_gap_samples: 1000
- F3 WEIGHTED: 0.3588 ± 0.1948
- F3 CLASSIC: 0.3942 ± 0.2147
- F1 WEIGHTED: 0.1547 ± 0.1423
- F1 CLASSIC: 0.1743 ± 0.1659
- RECALL 4S: 0.6977 ± 0.2924
- RECALL 10S: 0.8878 ± 0.2022
- PRECISION 4S: 0.0747 ± 0.0883
- PRECISION 10S: 0.1136 ± 0.1359
- EDD MEDIAN S: 2.8506
- FP PER MIN: 9.1468
- nab_score_standard: -9.4592 ± 28.5826
- nab_score_low_fp: -20.7645 ± 57.1210
- nab_score_low_fn: -5.4178 ± 14.7714
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 29151.0000
- NAB Scores:
  - nab_score_standard: -9.4592 ± 28.5826
  - nab_score_low_fp: -20.7645 ± 57.1210
  - nab_score_low_fn: -5.4178 ± 14.7714

## Comparison With Other Metrics
- F1 Weighted best: drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma_window=1, min_gap_samples=2000 (score=0.1593)
- F1 Classic best: drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma_window=1, min_gap_samples=2000 (score=0.2147)
- F3 Classic best: drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma_window=1, min_gap_samples=2000 (score=0.4379)
- Nab Standard best: drift_confidence=0.005, warning_confidence=0.001, two_side_option=False, ma_window=1, min_gap_samples=3000
- Nab Low Fp best: drift_confidence=0.0001, warning_confidence=0.001, two_side_option=False, ma_window=100, min_gap_samples=5000
- Nab Low Fn best: drift_confidence=0.005, warning_confidence=0.001, two_side_option=True, ma_window=1, min_gap_samples=2000

## Top 10 (F3-weighted)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.005 | 0.001 | True | 1 | 1000 | 0.3588 |
| 0.005 | 0.005 | True | 1 | 1000 | 0.3588 |
| 0.005 | 0.01 | True | 1 | 1000 | 0.3588 |
| 0.005 | 0.05 | True | 1 | 1000 | 0.3588 |
| 0.005 | 0.001 | False | 1 | 1000 | 0.3538 |
| 0.005 | 0.005 | False | 1 | 1000 | 0.3538 |
| 0.005 | 0.01 | False | 1 | 1000 | 0.3538 |
| 0.005 | 0.05 | False | 1 | 1000 | 0.3538 |
| 0.001 | 0.001 | True | 1 | 1000 | 0.3257 |
| 0.001 | 0.005 | True | 1 | 1000 | 0.3257 |
## Top 10 (NAB Standard)
| drift_confidence | warning_confidence | two_side_option | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.005 | 0.001 | False | 1 | 3000 | -5.1989 |
| 0.005 | 0.005 | False | 1 | 3000 | -5.1989 |
| 0.005 | 0.01 | False | 1 | 3000 | -5.1989 |
| 0.005 | 0.05 | False | 1 | 3000 | -5.1989 |
| 0.005 | 0.001 | True | 1 | 3000 | -5.2117 |
| 0.005 | 0.005 | True | 1 | 3000 | -5.2117 |
| 0.005 | 0.01 | True | 1 | 3000 | -5.2117 |
| 0.005 | 0.05 | True | 1 | 3000 | -5.2117 |
| 0.001 | 0.001 | True | 1 | 3000 | -5.2298 |
| 0.001 | 0.005 | True | 1 | 3000 | -5.2298 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._