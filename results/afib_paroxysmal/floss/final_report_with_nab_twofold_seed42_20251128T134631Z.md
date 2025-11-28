# Two-Fold Robustness Snapshot
Generated: 2025-11-28T13:46:31.268899 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/afib_paroxysmal/fold_assignments_seed42.json
Fold sizes: {'fold_a': 114, 'fold_b': 115}
---
## FOLD_A
- Records: 114
- Unique files: 114
- Best params: window_size: 125.0, regime_threshold: 0.65, regime_landmark: 5.5, min_gap_samples: 200.0
- Primary metric in fold: 0.4941
- Primary metric in opposite fold: 0.4556
- Generalization gap: 0.03849999999999998
- Cross-fold metrics (opposite fold):
  - window_size: 125.0
  - regime_threshold: 0.65
  - regime_landmark: 5.5
  - min_gap_samples: 200.0
  - f1_classic_mean: 0.3445
  - f1_classic_std: 0.2275
  - f1_classic_count: 115.0
  - f1_weighted_mean: 0.3006
  - f1_weighted_std: 0.2125
  - f1_weighted_count: 115.0
  - f3_classic_mean: 0.5202
  - f3_classic_std: 0.2374
  - f3_classic_count: 115.0
  - f3_weighted_mean: 0.4556
  - f3_weighted_std: 0.2299
  - f3_weighted_count: 115.0
  - recall_4s_mean: 0.3892
  - recall_4s_std: 0.2861
  - recall_10s_mean: 0.7014
  - recall_10s_std: 0.2518
  - precision_4s_mean: 0.1282
  - precision_4s_std: 0.1557
  - precision_10s_mean: 0.2795
  - precision_10s_std: 0.2415
  - edd_median_s_mean: 3.8453
  - fp_per_min_mean: 1.9352
  - nab_score_standard_mean: -2.1324
  - nab_score_standard_std: 5.2559
  - nab_score_low_fp_mean: -4.4524
  - nab_score_low_fp_std: 9.6657
  - nab_score_low_fn_mean: -3.2332
  - nab_score_low_fn_std: 5.972
  - n_ground_truth_sum: 589.0
  - n_detections_sum: 3359.0

## FOLD_B
- Records: 115
- Unique files: 115
- Best params: window_size: 100.0, regime_threshold: 0.7, regime_landmark: 4.0, min_gap_samples: 500.0
- Primary metric in fold: 0.477
- Primary metric in opposite fold: 0.4768
- Generalization gap: 0.00019999999999997797
- Cross-fold metrics (opposite fold):
  - window_size: 100.0
  - regime_threshold: 0.7
  - regime_landmark: 4.0
  - min_gap_samples: 500.0
  - f1_classic_mean: 0.3539
  - f1_classic_std: 0.2091
  - f1_classic_count: 114.0
  - f1_weighted_mean: 0.3227
  - f1_weighted_std: 0.1922
  - f1_weighted_count: 114.0
  - f3_classic_mean: 0.5215
  - f3_classic_std: 0.2458
  - f3_classic_count: 114.0
  - f3_weighted_mean: 0.4768
  - f3_weighted_std: 0.2325
  - f3_weighted_count: 114.0
  - recall_4s_mean: 0.5462
  - recall_4s_std: 0.2964
  - recall_10s_mean: 0.6838
  - recall_10s_std: 0.3028
  - precision_4s_mean: 0.2209
  - precision_4s_std: 0.1706
  - precision_10s_mean: 0.2948
  - precision_10s_std: 0.2252
  - edd_median_s_mean: 2.9598
  - fp_per_min_mean: 1.7998
  - nab_score_standard_mean: -1.9907
  - nab_score_standard_std: 6.0853
  - nab_score_low_fp_mean: -3.6807
  - nab_score_low_fp_std: 9.4744
  - nab_score_low_fn_mean: -4.251
  - nab_score_low_fn_std: 9.3971
  - n_ground_truth_sum: 712.0
  - n_detections_sum: 2461.0

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.477
  - primary_metric_in_opposite_fold: 0.4768
  - generalization_gap: 0.00019999999999997797
  - parameter_values: {'window_size': 100.0, 'regime_threshold': 0.7, 'regime_landmark': 4.0, 'min_gap_samples': 500.0}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.477
  - primary_metric_in_opposite_fold: 0.4768
  - generalization_gap: 0.00019999999999997797
  - parameter_values: {'window_size': 100.0, 'regime_threshold': 0.7, 'regime_landmark': 4.0, 'min_gap_samples': 500.0}
- Mean Cross Primary Metric:
  - value: 0.4662