"""
Test parameter portability across datasets (Option 2).

For each detector:
1. Extract best hyperparameters from source dataset (from two-fold report)
2. Filter predictions_intermediate.csv in target datasets with those exact parameters
3. Calculate F3 performance with transferred parameters
4. Compare with local best performance
5. Report transferability score
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Any
import sys
from datetime import datetime
import csv


def load_twofold_report(dataset: str, detector: str) -> Dict[str, Any]:
    """Load two-fold report for a detector/dataset."""
    path = Path(f"/home/franz/ts-segmentation/results/{dataset}/{detector}/final_report_with_nab_twofold_seed42.json")
    with open(path) as f:
        return json.load(f)


def extract_best_params(report: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the best hyperparameters from selection_guidance."""
    guidance = report.get("selection_guidance", {})
    highest_cross = guidance.get("highest_cross_primary_metric", {})
    params = highest_cross.get("parameter_values", {})
    cross_f3 = highest_cross.get("primary_metric_in_opposite_fold", None)

    return {
        "params": params,
        "cross_fold_f3": cross_f3,
        "selected_fold": highest_cross.get("fold", None)
    }


def load_metrics_csv(dataset: str, detector: str) -> pd.DataFrame:
    """Load metrics_comprehensive_with_nab.csv for a dataset/detector."""
    path = Path(f"/home/franz/ts-segmentation/results/{dataset}/{detector}/metrics_comprehensive_with_nab.csv")
    print(f"  Loading: {path.name} ({path.stat().st_size / 1e6:.1f} MB)")
    return pd.read_csv(path)


def filter_by_params(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """Filter dataframe to rows matching specific parameter values."""
    mask = pd.Series([True] * len(df), index=df.index)

    for param, value in params.items():
        if param in df.columns:
            # Handle floating point comparison with tolerance
            if isinstance(value, float):
                mask &= (df[param] - value).abs() < 1e-6
            else:
                mask &= df[param] == value

    return df[mask]


def calculate_f3_weighted(df: pd.DataFrame) -> float:
    """Calculate mean F3-weighted from filtered metrics."""
    if 'f3_weighted' in df.columns:
        return df['f3_weighted'].mean()
    return None


def test_parameter_transfer(
    source_dataset: str,
    target_dataset: str,
    detector: str
) -> Dict[str, Any]:
    """
    Test transferring parameters from source to target dataset.

    Returns dict with:
    - source_params: hyperparameters from source
    - source_cross_f3: performance in source (cross-fold)
    - target_transferred_f3: performance in target with transferred params
    - target_local_best_f3: best performance in target (optimized locally)
    - transferability_ratio: transferred / local_best
    - performance_drop: local_best - transferred
    """
    print(f"\n{'='*80}")
    print(f"Transfer Test: {detector.upper()} from {source_dataset} → {target_dataset}")
    print(f"{'='*80}")

    # Get best params from source
    source_report = load_twofold_report(source_dataset, detector)
    source_best = extract_best_params(source_report)
    source_params = source_best["params"]
    source_cross_f3 = source_best["cross_fold_f3"]

    print(f"\n📌 Source ({source_dataset}) best params:")
    for k, v in source_params.items():
        print(f"   {k}: {v}")
    print(f"   Cross-fold F3 in source: {source_cross_f3:.4f}")

    # Get local best from target
    target_report = load_twofold_report(target_dataset, detector)
    target_best = extract_best_params(target_report)
    target_local_f3 = target_best["cross_fold_f3"]

    print(f"\n📊 Target ({target_dataset}) local best:")
    print(f"   Cross-fold F3 (optimized): {target_local_f3:.4f}")

    # Load target metrics and filter by source params
    print(f"\n🔍 Testing transferred params in {target_dataset}...")
    target_df = load_metrics_csv(target_dataset, detector)
    filtered_df = filter_by_params(target_df, source_params)

    if len(filtered_df) == 0:
        print(f"   ⚠️  No matching rows found! Params may not be in target grid.")
        return None

    print(f"   Found {len(filtered_df):,} matching rows")

    # Calculate F3 with transferred params
    target_transferred_f3 = calculate_f3_weighted(filtered_df)

    if target_transferred_f3 is None:
        print(f"   ❌ Could not calculate F3 (missing column)")
        return None

    print(f"   Transferred F3: {target_transferred_f3:.4f}")

    # Calculate transferability metrics
    transferability_ratio = target_transferred_f3 / target_local_f3 if target_local_f3 > 0 else 0
    performance_drop = target_local_f3 - target_transferred_f3
    performance_drop_pct = (performance_drop / target_local_f3 * 100) if target_local_f3 > 0 else 0

    print(f"\n📈 Results:")
    print(f"   Transferability ratio: {transferability_ratio:.2%} ({target_transferred_f3:.4f}/{target_local_f3:.4f})")
    print(f"   Performance drop: {performance_drop:.4f} ({performance_drop_pct:.1f}%)")

    # Interpretation
    if transferability_ratio >= 0.95:
        interpretation = "✅ Excellent transfer"
    elif transferability_ratio >= 0.85:
        interpretation = "✅ Good transfer"
    elif transferability_ratio >= 0.75:
        interpretation = "⚠️  Acceptable transfer"
    elif transferability_ratio >= 0.60:
        interpretation = "⚠️  Moderate transfer"
    else:
        interpretation = "❌ Poor transfer"

    print(f"   {interpretation}")

    return {
        "source_dataset": source_dataset,
        "target_dataset": target_dataset,
        "detector": detector,
        "source_params": source_params,
        "source_cross_f3": source_cross_f3,
        "target_transferred_f3": target_transferred_f3,
        "target_local_best_f3": target_local_f3,
        "transferability_ratio": transferability_ratio,
        "performance_drop": performance_drop,
        "performance_drop_pct": performance_drop_pct,
        "interpretation": interpretation
    }


def run_full_transfer_analysis() -> List[Dict[str, Any]]:
    """
    Run full leave-one-dataset-out analysis.

    For each detector:
    - Test all source→target dataset pairs
    - Skip source==target (already measured in Option 1)
    """
    datasets = ["afib_paroxysmal", "malignantventricular", "vtachyarrhythmias"]
    detectors = ["adwin", "page_hinkley", "kswin", "hddm_a", "hddm_w", "floss"]

    results = []

    for detector in detectors:
        print(f"\n\n{'#'*100}")
        print(f"# DETECTOR: {detector.upper()}")
        print(f"{'#'*100}")

        for source_dataset in datasets:
            for target_dataset in datasets:
                if source_dataset == target_dataset:
                    continue  # Skip same-dataset (already in Option 1)

                try:
                    result = test_parameter_transfer(source_dataset, target_dataset, detector)
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"❌ Error: {e}")
                    import traceback
                    traceback.print_exc()

    return results


def generate_portability_report(results: List[Dict[str, Any]]) -> None:
    """Generate comprehensive portability report."""
    output_dir = Path("/home/franz/ts-segmentation/results/cross_dataset_analysis")
    output_dir.mkdir(exist_ok=True)

    if not results:
        print("⚠️  No results to report - all transfers failed")
        return

    # Export detailed CSV
    csv_path = output_dir / "parameter_portability_option2.csv"
    with open(csv_path, "w", newline="") as f:
        if results:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "detector", "source_dataset", "target_dataset",
                    "source_cross_f3", "target_transferred_f3", "target_local_best_f3",
                    "transferability_ratio", "performance_drop", "performance_drop_pct",
                    "interpretation"
                ]
            )
            writer.writeheader()

            for r in results:
                writer.writerow({
                    "detector": r["detector"],
                    "source_dataset": r["source_dataset"],
                    "target_dataset": r["target_dataset"],
                    "source_cross_f3": round(r["source_cross_f3"], 4),
                    "target_transferred_f3": round(r["target_transferred_f3"], 4),
                    "target_local_best_f3": round(r["target_local_best_f3"], 4),
                    "transferability_ratio": round(r["transferability_ratio"], 4),
                    "performance_drop": round(r["performance_drop"], 4),
                    "performance_drop_pct": round(r["performance_drop_pct"], 2),
                    "interpretation": r["interpretation"]
                })

    print(f"\n✅ CSV exported: {csv_path}")

    # Generate markdown report
    md_path = output_dir / "parameter_portability_option2.md"
    with open(md_path, "w") as f:
        f.write("# Parameter Portability Analysis (Option 2)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        f.write("## Executive Summary\n\n")
        f.write("This analysis tests **hyperparameter portability** by transferring the best parameters ")
        f.write("from one dataset to others, measuring real-world generalization.\n\n")

        f.write("### Methodology\n\n")
        f.write("1. Extract best hyperparameters from source dataset (from 2-fold CV)\n")
        f.write("2. Apply those exact parameters to target dataset (filter predictions_intermediate.csv)\n")
        f.write("3. Calculate F3 performance with transferred parameters\n")
        f.write("4. Compare with target's local best (optimized independently)\n")
        f.write("5. Compute transferability ratio = transferred_f3 / local_best_f3\n\n")

        f.write("**Interpretation**:\n")
        f.write("- Ratio ≥ 0.95 (≥95%): ✅ Excellent transfer (params are portable)\n")
        f.write("- Ratio ≥ 0.85 (≥85%): ✅ Good transfer\n")
        f.write("- Ratio ≥ 0.75 (≥75%): ⚠️  Acceptable transfer\n")
        f.write("- Ratio ≥ 0.60 (≥60%): ⚠️  Moderate transfer (consider re-tuning)\n")
        f.write("- Ratio < 0.60 (<60%): ❌ Poor transfer (re-tuning required)\n\n")

        f.write("---\n\n")

        # Per-detector summary
        f.write("## Summary by Detector\n\n")

        detectors = sorted(set(r["detector"] for r in results))

        for detector in detectors:
            detector_results = [r for r in results if r["detector"] == detector]
            avg_ratio = sum(r["transferability_ratio"] for r in detector_results) / len(detector_results)
            avg_drop = sum(r["performance_drop"] for r in detector_results) / len(detector_results)

            excellent = sum(1 for r in detector_results if r["transferability_ratio"] >= 0.95)
            good = sum(1 for r in detector_results if 0.85 <= r["transferability_ratio"] < 0.95)
            acceptable = sum(1 for r in detector_results if 0.75 <= r["transferability_ratio"] < 0.85)
            moderate = sum(1 for r in detector_results if 0.60 <= r["transferability_ratio"] < 0.75)
            poor = sum(1 for r in detector_results if r["transferability_ratio"] < 0.60)

            f.write(f"### {detector.upper()}\n\n")
            f.write(f"**Overall Portability**:\n")
            f.write(f"- Average transferability ratio: **{avg_ratio:.2%}**\n")
            f.write(f"- Average performance drop: {avg_drop:.4f} ({avg_drop/0.4*100:.1f}% relative)\n")
            f.write(f"- Transfer quality distribution:\n")
            f.write(f"  - ✅ Excellent (≥95%): {excellent}/{len(detector_results)}\n")
            f.write(f"  - ✅ Good (≥85%): {good}/{len(detector_results)}\n")
            f.write(f"  - ⚠️  Acceptable (≥75%): {acceptable}/{len(detector_results)}\n")
            f.write(f"  - ⚠️  Moderate (≥60%): {moderate}/{len(detector_results)}\n")
            f.write(f"  - ❌ Poor (<60%): {poor}/{len(detector_results)}\n\n")

            f.write("**Transfer Matrix**:\n\n")
            f.write("| Source → Target | Transferred F3 | Local Best F3 | Ratio | Drop | Status |\n")
            f.write("|-----------------|----------------|---------------|-------|------|--------|\n")

            for r in detector_results:
                source_short = r["source_dataset"][:6]
                target_short = r["target_dataset"][:6]
                f.write(
                    f"| {source_short} → {target_short} | {r['target_transferred_f3']:.4f} | "
                    f"{r['target_local_best_f3']:.4f} | {r['transferability_ratio']:.2%} | "
                    f"{r['performance_drop']:.4f} | {r['interpretation']} |\n"
                )

            f.write("\n")

        f.write("---\n\n")

        # Best source datasets
        f.write("## Best Source Datasets for Transfer\n\n")
        f.write("Which dataset's parameters transfer best to others?\n\n")

        datasets = ["afib_paroxysmal", "malignantventricular", "vtachyarrhythmias"]

        for source in datasets:
            source_results = [r for r in results if r["source_dataset"] == source]
            if source_results:
                avg_ratio = sum(r["transferability_ratio"] for r in source_results) / len(source_results)
                f.write(f"### {source}\n")
                f.write(f"- Average transferability to other datasets: **{avg_ratio:.2%}**\n")
                f.write(f"- Number of transfers tested: {len(source_results)}\n\n")

        f.write("---\n\n")

        # Recommendations
        f.write("## Recommendations for Production\n\n")

        # Find best overall portability
        detector_avg_ratios = {}
        for detector in detectors:
            detector_results = [r for r in results if r["detector"] == detector]
            detector_avg_ratios[detector] = sum(r["transferability_ratio"] for r in detector_results) / len(detector_results)

        best_detector = max(detector_avg_ratios.items(), key=lambda x: x[1])

        f.write(f"### Best Overall Portability: {best_detector[0].upper()}\n")
        f.write(f"- Average transferability: {best_detector[1]:.2%}\n")
        f.write(f"- This detector's parameters transfer best across different ECG datasets\n")
        f.write(f"- **Recommendation**: Safe to use parameters from any dataset on new data\n\n")

        f.write("### Use Cases\n\n")
        for detector, avg_ratio in sorted(detector_avg_ratios.items(), key=lambda x: x[1], reverse=True):
            if avg_ratio >= 0.85:
                f.write(f"**{detector.upper()}**: ✅ Portable (avg {avg_ratio:.2%})\n")
                f.write(f"  - Can use parameters from training dataset on production data\n")
                f.write(f"  - Minimal re-tuning needed\n\n")
            elif avg_ratio >= 0.75:
                f.write(f"**{detector.upper()}**: ⚠️  Moderately portable (avg {avg_ratio:.2%})\n")
                f.write(f"  - Consider validation on small sample before full deployment\n")
                f.write(f"  - May benefit from light re-tuning\n\n")
            else:
                f.write(f"**{detector.upper()}**: ❌ Limited portability (avg {avg_ratio:.2%})\n")
                f.write(f"  - Re-tuning strongly recommended for new datasets\n")
                f.write(f"  - Use with caution in production without validation\n\n")

    print(f"✅ Report exported: {md_path}")


def main():
    """Main execution."""
    print("\n" + "="*100)
    print("PARAMETER PORTABILITY TESTING (OPTION 2)")
    print("="*100)
    print("\nThis will test transferring hyperparameters between datasets.")
    print("Expected tests: 6 detectors × 3 datasets × 2 target datasets = 36 transfers\n")

    results = run_full_transfer_analysis()

    print("\n\n" + "="*100)
    print("GENERATING REPORT")
    print("="*100)

    generate_portability_report(results)

    print("\n✅ Parameter portability analysis complete!")
    print(f"   Total transfers tested: {len(results)}")


if __name__ == "__main__":
    main()
