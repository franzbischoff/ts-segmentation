# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:27:06.735172 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 1280
- **Total Evaluations**: 43520
- **Total Ground Truth Events**: 124160
- **Total Detections**: 3190935
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- alpha: 0.05
- window_size: 500.0
- stat_size: 50.0
- ma_window: 100.0
- min_gap_samples: 2000.0
- F3 WEIGHTED: 0.2409 ± 0.1219
- F3 CLASSIC: 0.2926 ± 0.1537
- F1 WEIGHTED: 0.0715 ± 0.0527
- F1 CLASSIC: 0.0882 ± 0.0694
- RECALL 4S: 0.5620 ± 0.3782
- RECALL 10S: 0.9804 ± 0.1143
- PRECISION 4S: 0.0253 ± 0.0229
- PRECISION 10S: 0.0477 ± 0.0407
- EDD MEDIAN S: 3.6699
- FP PER MIN: 6.3386
- nab_score_standard: -3.1356 ± 1.9814
- nab_score_low_fp: -8.0749 ± 2.1853
- nab_score_low_fn: -0.9895 ± 2.6171
- n_ground_truth_sum: 97.0000
- n_detections_sum: 1938.0000
- NAB Scores:
  - nab_score_standard: -3.1356 ± 1.9814
  - nab_score_low_fp: -8.0749 ± 2.1853
  - nab_score_low_fn: -0.9895 ± 2.6171

## Comparison With Other Metrics
- F1 Weighted best: alpha=0.001, window_size=500.0, stat_size=30.0, ma_window=10.0, min_gap_samples=3000.0 (score=0.0783)
- F1 Classic best: alpha=0.005, window_size=500.0, stat_size=20.0, ma_window=100.0, min_gap_samples=3000.0 (score=0.1097)
- F3 Classic best: alpha=0.005, window_size=500.0, stat_size=20.0, ma_window=100.0, min_gap_samples=3000.0 (score=0.3269)
- Nab Standard best: alpha=0.005, window_size=500.0, stat_size=50.0, ma_window=100.0, min_gap_samples=5000.0
- Nab Low Fp best: alpha=0.001, window_size=50.0, stat_size=50.0, ma_window=1.0, min_gap_samples=500.0
- Nab Low Fn best: alpha=0.001, window_size=500.0, stat_size=50.0, ma_window=10.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| alpha | window_size | stat_size | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.05 | 500 | 50 | 100 | 2000 | 0.2409 |
| 0.05 | 200 | 100 | 50 | 2000 | 0.2378 |
| 0.001 | 500 | 50 | 10 | 2000 | 0.2373 |
| 0.01 | 500 | 50 | 50 | 2000 | 0.2365 |
| 0.005 | 500 | 50 | 100 | 2000 | 0.236 |
| 0.005 | 200 | 100 | 50 | 2000 | 0.2358 |
| 0.01 | 500 | 50 | 100 | 2000 | 0.2356 |
| 0.005 | 500 | 50 | 50 | 2000 | 0.2355 |
| 0.01 | 100 | 50 | 10 | 2000 | 0.2351 |
| 0.001 | 500 | 50 | 50 | 2000 | 0.234 |
## Top 10 (NAB Standard)
| alpha | window_size | stat_size | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.005 | 500 | 50 | 100 | 5000 | -2.2784 |
| 0.05 | 500 | 50 | 1 | 5000 | -2.3043 |
| 0.01 | 500 | 50 | 100 | 5000 | -2.325 |
| 0.05 | 500 | 50 | 100 | 5000 | -2.3683 |
| 0.01 | 500 | 50 | 50 | 5000 | -2.3774 |
| 0.001 | 500 | 50 | 50 | 5000 | -2.384 |
| 0.05 | 500 | 50 | 50 | 5000 | -2.4017 |
| 0.001 | 500 | 50 | 100 | 5000 | -2.4229 |
| 0.005 | 500 | 20 | 100 | 3000 | -2.4274 |
| 0.05 | 500 | 20 | 10 | 3000 | -2.4517 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._