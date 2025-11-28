# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T12:14:20.896263 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 384
- **Total Evaluations**: 13056
- **Total Ground Truth Events**: 37248
- **Total Detections**: 1407507
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- lambda_: 10.0
- delta: 0.005
- alpha: 0.9999
- ma_window: 200.0
- min_gap_samples: 2000.0
- F3 WEIGHTED: 0.2295 ± 0.1309
- F3 CLASSIC: 0.2789 ± 0.1487
- F1 WEIGHTED: 0.0685 ± 0.0551
- F1 CLASSIC: 0.0834 ± 0.0650
- RECALL 4S: 0.5056 ± 0.3883
- RECALL 10S: 0.9660 ± 0.1267
- PRECISION 4S: 0.0251 ± 0.0264
- PRECISION 10S: 0.0450 ± 0.0378
- EDD MEDIAN S: 3.9130
- FP PER MIN: 6.6992
- nab_score_standard: -3.3804 ± 1.9981
- nab_score_low_fp: -8.5780 ± 2.2477
- nab_score_low_fn: -1.1051 ± 2.3741
- n_ground_truth_sum: 97.0000
- n_detections_sum: 2043.0000
- NAB Scores:
  - nab_score_standard: -3.3804 ± 1.9981
  - nab_score_low_fp: -8.5780 ± 2.2477
  - nab_score_low_fn: -1.1051 ± 2.3741

## Comparison With Other Metrics
- F1 Weighted best: lambda_=30.0, delta=0.02, alpha=0.9999, ma_window=200.0, min_gap_samples=4000.0 (score=0.0711)
- F1 Classic best: lambda_=50.0, delta=0.005, alpha=0.99, ma_window=200.0, min_gap_samples=4000.0 (score=0.1054)
- F3 Classic best: lambda_=50.0, delta=0.005, alpha=0.99, ma_window=200.0, min_gap_samples=4000.0 (score=0.2839)
- Nab Standard best: lambda_=30.0, delta=0.02, alpha=0.9999, ma_window=200.0, min_gap_samples=4000.0
- Nab Low Fp best: lambda_=30.0, delta=0.02, alpha=0.9999, ma_window=200.0, min_gap_samples=4000.0
- Nab Low Fn best: lambda_=80.0, delta=0.01, alpha=0.9999, ma_window=50.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| lambda_ | delta | alpha | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 10.0 | 0.005 | 0.9999 | 200 | 2000 | 0.2295 |
| 10.0 | 0.01 | 0.9999 | 200 | 2000 | 0.2295 |
| 10.0 | 0.04 | 0.99 | 200 | 2000 | 0.2291 |
| 80.0 | 0.01 | 0.9999 | 50 | 2000 | 0.2291 |
| 80.0 | 0.02 | 0.9999 | 50 | 2000 | 0.2291 |
| 80.0 | 0.04 | 0.9999 | 50 | 2000 | 0.2291 |
| 10.0 | 0.005 | 0.99 | 200 | 2000 | 0.2288 |
| 10.0 | 0.01 | 0.99 | 200 | 2000 | 0.2288 |
| 10.0 | 0.02 | 0.99 | 200 | 2000 | 0.2288 |
| 10.0 | 0.02 | 0.9999 | 200 | 2000 | 0.2283 |
## Top 10 (NAB Standard)
| lambda_ | delta | alpha | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 30.0 | 0.02 | 0.9999 | 200 | 4000 | -2.4641 |
| 30.0 | 0.04 | 0.9999 | 200 | 4000 | -2.4641 |
| 30.0 | 0.005 | 0.99 | 200 | 4000 | -2.4915 |
| 30.0 | 0.01 | 0.99 | 200 | 4000 | -2.4915 |
| 50.0 | 0.005 | 0.9999 | 200 | 4000 | -2.4937 |
| 50.0 | 0.01 | 0.9999 | 200 | 4000 | -2.4937 |
| 50.0 | 0.02 | 0.9999 | 200 | 4000 | -2.4937 |
| 50.0 | 0.04 | 0.9999 | 200 | 4000 | -2.4937 |
| 50.0 | 0.005 | 0.99 | 200 | 4000 | -2.5049 |
| 50.0 | 0.01 | 0.99 | 200 | 4000 | -2.5049 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._