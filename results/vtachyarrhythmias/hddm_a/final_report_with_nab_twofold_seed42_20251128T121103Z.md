# Two-Fold Robustness Snapshot
Generated: 2025-11-28T12:11:03.584812 UTC
Seed: 42
Primary metric column: f3_weighted_mean
Fold assignments file: results/vtachyarrhythmias/fold_assignments_seed42.json
Fold sizes: {'fold_a': 17, 'fold_b': 17}
---
## FOLD_A
- Records: 17
- Unique files: 17
- Best params: drift_confidence: 0.0001, warning_confidence: 0.001, two_side_option: False, ma_window: 10, min_gap_samples: 2000
- Primary metric in fold: 0.261
- Primary metric in opposite fold: 0.1825
- Generalization gap: 0.07850000000000001
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.0001
  - warning_confidence: 0.001
  - two_side_option: False
  - ma_window: 10
  - min_gap_samples: 2000
  - f1_classic_mean: 0.0714
  - f1_classic_std: 0.0561
  - f1_classic_count: 17
  - f1_weighted_mean: 0.0526
  - f1_weighted_std: 0.0502
  - f1_weighted_count: 17
  - f3_classic_mean: 0.2505
  - f3_classic_std: 0.1302
  - f3_classic_count: 17
  - f3_weighted_mean: 0.1825
  - f3_weighted_std: 0.1243
  - f3_weighted_count: 17
  - recall_4s_mean: 0.4265
  - recall_4s_std: 0.4525
  - recall_10s_mean: 0.9804
  - recall_10s_std: 0.0808
  - precision_4s_mean: 0.0179
  - precision_4s_std: 0.0254
  - precision_10s_mean: 0.0382
  - precision_10s_std: 0.0323
  - edd_median_s_mean: 4.6091
  - fp_per_min_mean: 7.0182
  - nab_score_standard_mean: -3.906
  - nab_score_standard_std: 1.9619
  - nab_score_low_fp_mean: -9.3466
  - nab_score_low_fp_std: 2.1886
  - nab_score_low_fn_mean: -1.421
  - nab_score_low_fn_std: 2.3664
  - n_ground_truth_sum: 43
  - n_detections_sum: 1059

## FOLD_B
- Records: 17
- Unique files: 17
- Best params: drift_confidence: 0.0001, warning_confidence: 0.001, two_side_option: True, ma_window: 100, min_gap_samples: 3000
- Primary metric in fold: 0.2032
- Primary metric in opposite fold: 0.2248
- Generalization gap: 0.021600000000000008
- Cross-fold metrics (opposite fold):
  - drift_confidence: 0.0001
  - warning_confidence: 0.001
  - two_side_option: True
  - ma_window: 100
  - min_gap_samples: 3000
  - f1_classic_mean: 0.1087
  - f1_classic_std: 0.0868
  - f1_classic_count: 17
  - f1_weighted_mean: 0.0749
  - f1_weighted_std: 0.0565
  - f1_weighted_count: 17
  - f3_classic_mean: 0.3196
  - f3_classic_std: 0.1697
  - f3_classic_count: 17
  - f3_weighted_mean: 0.2248
  - f3_weighted_std: 0.1248
  - f3_weighted_count: 17
  - recall_4s_mean: 0.4245
  - recall_4s_std: 0.39
  - recall_10s_mean: 0.8235
  - recall_10s_std: 0.2835
  - precision_4s_mean: 0.0248
  - precision_4s_std: 0.0194
  - precision_10s_mean: 0.0607
  - precision_10s_std: 0.0534
  - edd_median_s_mean: 4.4398
  - fp_per_min_mean: 4.7297
  - nab_score_standard_mean: -2.6199
  - nab_score_standard_std: 1.6917
  - nab_score_low_fp_mean: -6.282
  - nab_score_low_fp_std: 1.8776
  - nab_score_low_fn_mean: -1.5535
  - nab_score_low_fn_std: 2.1941
  - n_ground_truth_sum: 54
  - n_detections_sum: 726

## Selection Guidance
- Highest Cross Primary Metric:
  - fold: fold_b
  - primary_metric_in_fold: 0.2032
  - primary_metric_in_opposite_fold: 0.2248
  - generalization_gap: 0.021600000000000008
  - parameter_values: {'drift_confidence': 0.0001, 'warning_confidence': 0.001, 'two_side_option': True, 'ma_window': 100, 'min_gap_samples': 3000}
- Smallest Generalization Gap:
  - fold: fold_b
  - primary_metric_in_fold: 0.2032
  - primary_metric_in_opposite_fold: 0.2248
  - generalization_gap: 0.021600000000000008
  - parameter_values: {'drift_confidence': 0.0001, 'warning_confidence': 0.001, 'two_side_option': True, 'ma_window': 100, 'min_gap_samples': 3000}
- Mean Cross Primary Metric:
  - value: 0.20365