# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T13:51:34.558902 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 1280
- **Total Evaluations**: 28160
- **Total Ground Truth Events**: 757760
- **Total Detections**: 8504522
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- alpha: 0.01
- window_size: 500.0
- stat_size: 20.0
- ma_window: 100.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.2699 ± 0.1302
- F3 CLASSIC: 0.3071 ± 0.1677
- F1 WEIGHTED: 0.0901 ± 0.0682
- F1 CLASSIC: 0.1085 ± 0.1027
- RECALL 4S: 0.7562 ± 0.1674
- RECALL 10S: 0.9531 ± 0.1166
- PRECISION 4S: 0.0458 ± 0.0484
- PRECISION 10S: 0.0632 ± 0.0703
- EDD MEDIAN S: 2.9456
- FP PER MIN: 9.5130
- nab_score_standard: -27.9980 ± 13.7875
- nab_score_low_fp: -59.1191 ± 14.5709
- nab_score_low_fn: -22.3465 ± 29.1008
- n_ground_truth_sum: 592.0000
- n_detections_sum: 8010.0000
- NAB Scores:
  - nab_score_standard: -27.9980 ± 13.7875
  - nab_score_low_fp: -59.1191 ± 14.5709
  - nab_score_low_fn: -22.3465 ± 29.1008

## Comparison With Other Metrics
- F1 Weighted best: alpha=0.01, window_size=200.0, stat_size=30.0, ma_window=1.0, min_gap_samples=5000.0 (score=0.1010)
- F1 Classic best: alpha=0.005, window_size=200.0, stat_size=30.0, ma_window=50.0, min_gap_samples=3000.0 (score=0.1412)
- F3 Classic best: alpha=0.001, window_size=500.0, stat_size=20.0, ma_window=1.0, min_gap_samples=2000.0 (score=0.3531)
- Nab Standard best: alpha=0.05, window_size=500.0, stat_size=30.0, ma_window=10.0, min_gap_samples=2000.0
- Nab Low Fp best: alpha=0.001, window_size=50.0, stat_size=50.0, ma_window=1.0, min_gap_samples=500.0
- Nab Low Fn best: alpha=0.001, window_size=500.0, stat_size=100.0, ma_window=1.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| alpha | window_size | stat_size | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 0.01 | 500 | 20 | 100 | 1000 | 0.2699 |
| 0.05 | 500 | 30 | 50 | 1000 | 0.2693 |
| 0.05 | 500 | 20 | 10 | 1000 | 0.2684 |
| 0.05 | 500 | 30 | 100 | 1000 | 0.2683 |
| 0.001 | 500 | 30 | 10 | 1000 | 0.2682 |
| 0.01 | 500 | 30 | 100 | 1000 | 0.2681 |
| 0.001 | 500 | 30 | 100 | 1000 | 0.2675 |
| 0.001 | 500 | 30 | 50 | 1000 | 0.2674 |
| 0.005 | 500 | 20 | 100 | 1000 | 0.2674 |
| 0.01 | 200 | 20 | 50 | 2000 | 0.2673 |
## Top 10 (NAB Standard)
| alpha | window_size | stat_size | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 0.05 | 500 | 30 | 10 | 2000 | -19.7894 |
| 0.01 | 500 | 30 | 50 | 2000 | -19.9541 |
| 0.005 | 500 | 30 | 100 | 2000 | -19.9949 |
| 0.001 | 500 | 20 | 1 | 2000 | -20.0362 |
| 0.005 | 500 | 30 | 50 | 2000 | -20.1137 |
| 0.001 | 500 | 20 | 10 | 2000 | -20.1448 |
| 0.05 | 500 | 20 | 100 | 2000 | -20.2649 |
| 0.001 | 500 | 30 | 100 | 2000 | -20.2739 |
| 0.05 | 500 | 30 | 1 | 2000 | -20.2905 |
| 0.01 | 500 | 30 | 100 | 2000 | -20.3289 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._