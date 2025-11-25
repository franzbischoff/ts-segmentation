# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:25:41.476555 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 495
- **Total Evaluations**: 16830
- **Total Ground Truth Events**: 48015
- **Total Detections**: 820945
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- delta: 0.025
- ma_window: 250.0
- min_gap_samples: 2000.0
- F3 WEIGHTED: 0.2367 ± 0.1230
- F3 CLASSIC: 0.2768 ± 0.1529
- F1 WEIGHTED: 0.0693 ± 0.0509
- F1 CLASSIC: 0.0824 ± 0.0658
- RECALL 4S: 0.6350 ± 0.3447
- RECALL 10S: 0.9575 ± 0.1388
- PRECISION 4S: 0.0255 ± 0.0194
- PRECISION 10S: 0.0444 ± 0.0381
- EDD MEDIAN S: 3.4119
- FP PER MIN: 6.7720
- nab_score_standard: -3.3973 ± 1.8588
- nab_score_low_fp: -8.6368 ± 2.0690
- nab_score_low_fn: -1.1011 ± 2.1555
- n_ground_truth_sum: 97.0000
- n_detections_sum: 2061.0000
- NAB Scores:
  - nab_score_standard: -3.3973 ± 1.8588
  - nab_score_low_fp: -8.6368 ± 2.0690
  - nab_score_low_fn: -1.1011 ± 2.1555

## Comparison With Other Metrics
- F1 Weighted best: delta=0.005, ma_window=10.0, min_gap_samples=4000.0 (score=0.0884)
- F1 Classic best: delta=0.005, ma_window=10.0, min_gap_samples=4000.0 (score=0.1246)
- F3 Classic best: delta=0.06, ma_window=200.0, min_gap_samples=3000.0 (score=0.3109)
- Nab Standard best: delta=0.005, ma_window=10.0, min_gap_samples=4000.0
- Nab Low Fp best: delta=0.005, ma_window=10.0, min_gap_samples=4000.0
- Nab Low Fn best: delta=0.1, ma_window=150.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| delta | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|
| 0.025 | 250 | 2000 | 0.2367 |
| 0.1 | 25 | 3000 | 0.2331 |
| 0.08 | 25 | 3000 | 0.2319 |
| 0.1 | 150 | 2000 | 0.2287 |
| 0.02 | 200 | 2000 | 0.2275 |
| 0.06 | 25 | 3000 | 0.2274 |
| 0.01 | 150 | 2000 | 0.226 |
| 0.02 | 250 | 2000 | 0.2257 |
| 0.1 | 75 | 2000 | 0.2256 |
| 0.05 | 150 | 2000 | 0.2253 |
## Top 10 (NAB Standard)
| delta | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|
| 0.005 | 10 | 4000 | -1.8779 |
| 0.04 | 10 | 3000 | -1.8993 |
| 0.08 | 25 | 3000 | -2.0204 |
| 0.05 | 10 | 3000 | -2.0731 |
| 0.04 | 25 | 3000 | -2.0756 |
| 0.04 | 10 | 4000 | -2.0812 |
| 0.01 | 10 | 2000 | -2.1321 |
| 0.06 | 25 | 5000 | -2.1323 |
| 0.03 | 10 | 2000 | -2.1502 |
| 0.04 | 10 | 2000 | -2.1536 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._