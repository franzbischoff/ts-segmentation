# Two-Fold Robustness Snapshot
Generated: 2025-11-28T13:01:37.692848 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/malignantventricular/fold_assignments_seed42.json
Fold sizes: {'fold_a': 11, 'fold_b': 11}
---
## FOLD_A
- Records: 11
- Unique files: 11
- Best params: delta: 0.04, ma_window: 10.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.2389
- Primary metric in opposite fold: 0.2435
- Generalization gap: 0.004599999999999993
- Cross-fold metrics (opposite fold):
  - delta: 0.04
  - ma_window: 10.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1511
  - f1_classic_std: 0.0999
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.1173
  - f1_weighted_std: 0.0676
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.3031
  - f3_classic_std: 0.1375
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.2435
  - f3_weighted_std: 0.1086
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.4123
  - recall_4s_std: 0.2297
  - recall_10s_mean: 0.5953
  - recall_10s_std: 0.2957
  - precision_4s_mean: 0.071
  - precision_4s_std: 0.0588
  - precision_10s_mean: 0.1052
  - precision_10s_std: 0.0866
  - edd_median_s_mean: 4.0467
  - fp_per_min_mean: 5.8442
  - nab_score_standard_mean: -36.0
  - nab_score_standard_std: 29.8562
  - nab_score_low_fp_mean: -52.9239
  - nab_score_low_fp_std: 30.3762
  - nab_score_low_fn_mean: -56.9018
  - nab_score_low_fn_std: 68.7075
  - n_ground_truth_sum: 471.0
  - n_detections_sum: 2557.0

## FOLD_B
- Records: 11
- Unique files: 11
- Best params: delta: 0.025, ma_window: 100.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.3304
- Primary metric in opposite fold: 0.1816
- Generalization gap: 0.14880000000000002
- Cross-fold metrics (opposite fold):
  - delta: 0.025
  - ma_window: 100.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.0528
  - f1_classic_std: 0.038
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.0473
  - f1_weighted_std: 0.0373
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.2039
  - f3_classic_std: 0.1169
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.1816
  - f3_weighted_std: 0.1149
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.6915
  - recall_4s_std: 0.2501
  - recall_10s_mean: 0.9833
  - recall_10s_std: 0.0373
  - precision_4s_mean: 0.0194
  - precision_4s_std: 0.0177
  - precision_10s_mean: 0.0275
  - precision_10s_std: 0.0206
  - edd_median_s_mean: 3.1215
  - fp_per_min_mean: 10.9039
  - nab_score_standard_mean: -29.0761
  - nab_score_standard_std: 10.3184
  - nab_score_low_fp_mean: -63.2224
  - nab_score_low_fp_std: 19.309
  - nab_score_low_fn_mean: -14.0938
  - nab_score_low_fn_std: 6.1581
  - n_ground_truth_sum: 121.0
  - n_detections_sum: 4420.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.2389
  - primary_metric_in_opposite_fold: 0.2435
  - generalization_gap: 0.004599999999999993
  - parameter_values: {'delta': 0.04, 'ma_window': 10.0, 'min_gap_samples': 1000.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.2389
  - primary_metric_in_opposite_fold: 0.2435
  - generalization_gap: 0.004599999999999993
  - parameter_values: {'delta': 0.04, 'ma_window': 10.0, 'min_gap_samples': 1000.0}
- Mean Cross Primary Metric:
  - value: 0.21255000000000002