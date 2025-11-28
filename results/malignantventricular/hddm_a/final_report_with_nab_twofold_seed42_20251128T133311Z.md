# Two-Fold Robustness Snapshot
Generated: 2025-11-28T13:33:11.840283 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/malignantventricular/fold_assignments_seed42.json
Fold sizes: {'fold_a': 11, 'fold_b': 11}
---
## FOLD_A
- Records: 11
- Unique files: 11
- Best params: drift_confidence: 0.0001, warning_confidence: 0.001, two_side_option: False, ma_window: 100, min_gap_samples: 2000
- Primary metric in fold: 0.2129
- Primary metric in opposite fold: 0.3019
- Generalization gap: 0.089
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.0001
  - warning_confidence: 0.001
  - two_side_option: False
  - ma_window: 100
  - min_gap_samples: 2000
  - f1_classic_mean: 0.1879
  - f1_classic_std: 0.1083
  - f1_classic_count: 11
  - f1_weighted_mean: 0.1344
  - f1_weighted_std: 0.0683
  - f1_weighted_count: 11
  - f3_classic_mean: 0.4076
  - f3_classic_std: 0.1468
  - f3_classic_count: 11
  - f3_weighted_mean: 0.3019
  - f3_weighted_std: 0.1271
  - f3_weighted_count: 11
  - recall_4s_mean: 0.3832
  - recall_4s_std: 0.1248
  - recall_10s_mean: 0.7273
  - recall_10s_std: 0.2313
  - precision_4s_mean: 0.0729
  - precision_4s_std: 0.0665
  - precision_10s_mean: 0.1197
  - precision_10s_std: 0.0869
  - edd_median_s_mean: 5.0485
  - fp_per_min_mean: 5.2286
  - nab_score_standard_mean: -24.2628
  - nab_score_standard_std: 21.2323
  - nab_score_low_fp_mean: -41.462
  - nab_score_low_fp_std: 22.7562
  - nab_score_low_fn_mean: -37.845
  - nab_score_low_fn_std: 47.3783
  - n_ground_truth_sum: 471
  - n_detections_sum: 2329

## FOLD_B
- Records: 11
- Unique files: 11
- Best params: drift_confidence: 0.001, warning_confidence: 0.001, two_side_option: False, ma_window: 50, min_gap_samples: 1000
- Primary metric in fold: 0.3299
- Primary metric in opposite fold: 0.1802
- Generalization gap: 0.14970000000000003
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.001
  - warning_confidence: 0.001
  - two_side_option: False
  - ma_window: 50
  - min_gap_samples: 1000
  - f1_classic_mean: 0.0478
  - f1_classic_std: 0.0377
  - f1_classic_count: 11
  - f1_weighted_mean: 0.0462
  - f1_weighted_std: 0.0344
  - f1_weighted_count: 11
  - f3_classic_mean: 0.1858
  - f3_classic_std: 0.115
  - f3_classic_count: 11
  - f3_weighted_mean: 0.1802
  - f3_weighted_std: 0.1054
  - f3_weighted_count: 11
  - recall_4s_mean: 0.7897
  - recall_4s_std: 0.1674
  - recall_10s_mean: 0.9778
  - recall_10s_std: 0.0643
  - precision_4s_mean: 0.0207
  - precision_4s_std: 0.0173
  - precision_10s_mean: 0.0249
  - precision_10s_std: 0.0205
  - edd_median_s_mean: 2.2205
  - fp_per_min_mean: 12.2
  - nab_score_standard_mean: -34.3275
  - nab_score_standard_std: 8.373
  - nab_score_low_fp_mean: -74.2391
  - nab_score_low_fp_std: 13.5071
  - nab_score_low_fn_mean: -16.5535
  - nab_score_low_fn_std: 5.2923
  - n_ground_truth_sum: 121
  - n_detections_sum: 4924

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.2129
  - primary_metric_in_opposite_fold: 0.3019
  - generalization_gap: 0.089
  - parameter_values: {'drift_confidence': 0.0001, 'warning_confidence': 0.001, 'two_side_option': False, 'ma_window': 100, 'min_gap_samples': 2000}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.2129
  - primary_metric_in_opposite_fold: 0.3019
  - generalization_gap: 0.089
  - parameter_values: {'drift_confidence': 0.0001, 'warning_confidence': 0.001, 'two_side_option': False, 'ma_window': 100, 'min_gap_samples': 2000}
- Mean Cross Primary Metric:
  - value: 0.24105