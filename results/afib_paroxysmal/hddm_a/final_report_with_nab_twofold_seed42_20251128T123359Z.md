# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:33:59.796101 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/afib_paroxysmal/fold_assignments_seed42.json
Fold sizes: {'fold_a': 114, 'fold_b': 115}
---
## FOLD_A
- Records: 114
- Unique files: 114
- Best params: drift_confidence: 0.005, warning_confidence: 0.001, two_side_option: True, ma_window: 1, min_gap_samples: 1000
- Primary metric in fold: 0.3725
- Primary metric in opposite fold: 0.3451
- Generalization gap: 0.02739999999999998
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.005
  - warning_confidence: 0.001
  - two_side_option: True
  - ma_window: 1
  - min_gap_samples: 1000
  - f1_classic_mean: 0.1614
  - f1_classic_std: 0.1574
  - f1_classic_count: 115
  - f1_weighted_mean: 0.1438
  - f1_weighted_std: 0.1349
  - f1_weighted_count: 115
  - f3_classic_mean: 0.3772
  - f3_classic_std: 0.2183
  - f3_classic_count: 115
  - f3_weighted_mean: 0.3451
  - f3_weighted_std: 0.1966
  - f3_weighted_count: 115
  - recall_4s_mean: 0.6958
  - recall_4s_std: 0.2943
  - recall_10s_mean: 0.8929
  - recall_10s_std: 0.1876
  - precision_4s_mean: 0.0693
  - precision_4s_std: 0.0829
  - precision_10s_mean: 0.1022
  - precision_10s_std: 0.1197
  - edd_median_s_mean: 2.8074
  - fp_per_min_mean: 9.308
  - nab_score_standard_mean: -9.1502
  - nab_score_standard_std: 18.0197
  - nab_score_low_fp_mean: -20.2882
  - nab_score_low_fp_std: 36.3356
  - nab_score_low_fn_mean: -4.8855
  - nab_score_low_fn_std: 9.6106
  - n_ground_truth_sum: 589
  - n_detections_sum: 14557

## FOLD_B
- Records: 115
- Unique files: 115
- Best params: drift_confidence: 0.005, warning_confidence: 0.001, two_side_option: True, ma_window: 1, min_gap_samples: 1000
- Primary metric in fold: 0.3451
- Primary metric in opposite fold: 0.3725
- Generalization gap: 0.02739999999999998
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.005
  - warning_confidence: 0.001
  - two_side_option: True
  - ma_window: 1
  - min_gap_samples: 1000
  - f1_classic_mean: 0.1873
  - f1_classic_std: 0.1737
  - f1_classic_count: 114
  - f1_weighted_mean: 0.1658
  - f1_weighted_std: 0.1492
  - f1_weighted_count: 114
  - f3_classic_mean: 0.4114
  - f3_classic_std: 0.2105
  - f3_classic_count: 114
  - f3_weighted_mean: 0.3725
  - f3_weighted_std: 0.1929
  - f3_weighted_count: 114
  - recall_4s_mean: 0.6996
  - recall_4s_std: 0.2917
  - recall_10s_mean: 0.8827
  - recall_10s_std: 0.2167
  - precision_4s_mean: 0.0802
  - precision_4s_std: 0.0934
  - precision_10s_mean: 0.125
  - precision_10s_std: 0.1502
  - edd_median_s_mean: 2.8949
  - fp_per_min_mean: 8.9841
  - nab_score_standard_mean: -9.7709
  - nab_score_standard_std: 36.3402
  - nab_score_low_fp_mean: -21.2451
  - nab_score_low_fp_std: 72.4635
  - nab_score_low_fn_mean: -5.9548
  - nab_score_low_fn_std: 18.6143
  - n_ground_truth_sum: 712
  - n_detections_sum: 14594

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.3451
  - primary_metric_in_opposite_fold: 0.3725
  - generalization_gap: 0.02739999999999998
  - parameter_values: {'drift_confidence': 0.005, 'warning_confidence': 0.001, 'two_side_option': True, 'ma_window': 1, 'min_gap_samples': 1000}
- Smallest Generalization Gap:
  - fold: fold_a
  - primary_metric_in_fold: 0.3725
  - primary_metric_in_opposite_fold: 0.3451
  - generalization_gap: 0.02739999999999998
  - parameter_values: {'drift_confidence': 0.005, 'warning_confidence': 0.001, 'two_side_option': True, 'ma_window': 1, 'min_gap_samples': 1000}
- Mean Cross Primary Metric:
  - value: 0.3588