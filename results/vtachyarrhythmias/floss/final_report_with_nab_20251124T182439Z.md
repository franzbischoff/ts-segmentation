# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:24:39.373216 UTC
**Dataset**: vtachyarrhythmias
---
## Evaluation Summary
- **Total Files**: 34
- **Dataset**: vtachyarrhythmias
- **Total Param Combinations**: 25920
- **Total Evaluations**: 881280
- **Total Ground Truth Events**: 2514240
- **Total Detections**: 12962887
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- window_size: 75.0
- regime_threshold: 0.45
- regime_landmark: 3.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.5440 ± 0.2213
- F3 CLASSIC: 0.5865 ± 0.2332
- F1 WEIGHTED: 0.3158 ± 0.1707
- F1 CLASSIC: 0.3445 ± 0.1898
- RECALL 4S: 0.6644 ± 0.3529
- RECALL 10S: 0.7971 ± 0.3020
- PRECISION 4S: 0.1950 ± 0.1743
- PRECISION 10S: 0.2608 ± 0.2119
- EDD MEDIAN S: 2.8949
- FP PER MIN: 0.8634
- nab_score_standard: 0.1580 ± 1.4098
- nab_score_low_fp: -0.5569 ± 1.6008
- nab_score_low_fn: -0.3668 ± 2.5193
- n_ground_truth_sum: 97.0000
- n_detections_sum: 327.0000
- NAB Scores:
  - nab_score_standard: 0.1580 ± 1.4098
  - nab_score_low_fp: -0.5569 ± 1.6008
  - nab_score_low_fn: -0.3668 ± 2.5193

## Comparison With Other Metrics
- F1 Weighted best: window_size=125.0, regime_threshold=0.25, regime_landmark=3.5, min_gap_samples=2000.0 (score=0.3720)
- F1 Classic best: window_size=125.0, regime_threshold=0.25, regime_landmark=3.5, min_gap_samples=2000.0 (score=0.4133)
- F3 Classic best: window_size=125.0, regime_threshold=0.3, regime_landmark=3.5, min_gap_samples=2000.0 (score=0.5956)
- Nab Standard best: window_size=75.0, regime_threshold=0.45, regime_landmark=3.0, min_gap_samples=500.0
- Nab Low Fp best: window_size=75.0, regime_threshold=0.45, regime_landmark=3.0, min_gap_samples=1000.0
- Nab Low Fn best: window_size=150.0, regime_threshold=0.6, regime_landmark=4.0, min_gap_samples=1000.0

## Top 10 (F3-weighted)
| window_size | regime_threshold | regime_landmark | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|
| 75 | 0.45 | 3.0 | 1000 | 0.544 |
| 100 | 0.3 | 2.0 | 500 | 0.5431 |
| 125 | 0.35 | 3.5 | 2000 | 0.5415 |
| 100 | 0.3 | 3.5 | 1000 | 0.5409 |
| 125 | 0.3 | 3.5 | 2000 | 0.5406 |
| 125 | 0.3 | 3.5 | 1000 | 0.5392 |
| 75 | 0.45 | 3.0 | 500 | 0.5391 |
| 125 | 0.3 | 3.5 | 500 | 0.5378 |
| 125 | 0.35 | 3.5 | 1000 | 0.5375 |
| 125 | 0.3 | 3.5 | 3000 | 0.5374 |
## Top 10 (NAB Standard)
| window_size | regime_threshold | regime_landmark | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|
| 75 | 0.45 | 3.0 | 500 | 0.1824 |
| 75 | 0.45 | 3.0 | 1000 | 0.158 |
| 100 | 0.4 | 2.5 | 500 | 0.1561 |
| 100 | 0.4 | 2.5 | 200 | 0.1078 |
| 100 | 0.35 | 2.0 | 500 | 0.0556 |
| 75 | 0.45 | 3.0 | 200 | 0.054 |
| 100 | 0.4 | 3.5 | 500 | 0.0401 |
| 100 | 0.35 | 3.0 | 500 | 0.0342 |
| 100 | 0.35 | 2.0 | 200 | 0.017 |
| 75 | 0.45 | 2.0 | 500 | 0.0129 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._