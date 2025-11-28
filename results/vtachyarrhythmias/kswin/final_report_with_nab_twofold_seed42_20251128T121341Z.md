# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:13:41.449269 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: alpha: 0.005, window_size: 200.0, stat_size: 100.0, ma_window: 50.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2795
- Primary metric in opposite fold: 0.1921
- Generalization gap: 0.08740000000000003
- Cross-fold metrics (opposite fold):
  - alpha: 0.005
  - window_size: 200.0
  - stat_size: 100.0
  - ma_window: 50.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.0681
  - f1_classic_std: 0.0522
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.054
  - f1_weighted_std: 0.042
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.2417
  - f3_classic_std: 0.1244
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.1921
  - f3_weighted_std: 0.1098
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.3595
  - recall_4s_std: 0.3487
  - recall_10s_mean: 0.9739
  - recall_10s_std: 0.1078
  - precision_4s_mean: 0.0166
  - precision_4s_std: 0.0203
  - precision_10s_mean: 0.0362
  - precision_10s_std: 0.0299
  - edd_median_s_mean: 4.7186
  - fp_per_min_mean: 7.2263
  - nab_score_standard_mean: -4.0671
  - nab_score_standard_std: 1.8749
  - nab_score_low_fp_mean: -9.7074
  - nab_score_low_fp_std: 2.0736
  - nab_score_low_fn_mean: -1.541
  - nab_score_low_fn_std: 2.5679
  - n_ground_truth_sum: 43.0
  - n_detections_sum: 1085.0

## FOLD_B
- Records: 17
- Unique files: 17
- Best params: alpha: 0.001, window_size: 500.0, stat_size: 30.0, ma_window: 1.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2278
- Primary metric in opposite fold: 0.2142
- Generalization gap: 0.013600000000000001
- Cross-fold metrics (opposite fold):
  - alpha: 0.001
  - window_size: 500.0
  - stat_size: 30.0
  - ma_window: 1.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.1064
  - f1_classic_std: 0.0774
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.0685
  - f1_weighted_std: 0.0589
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.337
  - f3_classic_std: 0.1644
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.2142
  - f3_weighted_std: 0.1461
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.2882
  - recall_4s_std: 0.3421
  - recall_10s_mean: 0.9941
  - recall_10s_std: 0.0243
  - precision_4s_mean: 0.0174
  - precision_4s_std: 0.024
  - precision_10s_mean: 0.0581
  - precision_10s_std: 0.0458
  - edd_median_s_mean: 5.9401
  - fp_per_min_mean: 5.971
  - nab_score_standard_mean: -2.978
  - nab_score_standard_std: 1.5971
  - nab_score_low_fp_mean: -7.6943
  - nab_score_low_fp_std: 1.8258
  - nab_score_low_fn_mean: -0.914
  - nab_score_low_fn_std: 1.5678
  - n_ground_truth_sum: 54.0
  - n_detections_sum: 918.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.2278
  - primary_metric_in_opposite_fold: 0.2142
  - generalization_gap: 0.013600000000000001
  - parameter_values: {'alpha': 0.001, 'window_size': 500.0, 'stat_size': 30.0, 'ma_window': 1.0, 'min_gap_samples': 2000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.2278
  - primary_metric_in_opposite_fold: 0.2142
  - generalization_gap: 0.013600000000000001
  - parameter_values: {'alpha': 0.001, 'window_size': 500.0, 'stat_size': 30.0, 'ma_window': 1.0, 'min_gap_samples': 2000.0}
- Mean Cross Primary Metric:
  - value: 0.20315