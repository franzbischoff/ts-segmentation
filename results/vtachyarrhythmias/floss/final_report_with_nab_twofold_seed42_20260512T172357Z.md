# Two-Fold Robustness Snapshot
Generated: 2026-05-12T17:23:57.014369 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: window_size: 75.0, regime_threshold: 0.45, regime_landmark: 3.0, min_gap_samples: 500.0
- Primary metric in fold: 0.5513
- Primary metric in opposite fold: 0.5317
- Generalization gap: 0.019600000000000062
- Cross-fold metrics (opposite fold):
  - window_size: 75.0
  - regime_threshold: 0.45
  - regime_landmark: 3.0
  - min_gap_samples: 500.0
  - f1_classic_mean: 0.3187
  - f1_classic_std: 0.1783
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.295
  - f1_weighted_std: 0.1721
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.5733
  - f3_classic_std: 0.2062
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.5317
  - f3_weighted_std: 0.2104
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.7092
  - recall_4s_std: 0.3411
  - recall_10s_mean: 0.8219
  - recall_10s_std: 0.2885
  - precision_4s_mean: 0.1992
  - precision_4s_std: 0.2224
  - precision_10s_mean: 0.2427
  - precision_10s_std: 0.2296
  - edd_median_s_mean: 3.3661
  - fp_per_min_mean: 0.9501
  - nab_score_standard_mean: 0.0425
  - nab_score_standard_std: 1.2178
  - nab_score_low_fp_mean: -0.7525
  - nab_score_low_fp_std: 1.5764
  - nab_score_low_fn_mean: -0.2659
  - nab_score_low_fn_std: 2.2104
  - n_ground_truth_sum: 43.0
  - n_detections_sum: 171.0

## FOLD_B
- Records: 17
- Unique files: 17
- Best params: window_size: 100.0, regime_threshold: 0.3, regime_landmark: 3.5, min_gap_samples: 1000.0
- Primary metric in fold: 0.5901
- Primary metric in opposite fold: 0.4963
- Generalization gap: 0.09379999999999994
- Cross-fold metrics (opposite fold):
  - window_size: 100.0
  - regime_threshold: 0.3
  - regime_landmark: 3.5
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.3969
  - f1_classic_std: 0.2205
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.3582
  - f1_weighted_std: 0.205
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.5514
  - f3_classic_std: 0.2832
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.4963
  - f3_weighted_std: 0.2809
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.4593
  - recall_4s_std: 0.3785
  - recall_10s_mean: 0.6495
  - recall_10s_std: 0.3445
  - precision_4s_mean: 0.2083
  - precision_4s_std: 0.1662
  - precision_10s_mean: 0.3362
  - precision_10s_std: 0.2501
  - edd_median_s_mean: 3.6136
  - fp_per_min_mean: 0.534
  - nab_score_standard_mean: -0.3146
  - nab_score_standard_std: 1.7446
  - nab_score_low_fp_mean: -0.7611
  - nab_score_low_fp_std: 1.8099
  - nab_score_low_fn_mean: -1.5031
  - nab_score_low_fn_std: 3.3585
  - n_ground_truth_sum: 54.0
  - n_detections_sum: 110.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.5513
  - primary_metric_in_opposite_fold: 0.5317
  - generalization_gap: 0.019600000000000062
  - parameter_values: {'window_size': 75.0, 'regime_threshold': 0.45, 'regime_landmark': 3.0, 'min_gap_samples': 500.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.5513
  - primary_metric_in_opposite_fold: 0.5317
  - generalization_gap: 0.019600000000000062
  - parameter_values: {'window_size': 75.0, 'regime_threshold': 0.45, 'regime_landmark': 3.0, 'min_gap_samples': 500.0}
- Mean Cross Primary Metric:
  - value: 0.514