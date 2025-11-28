# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:51:00.843369 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/afib_paroxysmal/fold_assignments_seed42.json
Fold sizes: {'fold_a': 114, 'fold_b': 115}
---
## FOLD_A
- Records: 114
- Unique files: 114
- Best params: alpha: 0.005, window_size: 500.0, stat_size: 50.0, ma_window: 50.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.4396
- Primary metric in opposite fold: 0.3877
- Generalization gap: 0.0519
- Cross-fold metrics (opposite fold):
  - alpha: 0.005
  - window_size: 500.0
  - stat_size: 50.0
  - ma_window: 50.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1597
  - f1_classic_std: 0.1522
  - f1_classic_count: 115.0
  - f1_weighted_mean: 0.1516
  - f1_weighted_std: 0.1435
  - f1_weighted_count: 115.0
  - f3_classic_mean: 0.4073
  - f3_classic_std: 0.2224
  - f3_classic_count: 115.0
  - f3_weighted_mean: 0.3877
  - f3_weighted_std: 0.2116
  - f3_weighted_count: 115.0
  - recall_4s_mean: 0.7249
  - recall_4s_std: 0.2692
  - recall_10s_mean: 0.9924
  - recall_10s_std: 0.0392
  - precision_4s_mean: 0.0642
  - precision_4s_std: 0.0704
  - precision_10s_mean: 0.0958
  - precision_10s_std: 0.1082
  - edd_median_s_mean: 3.0237
  - fp_per_min_mean: 9.5741
  - nab_score_standard_mean: -10.6371
  - nab_score_standard_std: 38.116
  - nab_score_low_fp_mean: -23.8765
  - nab_score_low_fp_std: 76.2037
  - nab_score_low_fn_mean: -5.0
  - nab_score_low_fn_std: 19.2159
  - n_ground_truth_sum: 589.0
  - n_detections_sum: 16786.0

## FOLD_B
- Records: 115
- Unique files: 115
- Best params: alpha: 0.05, window_size: 500.0, stat_size: 20.0, ma_window: 100.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.3929
- Primary metric in opposite fold: 0.4305
- Generalization gap: 0.03759999999999997
- Cross-fold metrics (opposite fold):
  - alpha: 0.05
  - window_size: 500.0
  - stat_size: 20.0
  - ma_window: 100.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1988
  - f1_classic_std: 0.172
  - f1_classic_count: 114.0
  - f1_weighted_mean: 0.1803
  - f1_weighted_std: 0.1529
  - f1_weighted_count: 114.0
  - f3_classic_mean: 0.4705
  - f3_classic_std: 0.2248
  - f3_classic_count: 114.0
  - f3_weighted_mean: 0.4305
  - f3_weighted_std: 0.2024
  - f3_weighted_count: 114.0
  - recall_4s_mean: 0.6167
  - recall_4s_std: 0.3083
  - recall_10s_mean: 0.9933
  - recall_10s_std: 0.031
  - precision_4s_mean: 0.0689
  - precision_4s_std: 0.0735
  - precision_10s_mean: 0.1228
  - precision_10s_std: 0.1287
  - edd_median_s_mean: 3.2471
  - fp_per_min_mean: 8.8039
  - nab_score_standard_mean: -7.7039
  - nab_score_standard_std: 31.4654
  - nab_score_low_fp_mean: -17.8534
  - nab_score_low_fp_std: 62.4722
  - nab_score_low_fn_mean: -4.1731
  - nab_score_low_fn_std: 16.3153
  - n_ground_truth_sum: 712.0
  - n_detections_sum: 12980.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.3929
  - primary_metric_in_opposite_fold: 0.4305
  - generalization_gap: 0.03759999999999997
  - parameter_values: {'alpha': 0.05, 'window_size': 500.0, 'stat_size': 20.0, 'ma_window': 100.0, 'min_gap_samples': 1000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.3929
  - primary_metric_in_opposite_fold: 0.4305
  - generalization_gap: 0.03759999999999997
  - parameter_values: {'alpha': 0.05, 'window_size': 500.0, 'stat_size': 20.0, 'ma_window': 100.0, 'min_gap_samples': 1000.0}
- Mean Cross Primary Metric:
  - value: 0.4091