# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:22:00.762852 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: window_size: 75.0, regime_threshold: 0.45, regime_landmark: 3.0, min_gap_samples: 500.0
- Primary metric in fold: 0.5483
- Primary metric in opposite fold: 0.5299
- Generalization gap: 0.018399999999999972
- Cross-fold metrics (opposite fold):
  - window_size: 75.0
  - regime_threshold: 0.45
  - regime_landmark: 3.0
  - min_gap_samples: 500.0
  - f1_classic_mean: 0.3187
  - f1_classic_std: 0.1783
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.291
  - f1_weighted_std: 0.171
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.5733
  - f3_classic_std: 0.2062
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.5299
  - f3_weighted_std: 0.2108
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
- Best params: window_size: 125.0, regime_threshold: 0.3, regime_landmark: 3.5, min_gap_samples: 3000.0
- Primary metric in fold: 0.5885
- Primary metric in opposite fold: 0.4864
- Generalization gap: 0.10210000000000002
- Cross-fold metrics (opposite fold):
  - window_size: 125.0
  - regime_threshold: 0.3
  - regime_landmark: 3.5
  - min_gap_samples: 3000.0
  - f1_classic_mean: 0.3814
  - f1_classic_std: 0.223
  - f1_classic_count: 17.0
  - f1_weighted_mean: 0.3227
  - f1_weighted_std: 0.1881
  - f1_weighted_count: 17.0
  - f3_classic_mean: 0.5596
  - f3_classic_std: 0.3075
  - f3_classic_count: 17.0
  - f3_weighted_mean: 0.4864
  - f3_weighted_std: 0.2885
  - f3_weighted_count: 17.0
  - recall_4s_mean: 0.4387
  - recall_4s_std: 0.3852
  - recall_10s_mean: 0.6701
  - recall_10s_std: 0.3787
  - precision_4s_mean: 0.1646
  - precision_4s_std: 0.1251
  - precision_10s_mean: 0.3145
  - precision_10s_std: 0.2493
  - edd_median_s_mean: 3.628
  - fp_per_min_mean: 0.5548
  - nab_score_standard_mean: -0.2545
  - nab_score_standard_std: 1.9104
  - nab_score_low_fp_mean: -0.701
  - nab_score_low_fp_std: 1.9634
  - nab_score_low_fn_mean: -1.3842
  - nab_score_low_fn_std: 3.6162
  - n_ground_truth_sum: 54.0
  - n_detections_sum: 113.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_a
  - primary_metric_in_fold: 0.5483
  - primary_metric_in_opposite_fold: 0.5299
  - generalization_gap: 0.018399999999999972
  - parameter_values: {'window_size': 75.0, 'regime_threshold': 0.45, 'regime_landmark': 3.0, 'min_gap_samples': 500.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.5483
  - primary_metric_in_opposite_fold: 0.5299
  - generalization_gap: 0.018399999999999972
  - parameter_values: {'window_size': 75.0, 'regime_threshold': 0.45, 'regime_landmark': 3.0, 'min_gap_samples': 500.0}
- Mean Cross Primary Metric:
  - value: 0.50815