# Two-Fold Robustness Snapshot
Generated: 2026-05-12T17:14:02.849415 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/malignantventricular/fold_assignments_seed42.json
Fold sizes: {'fold_a': 11, 'fold_b': 11}
---
## FOLD_A
- Records: 11
- Unique files: 11
- Best params: lambda_: 80.0, delta: 0.02, alpha: 0.99, ma_window: 200.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2189
- Primary metric in opposite fold: 0.2775
- Generalization gap: 0.05860000000000001
- Cross-fold metrics (opposite fold):
  - lambda_: 80.0
  - delta: 0.02
  - alpha: 0.99
  - ma_window: 200.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.1972
  - f1_classic_std: 0.1219
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.1382
  - f1_weighted_std: 0.0804
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.3952
  - f3_classic_std: 0.1769
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.2775
  - f3_weighted_std: 0.1347
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.3289
  - recall_4s_std: 0.1686
  - recall_10s_mean: 0.6641
  - recall_10s_std: 0.2935
  - precision_4s_mean: 0.0684
  - precision_4s_std: 0.0612
  - precision_10s_mean: 0.129
  - precision_10s_std: 0.0958
  - edd_median_s_mean: 4.9688
  - fp_per_min_mean: 4.626
  - nab_score_standard_mean: -24.1056
  - nab_score_standard_std: 22.5674
  - nab_score_low_fp_mean: -39.3482
  - nab_score_low_fp_std: 25.3943
  - nab_score_low_fn_mean: -39.1207
  - nab_score_low_fn_std: 47.9337
  - n_ground_truth_sum: 471.0
  - n_detections_sum: 2078.0

## FOLD_B
- Records: 11
- Unique files: 11
- Best params: lambda_: 10.0, delta: 0.02, alpha: 0.99, ma_window: 50.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.3291
- Primary metric in opposite fold: 0.178
- Generalization gap: 0.1511
- Cross-fold metrics (opposite fold):
  - lambda_: 10.0
  - delta: 0.02
  - alpha: 0.99
  - ma_window: 50.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.0479
  - f1_classic_std: 0.0377
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.0456
  - f1_weighted_std: 0.033
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.186
  - f3_classic_std: 0.1149
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.178
  - f3_weighted_std: 0.1014
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.7992
  - recall_4s_std: 0.1357
  - recall_10s_mean: 0.9778
  - recall_10s_std: 0.0643
  - precision_4s_mean: 0.0197
  - precision_4s_std: 0.0154
  - precision_10s_mean: 0.0249
  - precision_10s_std: 0.0205
  - edd_median_s_mean: 2.494
  - fp_per_min_mean: 12.1974
  - nab_score_standard_mean: -34.436
  - nab_score_standard_std: 8.378
  - nab_score_low_fp_mean: -74.3566
  - nab_score_low_fp_std: 13.6307
  - nab_score_low_fn_mean: -16.6575
  - nab_score_low_fn_std: 5.2465
  - n_ground_truth_sum: 121.0
  - n_detections_sum: 4920.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.2189
  - primary_metric_in_opposite_fold: 0.2775
  - generalization_gap: 0.05860000000000001
  - parameter_values: {'lambda_': 80.0, 'delta': 0.02, 'alpha': 0.99, 'ma_window': 200.0, 'min_gap_samples': 2000.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.2189
  - primary_metric_in_opposite_fold: 0.2775
  - generalization_gap: 0.05860000000000001
  - parameter_values: {'lambda_': 80.0, 'delta': 0.02, 'alpha': 0.99, 'ma_window': 200.0, 'min_gap_samples': 2000.0}
- Mean Cross Primary Metric:
  - value: 0.22775