# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T12:31:21.786990 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 594
- **Total Evaluations**: 136026
- **Total Ground Truth Events**: 772794
- **Total Detections**: 10967500
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- delta: 0.005
- ma_window: 300.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.3994 ± 0.2159
- F3 CLASSIC: 0.4188 ± 0.2252
- F1 WEIGHTED: 0.1603 ± 0.1468
- F1 CLASSIC: 0.1689 ± 0.1544
- RECALL 4S: 0.7863 ± 0.2627
- RECALL 10S: 0.9777 ± 0.0988
- PRECISION 4S: 0.0714 ± 0.0718
- PRECISION 10S: 0.1020 ± 0.1101
- EDD MEDIAN S: 2.6366
- FP PER MIN: 10.0009
- nab_score_standard: -8.8409 ± 27.7487
- nab_score_low_fp: -20.1729 ± 55.2268
- nab_score_low_fn: -4.4326 ± 14.3788
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 29719.0000
- NAB Scores:
  - nab_score_standard: -8.8409 ± 27.7487
  - nab_score_low_fp: -20.1729 ± 55.2268
  - nab_score_low_fn: -4.4326 ± 14.3788

## Comparison With Other Metrics
- F1 Weighted best: delta=0.005, ma_window=10.0, min_gap_samples=1000.0 (score=0.1682)
- F1 Classic best: delta=0.015, ma_window=300.0, min_gap_samples=2000.0 (score=0.2239)
- F3 Classic best: delta=0.1, ma_window=300.0, min_gap_samples=2000.0 (score=0.4882)
- Nab Standard best: delta=0.05, ma_window=10.0, min_gap_samples=2000.0
- Nab Low Fp best: delta=0.005, ma_window=10.0, min_gap_samples=5000.0
- Nab Low Fn best: delta=0.08, ma_window=100.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| delta | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|
| 0.005 | 300 | 1000 | 0.3994 |
| 0.01 | 300 | 1000 | 0.3993 |
| 0.015 | 250 | 1000 | 0.3993 |
| 0.04 | 100 | 1000 | 0.399 |
| 0.005 | 75 | 1000 | 0.3983 |
| 0.05 | 150 | 1000 | 0.398 |
| 0.015 | 150 | 1000 | 0.3977 |
| 0.025 | 200 | 1000 | 0.3977 |
| 0.025 | 300 | 1000 | 0.3976 |
| 0.015 | 200 | 1000 | 0.3975 |
## Top 10 (NAB Standard)
| delta | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|
| 0.05 | 10 | 2000 | -4.282 |
| 0.025 | 10 | 2000 | -4.2854 |
| 0.04 | 10 | 2000 | -4.2984 |
| 0.005 | 10 | 2000 | -4.3223 |
| 0.08 | 25 | 2000 | -4.3271 |
| 0.01 | 25 | 2000 | -4.3343 |
| 0.1 | 25 | 2000 | -4.3423 |
| 0.005 | 25 | 2000 | -4.3466 |
| 0.08 | 10 | 2000 | -4.3499 |
| 0.02 | 10 | 2000 | -4.3574 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._