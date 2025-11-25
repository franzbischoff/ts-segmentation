# Comparative Report — Temporary Snapshot
Generated: 2025-11-24T18:29:42.624447 UTC
**Dataset**: afib_paroxysmal
---
## Evaluation Summary
- **Total Files**: 229
- **Dataset**: afib_paroxysmal
- **Total Param Combinations**: 600
- **Total Evaluations**: 137400
- **Total Ground Truth Events**: 780600
- **Total Detections**: 6277641
## Best Parameter Configurations
### BEST GLOBAL PARAMETERS (F3 Weighted Primary Metric)
- lambda_: 1.0
- delta: 0.04
- alpha: 0.9999
- ma_window: 50.0
- min_gap_samples: 1000.0
- F3 WEIGHTED: 0.3885 ± 0.2117
- F3 CLASSIC: 0.4162 ± 0.2210
- F1 WEIGHTED: 0.1551 ± 0.1432
- F1 CLASSIC: 0.1661 ± 0.1517
- RECALL 4S: 0.7293 ± 0.2623
- RECALL 10S: 0.9540 ± 0.1289
- PRECISION 4S: 0.0686 ± 0.0705
- PRECISION 10S: 0.1002 ± 0.1096
- EDD MEDIAN S: 2.8280
- FP PER MIN: 9.7266
- nab_score_standard: -9.3331 ± 32.9592
- nab_score_low_fp: -21.0545 ± 65.6269
- nab_score_low_fn: -4.7868 ± 16.8733
- n_ground_truth_sum: 1301.0000
- n_detections_sum: 30132.0000
- NAB Scores:
  - nab_score_standard: -9.3331 ± 32.9592
  - nab_score_low_fp: -21.0545 ± 65.6269
  - nab_score_low_fn: -4.7868 ± 16.8733

## Comparison With Other Metrics
- F1 Weighted best: lambda_=1.0, delta=0.001, alpha=0.9999, ma_window=50.0, min_gap_samples=2000.0 (score=0.1626)
- F1 Classic best: lambda_=1.0, delta=0.04, alpha=0.99, ma_window=50.0, min_gap_samples=2000.0 (score=0.2168)
- F3 Classic best: lambda_=1.0, delta=0.02, alpha=0.99, ma_window=10.0, min_gap_samples=2000.0 (score=0.4770)
- Nab Standard best: lambda_=1.0, delta=0.02, alpha=0.9999, ma_window=50.0, min_gap_samples=4000.0
- Nab Low Fp best: lambda_=80.0, delta=0.005, alpha=0.99, ma_window=200.0, min_gap_samples=4000.0
- Nab Low Fn best: lambda_=1.0, delta=0.001, alpha=0.9999, ma_window=10.0, min_gap_samples=2000.0

## Top 10 (F3-weighted)
| lambda_ | delta | alpha | ma_window | min_gap_samples | f3_weighted_mean |
|---|---|---|---|---|---|
| 1.0 | 0.04 | 0.9999 | 50 | 1000 | 0.3885 |
| 1.0 | 0.001 | 0.9999 | 50 | 1000 | 0.3884 |
| 1.0 | 0.04 | 0.99 | 10 | 1000 | 0.3878 |
| 1.0 | 0.04 | 0.9999 | 10 | 1000 | 0.3876 |
| 1.0 | 0.02 | 0.9999 | 50 | 1000 | 0.3875 |
| 1.0 | 0.01 | 0.9999 | 50 | 1000 | 0.3873 |
| 1.0 | 0.02 | 0.99 | 50 | 1000 | 0.3872 |
| 1.0 | 0.005 | 0.9999 | 50 | 1000 | 0.3871 |
| 1.0 | 0.001 | 0.99 | 50 | 1000 | 0.387 |
| 1.0 | 0.005 | 0.99 | 50 | 1000 | 0.387 |
## Top 10 (NAB Standard)
| lambda_ | delta | alpha | ma_window | min_gap_samples | nab_score_standard_mean |
|---|---|---|---|---|---|
| 1.0 | 0.02 | 0.9999 | 50 | 4000 | -5.2182 |
| 30.0 | 0.01 | 0.9999 | 10 | 2000 | -5.2258 |
| 10.0 | 0.001 | 0.99 | 10 | 4000 | -5.2333 |
| 10.0 | 0.04 | 0.99 | 10 | 2000 | -5.2434 |
| 1.0 | 0.001 | 0.9999 | 50 | 4000 | -5.2452 |
| 30.0 | 0.005 | 0.9999 | 10 | 2000 | -5.2494 |
| 10.0 | 0.02 | 0.99 | 10 | 4000 | -5.2629 |
| 10.0 | 0.04 | 0.9999 | 10 | 4000 | -5.2841 |
| 30.0 | 0.01 | 0.9999 | 50 | 2000 | -5.2867 |
| 10.0 | 0.02 | 0.99 | 10 | 2000 | -5.2871 |
---
_This is a temporary snapshot created to avoid overwriting final reports. It includes the main summary and top configurations._