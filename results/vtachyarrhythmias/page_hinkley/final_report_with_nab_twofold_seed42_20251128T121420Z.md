# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:14:20.956746 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: lambda_: 30.0, delta: 0.005, alpha: 0.99, ma_window: 200.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2576
- Primary metric in opposite fold: 0.1943
- Generalization gap: 0.0633
- Cross-fold metrics (opposite fold):
  - lambda_: 30.0
  - delta: 0.005
  - alpha: 0.99
  - ma_window: 200.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.0695
  - f1_classic_std: 0.0527
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.0543
  - f1_weighted_std: 0.0371
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.2432
  - f3_classic_std: 0.1254
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.1943
  - f3_weighted_std: 0.0937
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.5147
  - recall_4s_std: 0.4231
  - recall_10s_mean: 0.9379
  - recall_10s_std: 0.1756
  - precision_4s_mean: 0.0202
  - precision_4s_std: 0.0194
  - precision_10s_mean: 0.0372
  - precision_10s_std: 0.0303
  - edd_median_s_mean: 3.9714
  - fp_per_min_mean: 6.6437
  - nab_score_standard_mean: -3.7462
  - nab_score_standard_std: 1.763
  - nab_score_low_fp_mean: -8.915
  - nab_score_low_fp_std: 1.8608
  - nab_score_low_fn_mean: -1.5147
  - nab_score_low_fn_std: 2.61
  - n_ground_truth_sum: 43.0
  - n_detections_sum: 1001.0

## FOLD_B
- Records: 17
- Unique files: 17
- Best params: lambda_: 10.0, delta: 0.005, alpha: 0.99, ma_window: 200.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2019
- Primary metric in opposite fold: 0.2557
- Generalization gap: 0.05379999999999999
- Cross-fold metrics (opposite fold):
  - lambda_: 10.0
  - delta: 0.005
  - alpha: 0.99
  - ma_window: 200.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.0975
  - f1_classic_std: 0.0738
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.0794
  - f1_weighted_std: 0.0632
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.3156
  - f3_classic_std: 0.1636
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.2557
  - f3_weighted_std: 0.1482
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.5235
  - recall_4s_std: 0.3869
  - recall_10s_mean: 0.9941
  - recall_10s_std: 0.0243
  - precision_4s_mean: 0.0293
  - precision_4s_std: 0.0304
  - precision_10s_mean: 0.053
  - precision_10s_std: 0.0432
  - edd_median_s_mean: 4.2044
  - fp_per_min_mean: 6.7061
  - nab_score_standard_mean: -3.0521
  - nab_score_standard_std: 2.0497
  - nab_score_low_fp_mean: -8.2465
  - nab_score_low_fp_std: 2.4236
  - nab_score_low_fn_mean: -0.749
  - nab_score_low_fn_std: 1.9585
  - n_ground_truth_sum: 54.0
  - n_detections_sum: 1033.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.2019
  - primary_metric_in_opposite_fold: 0.2557
  - generalization_gap: 0.05379999999999999
  - parameter_values: {'lambda_': 10.0, 'delta': 0.005, 'alpha': 0.99, 'ma_window': 200.0, 'min_gap_samples': 2000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.2019
  - primary_metric_in_opposite_fold: 0.2557
  - generalization_gap: 0.05379999999999999
  - parameter_values: {'lambda_': 10.0, 'delta': 0.005, 'alpha': 0.99, 'ma_window': 200.0, 'min_gap_samples': 2000.0}
- Mean Cross Primary Metric:
  - value: 0.22499999999999998