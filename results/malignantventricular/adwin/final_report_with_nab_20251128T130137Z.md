# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T13:01:37.637786 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 495
- **Total Evaluations**: 10890
- **Total Ground Truth Events**: 293040
- **Total Detections**: 2044932
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- delta: 0.1
- ma_window: 150.0
- min_gap_samples: 2000.0
- F3 WEIGHTED: 0.2641 ± 0.1196
- F3 CLASSIC: 0.3471 ± 0.1515
- F1 WEIGHTED: 0.0959 ± 0.0624
- F1 CLASSIC: 0.1316 ± 0.1004
- RECALL 4S: 0.4837 ± 0.1103
- RECALL 10S: 0.8974 ± 0.1609
- PRECISION 4S: 0.0459 ± 0.0495
- PRECISION 10S: 0.0797 ± 0.0767
- EDD MEDIAN S: 4.3835
- FP PER MIN: 6.3429
- nab_score_standard: -20.7667 ± 15.1843
- nab_score_low_fp: -41.3635 ± 14.9346
- nab_score_low_fn: -22.0592 ± 35.9958
- n_ground_truth_sum: 592.0000
- n_detections_sum: 5367.0000
- NAB Scores:
  - nab_score_standard: -20.7667 ± 15.1843
  - nab_score_low_fp: -41.3635 ± 14.9346
  - nab_score_low_fn: -22.0592 ± 35.9958

## Comparison With Other Metrics
- F1 Weighted best: delta=0.005, ma_window=10.0, min_gap_samples=1000.0 (score=0.0995)
- F1 Classic best: delta=0.02, ma_window=75.0, min_gap_samples=2000.0 (score=0.1417)
- F3 Classic best: delta=0.025, ma_window=100.0, min_gap_samples=2000.0 (score=0.3566)
- Nab Standard best: delta=0.02, ma_window=75.0, min_gap_samples=2000.0
- Nab Low Fp best: delta=0.01, ma_window=25.0, min_gap_samples=4000.0
- Nab Low Fn best: delta=0.015, ma_window=150.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| delta | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|
| 0.1 | 150 | 2000 | 0.2641 |
| 0.06 | 200 | 2000 | 0.2614 |
| 0.02 | 250 | 2000 | 0.261 |
| 0.06 | 100 | 1000 | 0.2608 |
| 0.02 | 200 | 1000 | 0.2603 |
| 0.02 | 100 | 1000 | 0.26 |
| 0.04 | 100 | 1000 | 0.26 |
| 0.005 | 200 | 2000 | 0.2597 |
| 0.005 | 200 | 1000 | 0.2592 |
| 0.05 | 200 | 2000 | 0.2592 |
## Top 10 (NAB Standard)
| delta | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|
| 0.02 | 75 | 2000 | -18.9256 |
| 0.025 | 100 | 2000 | -19.4143 |
| 0.08 | 75 | 2000 | -19.4487 |
| 0.1 | 75 | 2000 | -19.5897 |
| 0.025 | 75 | 2000 | -19.7447 |
| 0.04 | 100 | 2000 | -19.7529 |
| 0.02 | 75 | 3000 | -19.7619 |
| 0.015 | 100 | 2000 | -19.7666 |
| 0.03 | 100 | 2000 | -19.8304 |
| 0.01 | 100 | 2000 | -19.8505 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._