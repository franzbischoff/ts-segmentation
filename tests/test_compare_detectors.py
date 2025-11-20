import pandas as pd
import numpy as np
from src.compare_detectors import aggregate_metrics_by_params, generate_robustness_analysis


def test_aggregate_metrics_by_params_simple():
    # Setup sample data with repeated parameter combos
    data = [
        {"record_id": "r1", "detector": "adwin", "delta": 0.01, "ma_window": 10, "f3_weighted": 0.5, "f1_weighted": 0.6},
        {"record_id": "r1", "detector": "adwin", "delta": 0.01, "ma_window": 10, "f3_weighted": 0.7, "f1_weighted": 0.5},
        {"record_id": "r2", "detector": "adwin", "delta": 0.03, "ma_window": 50, "f3_weighted": 0.9, "f1_weighted": 0.85},
    ]

    df = pd.DataFrame(data)

    aggregated = aggregate_metrics_by_params(df)

    # Should have two unique parameter combos
    assert len(aggregated) == 2
    # Check mean calculated for f3_weighted for the first combo
    row = aggregated[(aggregated['delta'] == 0.01) & (aggregated['ma_window'] == 10)]
    assert not row.empty
    assert np.isclose(row['f3_weighted'].iloc[0], 0.6)


def test_generate_robustness_analysis_topn_and_count():
    # Create a list of unique parameter combos
    rows = []
    for i in range(15):
        rows.append(
            {
                "record_id": f"r{i}",
                "detector": "kswin",
                "alpha": 0.005,
                "window_size": (i % 5) * 50 + 50,
                "stat_size": (i % 4) * 10 + 20,
                "ma_window": (i % 3) * 10 + 1,
                "f3_weighted": 1.0 - (i * 0.01),
                "f1_weighted": 0.5 + (i * 0.01),
                "recall_10s": 0.6 + (i * 0.02),
                "precision_10s": 0.7 - (i * 0.01),
                "edd_median_s": 2.0 + (i * 0.1),
                "fp_per_min": 0.05 + (i * 0.01),
                "nab_score_standard": 0.2 + i * 0.005,
            }
        )

    df = pd.DataFrame(rows)
    metrics_dfs = {"kswin": df}

    # Test top-n selection
    rob = generate_robustness_analysis(metrics_dfs, top_n=5, top_percent=0.0)
    assert not rob.empty

    # Check total configs for F3-Weighted for kswin equals number of unique combos
    f3_rows = rob[(rob['Metric'] == 'F3-Weighted') & (rob['Detector'] == 'kswin')]
    assert not f3_rows.empty
    total_configs = int(f3_rows['Total Configs'].iloc[0])
    assert total_configs == len(df)

    # Check that Top-10 Mean is a numeric string
    top10_str = f3_rows['Top-10 Mean'].iloc[0]
    try:
        float_val = float(top10_str)
        assert float_val > 0
    except Exception:
        assert False, "Top-10 Mean should be parseable as float"

    # Test top-percent selection: when top_percent selects fewer combos than top_n,
    # the Top-mean should be greater or equal (fewer top elements => larger mean).
    rob2 = generate_robustness_analysis(metrics_dfs, top_n=5, top_percent=10.0)
    f3_rows2 = rob2[(rob2['Metric'] == 'F3-Weighted') & (rob2['Detector'] == 'kswin')]
    assert not f3_rows2.empty
    cutoff = int(len(df) * 0.10) or 1
    if cutoff < 5:
        assert float(f3_rows2['Top-10 Mean'].iloc[0]) >= float(top10_str)
    else:
        assert float(f3_rows2['Top-10 Mean'].iloc[0]) <= float(top10_str)
