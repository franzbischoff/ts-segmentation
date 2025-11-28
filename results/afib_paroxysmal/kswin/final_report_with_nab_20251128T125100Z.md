# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T12:51:00.666990 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 1280
- **Total Evaluations**: 293120
- **Total Ground Truth Events**: 1665280
- **Total Detections**: 30499750
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- alpha: 0.005
- window_size: 500.0
- stat_size: 50.0
- ma_window: 50.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.4135 ± 0.2116
- F3 CLASSIC: 0.4348 ± 0.2260
- F1 WEIGHTED: 0.1670 ± 0.1515
- F1 CLASSIC: 0.1765 ± 0.1624
- RECALL 4S: 0.7462 ± 0.2605
- RECALL 10S: 0.9944 ± 0.0303
- PRECISION 4S: 0.0719 ± 0.0745
- PRECISION 10S: 0.1074 ± 0.1183
- EDD MEDIAN S: 2.8931
- FP PER MIN: 9.4279
- nab_score_standard: -9.4336 ± 35.8361
- nab_score_low_fp: -21.4551 ± 71.4529
- nab_score_low_fn: -4.6499 ± 18.2335
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 30606.0000
- NAB Scores:
  - nab_score_standard: -9.4336 ± 35.8361
  - nab_score_low_fp: -21.4551 ± 71.4529
  - nab_score_low_fn: -4.6499 ± 18.2335

## Comparison With Other Metrics
- F1 Weighted best: alpha=0.005, window_size=500.0, stat_size=100.0, ma_window=1.0, min_gap_samples=2000.0 (score=0.1700)
- F1 Classic best: alpha=0.001, window_size=500.0, stat_size=20.0, ma_window=10.0, min_gap_samples=2000.0 (score=0.2261)
- F3 Classic best: alpha=0.01, window_size=500.0, stat_size=50.0, ma_window=10.0, min_gap_samples=2000.0 (score=0.4948)
- Nab Standard best: alpha=0.005, window_size=200.0, stat_size=20.0, ma_window=50.0, min_gap_samples=3000.0
- Nab Low Fp best: alpha=0.001, window_size=50.0, stat_size=50.0, ma_window=1.0, min_gap_samples=500.0
- Nab Low Fn best: alpha=0.01, window_size=500.0, stat_size=50.0, ma_window=10.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| alpha | window_size | stat_size | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.005 | 500 | 50 | 50 | 1000 | 0.4135 |
| 0.005 | 500 | 50 | 10 | 1000 | 0.4133 |
| 0.01 | 500 | 50 | 100 | 1000 | 0.4132 |
| 0.05 | 500 | 50 | 50 | 1000 | 0.413 |
| 0.001 | 500 | 20 | 1 | 1000 | 0.4128 |
| 0.01 | 500 | 50 | 1 | 1000 | 0.4128 |
| 0.005 | 500 | 50 | 100 | 1000 | 0.4127 |
| 0.01 | 500 | 50 | 50 | 1000 | 0.4127 |
| 0.05 | 500 | 50 | 100 | 1000 | 0.4124 |
| 0.001 | 500 | 50 | 50 | 1000 | 0.4123 |
## Top 10 (NAB Standard)
| alpha | window_size | stat_size | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.005 | 200 | 20 | 50 | 3000 | -5.2573 |
| 0.001 | 200 | 30 | 100 | 3000 | -5.2641 |
| 0.001 | 500 | 20 | 10 | 3000 | -5.269 |
| 0.001 | 200 | 30 | 10 | 3000 | -5.2711 |
| 0.01 | 200 | 20 | 50 | 3000 | -5.2766 |
| 0.001 | 200 | 30 | 1 | 3000 | -5.2947 |
| 0.005 | 200 | 20 | 100 | 3000 | -5.2973 |
| 0.05 | 100 | 20 | 10 | 3000 | -5.3011 |
| 0.01 | 200 | 30 | 50 | 3000 | -5.304 |
| 0.001 | 200 | 20 | 1 | 3000 | -5.3091 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._