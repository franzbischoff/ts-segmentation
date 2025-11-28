# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:59:46.155167 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/afib_paroxysmal/fold_assignments_seed42.json
Fold sizes: {'fold_a': 114, 'fold_b': 115}
---
## FOLD_A
- Records: 114
- Unique files: 114
- Best params: lambda_: 1.0, delta: 0.04, alpha: 0.9999, ma_window: 50.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.4148
- Primary metric in opposite fold: 0.3625
- Generalization gap: 0.05230000000000001
- Cross-fold metrics (opposite fold):
  - lambda_: 1.0
  - delta: 0.04
  - alpha: 0.9999
  - ma_window: 50.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1489
  - f1_classic_std: 0.143
  - f1_classic_count: 115.0
  - f1_weighted_mean: 0.1402
  - f1_weighted_std: 0.1388
  - f1_weighted_count: 115.0
  - f3_classic_mean: 0.3864
  - f3_classic_std: 0.2175
  - f3_classic_count: 115.0
  - f3_weighted_mean: 0.3625
  - f3_weighted_std: 0.2102
  - f3_weighted_count: 115.0
  - recall_4s_mean: 0.723
  - recall_4s_std: 0.2784
  - recall_10s_mean: 0.9433
  - recall_10s_std: 0.1554
  - precision_4s_mean: 0.0623
  - precision_4s_std: 0.0703
  - precision_10s_mean: 0.0888
  - precision_10s_std: 0.1031
  - edd_median_s_mean: 2.7983
  - fp_per_min_mean: 9.9179
  - nab_score_standard_mean: -9.8726
  - nab_score_standard_std: 27.505
  - nab_score_low_fp_mean: -22.1626
  - nab_score_low_fp_std: 54.8623
  - nab_score_low_fn_mean: -4.8145
  - nab_score_low_fn_std: 14.1805
  - n_ground_truth_sum: 589.0
  - n_detections_sum: 15881.0

## FOLD_B
- Records: 115
- Unique files: 115
- Best params: lambda_: 1.0, delta: 0.04, alpha: 0.99, ma_window: 10.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.3654
- Primary metric in opposite fold: 0.4103
- Generalization gap: 0.044899999999999995
- Cross-fold metrics (opposite fold):
  - lambda_: 1.0
  - delta: 0.04
  - alpha: 0.99
  - ma_window: 10.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.164
  - f1_classic_std: 0.1519
  - f1_classic_count: 114.0
  - f1_weighted_mean: 0.1609
  - f1_weighted_std: 0.1475
  - f1_weighted_count: 114.0
  - f3_classic_mean: 0.4171
  - f3_classic_std: 0.2244
  - f3_classic_count: 114.0
  - f3_weighted_mean: 0.4103
  - f3_weighted_std: 0.2189
  - f3_weighted_count: 114.0
  - recall_4s_mean: 0.9103
  - recall_4s_std: 0.1411
  - recall_10s_mean: 0.994
  - recall_10s_std: 0.0477
  - precision_4s_mean: 0.0751
  - precision_4s_std: 0.0686
  - precision_10s_mean: 0.0981
  - precision_10s_std: 0.1067
  - edd_median_s_mean: 2.3203
  - fp_per_min_mean: 11.6625
  - nab_score_standard_mean: -10.6028
  - nab_score_standard_std: 41.9468
  - nab_score_low_fp_mean: -24.0593
  - nab_score_low_fp_std: 83.4419
  - nab_score_low_fn_mean: -5.2166
  - nab_score_low_fn_std: 21.3847
  - n_ground_truth_sum: 712.0
  - n_detections_sum: 17277.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.3654
  - primary_metric_in_opposite_fold: 0.4103
  - generalization_gap: 0.044899999999999995
  - parameter_values: {'lambda_': 1.0, 'delta': 0.04, 'alpha': 0.99, 'ma_window': 10.0, 'min_gap_samples': 1000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.3654
  - primary_metric_in_opposite_fold: 0.4103
  - generalization_gap: 0.044899999999999995
  - parameter_values: {'lambda_': 1.0, 'delta': 0.04, 'alpha': 0.99, 'ma_window': 10.0, 'min_gap_samples': 1000.0}
- Mean Cross Primary Metric:
  - value: 0.38639999999999997