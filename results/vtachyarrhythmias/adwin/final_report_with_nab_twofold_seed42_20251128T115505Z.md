# Two-Fold Robustness Snapshot
Generated: 2025-11-28T11:55:05.117344 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: delta: 0.025, ma_window: 250.0, min_gap_samples: 2000.0
- Primary metric in fold: 0.2753
- Primary metric in opposite fold: 0.198
- Generalization gap: 0.07729999999999998
- Cross-fold metrics (opposite fold):
  - delta: 0.025
  - ma_window: 250.0
  - min_gap_samples: 2000.0
  - f1_classic_mean: 0.0677
  - f1_classic_std: 0.0557
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.0559
  - f1_weighted_std: 0.045
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.2362
  - f3_classic_std: 0.1326
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.198
  - f3_weighted_std: 0.1151
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.6626
  - recall_4s_std: 0.3521
  - recall_10s_mean: 0.915
  - recall_10s_std: 0.1895
  - precision_4s_mean: 0.023
  - precision_4s_std: 0.0189
  - precision_10s_mean: 0.0362
  - precision_10s_std: 0.032
  - edd_median_s_mean: 3.4109
  - fp_per_min_mean: 6.8379
  - nab_score_standard_mean: -3.8015
  - nab_score_standard_std: 1.952
  - nab_score_low_fp_mean: -9.0806
  - nab_score_low_fp_std: 2.1583
  - nab_score_low_fn_mean: -1.5149
  - nab_score_low_fn_std: 2.4518
  - n_ground_truth_sum: 43.0
  - n_detections_sum: 1033.0

## FOLD_B
- Records: 17
- Unique files: 17
- Best params: delta: 0.06, ma_window: 25.0, min_gap_samples: 5000.0
- Primary metric in fold: 0.2606
- Primary metric in opposite fold: 0.1872
- Generalization gap: 0.07339999999999999
- Cross-fold metrics (opposite fold):
  - delta: 0.06
  - ma_window: 25.0
  - min_gap_samples: 5000.0
  - f1_classic_mean: 0.1012
  - f1_classic_std: 0.0876
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.0808
  - f1_weighted_std: 0.0718
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.2282
  - f3_classic_std: 0.1739
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.1872
  - f3_weighted_std: 0.159
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.2436
  - recall_4s_std: 0.3148
  - recall_10s_mean: 0.3833
  - recall_10s_std: 0.3268
  - precision_4s_mean: 0.0327
  - precision_4s_std: 0.0426
  - precision_10s_mean: 0.0618
  - precision_10s_std: 0.0582
  - edd_median_s_mean: 3.4357
  - fp_per_min_mean: 2.2192
  - nab_score_standard_mean: -2.6655
  - nab_score_standard_std: 1.4571
  - nab_score_low_fp_mean: -4.3155
  - nab_score_low_fp_std: 1.5101
  - nab_score_low_fn_mean: -3.8405
  - nab_score_low_fn_std: 3.1165
  - n_ground_truth_sum: 54.0
  - n_detections_sum: 343.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.2753
  - primary_metric_in_opposite_fold: 0.198
  - generalization_gap: 0.07729999999999998
  - parameter_values: {'delta': 0.025, 'ma_window': 250.0, 'min_gap_samples': 2000.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.2606
  - primary_metric_in_opposite_fold: 0.1872
  - generalization_gap: 0.07339999999999999
  - parameter_values: {'delta': 0.06, 'ma_window': 25.0, 'min_gap_samples': 5000.0}
- Mean Cross Primary Metric:
  - value: 0.1926