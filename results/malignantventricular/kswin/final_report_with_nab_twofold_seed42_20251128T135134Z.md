# Two-Fold Robustness Snapshot
Generated: 2025-11-28T13:51:34.624508 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/malignantventricular/fold_assignments_seed42.json
Fold sizes: {'fold_a': 11, 'fold_b': 11}
---
## FOLD_A
- Records: 11
- Unique files: 11
- Best params: alpha: 0.01, window_size: 200.0, stat_size: 20.0, ma_window: 50.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2266
- Primary metric in opposite fold: 0.308
- Generalization gap: 0.0814
- Cross-fold metrics (opposite fold):
  - alpha: 0.01
  - window_size: 200.0
  - stat_size: 20.0
  - ma_window: 50.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.1829
  - f1_classic_std: 0.1106
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.128
  - f1_weighted_std: 0.0615
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.4159
  - f3_classic_std: 0.1264
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.308
  - f3_weighted_std: 0.0992
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.5071
  - recall_4s_std: 0.1336
  - recall_10s_mean: 0.8273
  - recall_10s_std: 0.1979
  - precision_4s_mean: 0.0716
  - precision_4s_std: 0.0606
  - precision_10s_mean: 0.1165
  - precision_10s_std: 0.0912
  - edd_median_s_mean: 4.2464
  - fp_per_min_mean: 6.0987
  - nab_score_standard_mean: -25.0724
  - nab_score_standard_std: 20.427
  - nab_score_low_fp_mean: -45.1402
  - nab_score_low_fp_std: 19.5874
  - nab_score_low_fn_mean: -35.7658
  - nab_score_low_fn_std: 48.0789
  - n_ground_truth_sum: 471.0
  - n_detections_sum: 2693.0

## FOLD_B
- Records: 11
- Unique files: 11
- Best params: alpha: 0.05, window_size: 500.0, stat_size: 30.0, ma_window: 100.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.332
- Primary metric in opposite fold: 0.2046
- Generalization gap: 0.1274
- Cross-fold metrics (opposite fold):
  - alpha: 0.05
  - window_size: 500.0
  - stat_size: 30.0
  - ma_window: 100.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.0575
  - f1_classic_std: 0.0451
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.0543
  - f1_weighted_std: 0.0421
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.2161
  - f3_classic_std: 0.131
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.2046
  - f3_weighted_std: 0.1225
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.8285
  - recall_4s_std: 0.128
  - recall_10s_mean: 0.9924
  - recall_10s_std: 0.0251
  - precision_4s_mean: 0.023
  - precision_4s_std: 0.0177
  - precision_10s_mean: 0.0301
  - precision_10s_std: 0.0248
  - edd_median_s_mean: 2.7204
  - fp_per_min_mean: 10.1299
  - nab_score_standard_mean: -27.8136
  - nab_score_standard_std: 6.6764
  - nab_score_low_fp_mean: -60.9247
  - nab_score_low_fp_std: 8.042
  - nab_score_low_fn_mean: -13.349
  - nab_score_low_fn_std: 5.2331
  - n_ground_truth_sum: 121.0
  - n_detections_sum: 4092.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.2266
  - primary_metric_in_opposite_fold: 0.308
  - generalization_gap: 0.0814
  - parameter_values: {'alpha': 0.01, 'window_size': 200.0, 'stat_size': 20.0, 'ma_window': 50.0, 'min_gap_samples': 2000.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.2266
  - primary_metric_in_opposite_fold: 0.308
  - generalization_gap: 0.0814
  - parameter_values: {'alpha': 0.01, 'window_size': 200.0, 'stat_size': 20.0, 'ma_window': 50.0, 'min_gap_samples': 2000.0}
- Mean Cross Primary Metric:
  - value: 0.2563