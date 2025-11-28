# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:31:21.893401 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/afib_paroxysmal/fold_assignments_seed42.json
Fold sizes: {'fold_a': 114, 'fold_b': 115}
---
## FOLD_A
- Records: 114
- Unique files: 114
- Best params: delta: 0.005, ma_window: 75.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.428
- Primary metric in opposite fold: 0.3688
- Generalization gap: 0.059199999999999975
- Cross-fold metrics (opposite fold):
  - delta: 0.005
  - ma_window: 75.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1562
  - f1_classic_std: 0.1486
  - f1_classic_count: 115.0
  - f1_weighted_mean: 0.1449
  - f1_weighted_std: 0.1378
  - f1_weighted_count: 115.0
  - f3_classic_mean: 0.3941
  - f3_classic_std: 0.2191
  - f3_classic_count: 115.0
  - f3_weighted_mean: 0.3688
  - f3_weighted_std: 0.2072
  - f3_weighted_count: 115.0
  - recall_4s_mean: 0.7507
  - recall_4s_std: 0.2823
  - recall_10s_mean: 0.9465
  - recall_10s_std: 0.1485
  - precision_4s_mean: 0.0651
  - precision_4s_std: 0.0674
  - precision_10s_mean: 0.0939
  - precision_10s_std: 0.1056
  - edd_median_s_mean: 2.7702
  - fp_per_min_mean: 9.2875
  - nab_score_standard_mean: -7.1775
  - nab_score_standard_std: 16.9131
  - nab_score_low_fp_mean: -16.369
  - nab_score_low_fp_std: 33.4634
  - nab_score_low_fn_mean: -3.8426
  - nab_score_low_fn_std: 9.4387
  - n_ground_truth_sum: 589.0
  - n_detections_sum: 12582.0

## FOLD_B
- Records: 115
- Unique files: 115
- Best params: delta: 0.015, ma_window: 250.0, min_gap_samples: 1000.0
- Primary metric in fold: 0.3768
- Primary metric in opposite fold: 0.4221
- Generalization gap: 0.04529999999999995
- Cross-fold metrics (opposite fold):
  - delta: 0.015
  - ma_window: 250.0
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.181
  - f1_classic_std: 0.1609
  - f1_classic_count: 114.0
  - f1_weighted_mean: 0.1725
  - f1_weighted_std: 0.1532
  - f1_weighted_count: 114.0
  - f3_classic_mean: 0.4409
  - f3_classic_std: 0.2264
  - f3_classic_count: 114.0
  - f3_weighted_mean: 0.4221
  - f3_weighted_std: 0.2145
  - f3_weighted_count: 114.0
  - recall_4s_mean: 0.8015
  - recall_4s_std: 0.2505
  - recall_10s_mean: 0.9839
  - recall_10s_std: 0.0879
  - precision_4s_mean: 0.0779
  - precision_4s_std: 0.0731
  - precision_10s_mean: 0.1102
  - precision_10s_std: 0.1166
  - edd_median_s_mean: 2.5589
  - fp_per_min_mean: 10.1416
  - nab_score_standard_mean: -8.3346
  - nab_score_standard_std: 28.6049
  - nab_score_low_fp_mean: -19.1572
  - nab_score_low_fp_std: 56.7336
  - nab_score_low_fn_mean: -4.432
  - nab_score_low_fn_std: 15.013
  - n_ground_truth_sum: 712.0
  - n_detections_sum: 14200.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.3768
  - primary_metric_in_opposite_fold: 0.4221
  - generalization_gap: 0.04529999999999995
  - parameter_values: {'delta': 0.015, 'ma_window': 250.0, 'min_gap_samples': 1000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.3768
  - primary_metric_in_opposite_fold: 0.4221
  - generalization_gap: 0.04529999999999995
  - parameter_values: {'delta': 0.015, 'ma_window': 250.0, 'min_gap_samples': 1000.0}
- Mean Cross Primary Metric:
  - value: 0.39544999999999997