# Comparative Report — Temporary Snapshot
Generated: 2025-11-28T15:06:39.409824 UTC
**Dataset**: malignantventricular
---
## Evaluation Summary
- **Total Files**: 22
- **Dataset**: malignantventricular
- **Total Param Combinations**: 384
- **Total Evaluations**: 8448
- **Total Ground Truth Events**: 227328
- **Total Detections**: 3250374
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- lambda_: 80.0
- delta: 0.04
- alpha: 0.9999
- ma_window: 200.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.2559 ± 0.1400
- F3 CLASSIC: 0.2933 ± 0.1780
- F1 WEIGHTED: 0.0913 ± 0.0774
- F1 CLASSIC: 0.1081 ± 0.1019
- RECALL 4S: 0.6934 ± 0.2417
- RECALL 10S: 0.8427 ± 0.2207
- PRECISION 4S: 0.0466 ± 0.0488
- PRECISION 10S: 0.0627 ± 0.0662
- EDD MEDIAN S: 2.6899
- FP PER MIN: 9.1714
- nab_score_standard: -28.1821 ± 17.7007
- nab_score_low_fp: -58.2469 ± 26.8829
- nab_score_low_fn: -23.8315 ± 27.4551
- n_ground_truth_sum: 592.0000
- n_detections_sum: 7787.0000
- NAB Scores:
  - nab_score_standard: -28.1821 ± 17.7007
  - nab_score_low_fp: -58.2469 ± 26.8829
  - nab_score_low_fn: -23.8315 ± 27.4551

## Comparison With Other Metrics
- F1 Weighted best: lambda_=80.0, delta=0.04, alpha=0.99, ma_window=200.0, min_gap_samples=2000.0 (score=0.1002)
- F1 Classic best: lambda_=50.0, delta=0.005, alpha=0.9999, ma_window=200.0, min_gap_samples=2000.0 (score=0.1412)
- F3 Classic best: lambda_=10.0, delta=0.005, alpha=0.99, ma_window=50.0, min_gap_samples=2000.0 (score=0.3431)
- Nab Standard best: lambda_=10.0, delta=0.04, alpha=0.99, ma_window=200.0, min_gap_samples=2000.0
- Nab Low Fp best: lambda_=10.0, delta=0.04, alpha=0.9999, ma_window=200.0, min_gap_samples=4000.0
- Nab Low Fn best: lambda_=10.0, delta=0.04, alpha=0.99, ma_window=50.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| lambda_ | delta | alpha | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 80.0 | 0.04 | 0.9999 | 200 | 1000 | 0.2559 |
| 50.0 | 0.005 | 0.9999 | 200 | 1000 | 0.2558 |
| 80.0 | 0.02 | 0.9999 | 200 | 1000 | 0.2558 |
| 80.0 | 0.005 | 0.9999 | 200 | 1000 | 0.2557 |
| 80.0 | 0.01 | 0.9999 | 200 | 1000 | 0.2557 |
| 30.0 | 0.04 | 0.99 | 200 | 1000 | 0.2555 |
| 50.0 | 0.01 | 0.99 | 200 | 1000 | 0.2555 |
| 50.0 | 0.01 | 0.9999 | 200 | 1000 | 0.2555 |
| 50.0 | 0.02 | 0.99 | 200 | 1000 | 0.2555 |
| 50.0 | 0.04 | 0.99 | 200 | 1000 | 0.2555 |
## Top 10 (NAB Standard)
| lambda_ | delta | alpha | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 10.0 | 0.04 | 0.99 | 200 | 2000 | -20.0441 |
| 10.0 | 0.02 | 0.99 | 200 | 2000 | -20.0633 |
| 10.0 | 0.01 | 0.99 | 200 | 2000 | -20.0646 |
| 10.0 | 0.005 | 0.99 | 200 | 2000 | -20.07 |
| 50.0 | 0.04 | 0.9999 | 200 | 2000 | -20.2032 |
| 50.0 | 0.01 | 0.9999 | 200 | 2000 | -20.2461 |
| 50.0 | 0.005 | 0.9999 | 200 | 2000 | -20.2541 |
| 50.0 | 0.04 | 0.99 | 200 | 2000 | -20.2833 |
| 50.0 | 0.02 | 0.9999 | 200 | 2000 | -20.2864 |
| 30.0 | 0.02 | 0.9999 | 200 | 2000 | -20.3024 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._