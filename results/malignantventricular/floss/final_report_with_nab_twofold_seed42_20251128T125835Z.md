# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:58:35.942060 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/malignantventricular/fold_assignments_seed42.json
Fold sizes: {'fold_a': 11, 'fold_b': 11}
---
## FOLD_A
- Records: 11
- Unique files: 11
- Best params: window_size: 75.0, regime_threshold: 0.6, regime_landmark: 4.5, min_gap_samples: 500.0
- Primary metric in fold: 0.3064
- Primary metric in opposite fold: 0.2717
- Generalization gap: 0.03470000000000001
- Cross-fold metrics (opposite fold):
  - window_size: 75.0
  - regime_threshold: 0.6
  - regime_landmark: 4.5
  - min_gap_samples: 500.0
  - f1_classic_mean: 0.2345
  - f1_classic_std: 0.1045
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.2023
  - f1_weighted_std: 0.0936
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.3064
  - f3_classic_std: 0.141
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.2717
  - f3_weighted_std: 0.1363
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.2298
  - recall_4s_std: 0.1582
  - recall_10s_mean: 0.3656
  - recall_10s_std: 0.1666
  - precision_4s_mean: 0.1431
  - precision_4s_std: 0.1045
  - precision_10s_mean: 0.2516
  - precision_10s_std: 0.2097
  - edd_median_s_mean: 3.9058
  - fp_per_min_mean: 1.1013
  - nab_score_standard_mean: -28.2273
  - nab_score_standard_std: 35.5587
  - nab_score_low_fp_mean: -31.831
  - nab_score_low_fp_std: 35.1839
  - nab_score_low_fn_mean: -59.1528
  - nab_score_low_fn_std: 74.7871
  - n_ground_truth_sum: 471.0
  - n_detections_sum: 569.0

## FOLD_B
- Records: 11
- Unique files: 11
- Best params: window_size: 125.0, regime_threshold: 0.75, regime_landmark: 5.5, min_gap_samples: 1000.0
- Primary metric in fold: 0.3234
- Primary metric in opposite fold: 0.2788
- Generalization gap: 0.04460000000000003
- Cross-fold metrics (opposite fold):
  - window_size: 125.0
  - regime_threshold: 0.75
  - regime_landmark: 5.5
  - min_gap_samples: 1000.0
  - f1_classic_mean: 0.1352
  - f1_classic_std: 0.0874
  - f1_classic_count: 11.0
  - f1_weighted_mean: 0.1081
  - f1_weighted_std: 0.0685
  - f1_weighted_count: 11.0
  - f3_classic_mean: 0.3441
  - f3_classic_std: 0.1692
  - f3_classic_count: 11.0
  - f3_weighted_mean: 0.2788
  - f3_weighted_std: 0.1297
  - f3_weighted_count: 11.0
  - recall_4s_mean: 0.4493
  - recall_4s_std: 0.1049
  - recall_10s_mean: 0.674
  - recall_10s_std: 0.113
  - precision_4s_mean: 0.0456
  - precision_4s_std: 0.0305
  - precision_10s_mean: 0.078
  - precision_10s_std: 0.0543
  - edd_median_s_mean: 3.6113
  - fp_per_min_mean: 2.6675
  - nab_score_standard_mean: -6.7585
  - nab_score_standard_std: 3.7391
  - nab_score_low_fp_mean: -15.6158
  - nab_score_low_fp_std: 5.4839
  - nab_score_low_fn_mean: -6.148
  - nab_score_low_fn_std: 3.0481
  - n_ground_truth_sum: 121.0
  - n_detections_sum: 1117.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.3234
  - primary_metric_in_opposite_fold: 0.2788
  - generalization_gap: 0.04460000000000003
  - parameter_values: {'window_size': 125.0, 'regime_threshold': 0.75, 'regime_landmark': 5.5, 'min_gap_samples': 1000.0}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.3064
  - primary_metric_in_opposite_fold: 0.2717
  - generalization_gap: 0.03470000000000001
  - parameter_values: {'window_size': 75.0, 'regime_threshold': 0.6, 'regime_landmark': 4.5, 'min_gap_samples': 500.0}
- Mean Cross Primary Metric:
  - value: 0.27525