# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T13:46:28.931634 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 25920
- **Total Evaluations**: 5935680
- **Total Ground Truth Events**: 33721920
- **Total Detections**: 87197121
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- window_size: 75.0
- regime_threshold: 0.7
- regime_landmark: 4.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.4776 ± 0.2274
- F3 CLASSIC: 0.5242 ± 0.2378
- F1 WEIGHTED: 0.3397 ± 0.2065
- F1 CLASSIC: 0.3754 ± 0.2227
- RECALL 4S: 0.4958 ± 0.2884
- RECALL 10S: 0.6499 ± 0.2749
- PRECISION 4S: 0.2264 ± 0.1965
- PRECISION 10S: 0.3169 ± 0.2386
- EDD MEDIAN S: 3.2786
- FP PER MIN: 1.4215
- nab_score_standard: -1.6124 ± 4.9029
- nab_score_low_fp: -3.1104 ± 7.6493
- nab_score_low_fn: -3.5926 ± 7.5980
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 4244.0000
- NAB Scores:
  - nab_score_standard: -1.6124 ± 4.9029
  - nab_score_low_fp: -3.1104 ± 7.6493
  - nab_score_low_fn: -3.5926 ± 7.5980

## Comparison With Other Metrics
- F1 Weighted best: window_size=125.0, regime_threshold=0.55, regime_landmark=5.0, min_gap_samples=1000.0 (score=0.3757)
- F1 Classic best: window_size=75.0, regime_threshold=0.65, regime_landmark=8.5, min_gap_samples=2000.0 (score=0.4601)
- F3 Classic best: window_size=75.0, regime_threshold=0.7, regime_landmark=7.5, min_gap_samples=500.0 (score=0.5786)
- Nab Standard best: window_size=50.0, regime_threshold=0.75, regime_landmark=4.5, min_gap_samples=1000.0
- Nab Low Fp best: window_size=75.0, regime_threshold=0.7, regime_landmark=7.5, min_gap_samples=2000.0
- Nab Low Fn best: window_size=50.0, regime_threshold=0.8, regime_landmark=3.5, min_gap_samples=500.0

## Top 10 (F3-weighted)
| window_size | regime_threshold | regime_landmark | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|
| 75 | 0.7 | 4.0 | 1000 | 0.4776 |
| 50 | 0.75 | 4.0 | 500 | 0.4773 |
| 75 | 0.7 | 4.0 | 200 | 0.477 |
| 75 | 0.7 | 4.0 | 500 | 0.4769 |
| 75 | 0.7 | 5.0 | 200 | 0.4769 |
| 100 | 0.7 | 4.0 | 500 | 0.4769 |
| 50 | 0.75 | 4.5 | 500 | 0.4759 |
| 50 | 0.75 | 3.5 | 500 | 0.475 |
| 50 | 0.75 | 4.5 | 1000 | 0.475 |
| 125 | 0.65 | 5.5 | 200 | 0.4748 |
## Top 10 (NAB Standard)
| window_size | regime_threshold | regime_landmark | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|
| 50 | 0.75 | 4.5 | 1000 | -1.4142 |
| 50 | 0.75 | 5.0 | 1000 | -1.4567 |
| 75 | 0.7 | 4.5 | 1000 | -1.5106 |
| 75 | 0.7 | 7.0 | 1000 | -1.5112 |
| 100 | 0.7 | 6.5 | 1000 | -1.5124 |
| 75 | 0.7 | 5.5 | 1000 | -1.5146 |
| 75 | 0.75 | 7.0 | 1000 | -1.5163 |
| 75 | 0.75 | 6.5 | 1000 | -1.5286 |
| 50 | 0.75 | 4.5 | 500 | -1.5303 |
| 50 | 0.75 | 5.5 | 1000 | -1.5311 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._