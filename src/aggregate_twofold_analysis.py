"""
Aggregate two-fold cross-validation results across all detectors and datasets.

For each detector×dataset combination:
1. Compares fold A→B and fold B→A performances
2. Selects the best generalizing configuration
3. Creates summary tables with robustness insights
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any
import sys
from datetime import datetime


def load_twofold_report(path: Path) -> Dict[str, Any]:
    """Load and parse a two-fold report JSON."""
    with open(path) as f:
        return json.load(f)


def extract_best_generalization(report: Dict[str, Any]) -> Tuple[str, float, float, float, Dict]:
    """
    Extract the configuration with best generalization.

    Rules:
    1. Compare fold_a→fold_b vs fold_b→fold_a cross-validation scores
    2. Select the one with higher cross-validation score (opposite fold)
    3. If tied, select the one with smallest generalization gap
    4. Return: (selected_fold, intra_fold_score, cross_fold_score, gap, params)
    """
    folds = report["fold_reports"]
    metric_col = report["primary_metric_column"]

    fold_a = folds["fold_a"]
    fold_b = folds["fold_b"]

    # Get metrics for each fold
    fold_a_intra = fold_a["primary_metric_in_fold"]
    fold_a_cross = fold_a["primary_metric_in_opposite_fold"]
    fold_a_gap = fold_a["generalization_gap"]

    fold_b_intra = fold_b["primary_metric_in_fold"]
    fold_b_cross = fold_b["primary_metric_in_opposite_fold"]
    fold_b_gap = fold_b["generalization_gap"]

    # Compare cross-fold scores (performance in opposite fold)
    if abs(fold_a_cross - fold_b_cross) > 1e-6:  # Not equal
        if fold_a_cross > fold_b_cross:
            selected_fold = "fold_a"
        else:
            selected_fold = "fold_b"
    else:  # Tied, use generalization gap
        if fold_a_gap < fold_b_gap:
            selected_fold = "fold_a"
        else:
            selected_fold = "fold_b"

    if selected_fold == "fold_a":
        params = fold_a["best_params_in_fold"]
        intra = fold_a_intra
        cross = fold_a_cross
        gap = fold_a_gap
    else:
        params = fold_b["best_params_in_fold"]
        intra = fold_b_intra
        cross = fold_b_cross
        gap = fold_b_gap

    # Extract only parameter values (skip metrics)
    param_keys = [k for k in params.keys() if not k.endswith("_mean") and not k.endswith("_std") and not k.endswith("_count") and not k.endswith("_sum")]
    selected_params = {k: params[k] for k in param_keys}

    return selected_fold, intra, cross, gap, selected_params


def process_all_twofold_reports() -> Dict[str, List[Dict]]:
    """
    Process all two-fold reports and aggregate results.

    Returns dict: {
        dataset: [
            {
                detector: str,
                best_fold: str,
                intra_fold_f3: float,
                cross_fold_f3: float,
                gap: float,
                parameters: dict
            },
            ...
        ]
    }
    """
    results_dir = Path("/home/franz/ts-segmentation/results")
    datasets = ["afib_paroxysmal", "malignantventricular", "vtachyarrhythmias"]
    detectors = ["adwin", "page_hinkley", "kswin", "hddm_a", "hddm_w", "floss"]

    aggregated = {ds: [] for ds in datasets}

    for dataset in datasets:
        for detector in detectors:
            report_path = results_dir / dataset / detector / "final_report_with_nab_twofold_seed42.json"

            if not report_path.exists():
                print(f"⚠️  Missing: {dataset}/{detector}", file=sys.stderr)
                continue

            try:
                report = load_twofold_report(report_path)
                selected_fold, intra, cross, gap, params = extract_best_generalization(report)

                aggregated[dataset].append({
                    "detector": detector,
                    "selected_fold": selected_fold,
                    "intra_fold_f3": round(intra, 4),
                    "cross_fold_f3": round(cross, 4),
                    "generalization_gap": round(gap, 4),
                    "parameters": params
                })
            except Exception as e:
                print(f"❌ Error processing {dataset}/{detector}: {e}", file=sys.stderr)

    return aggregated


def generate_robustness_table(aggregated: Dict[str, List[Dict]]) -> None:
    """
    Generate robustness metrics table.

    Shows for each detector:
    - Average cross-fold F3 across datasets
    - Average generalization gap (lower = more robust)
    - How often it was selected from fold_a vs fold_b
    """
    detectors_data = {}

    for dataset, entries in aggregated.items():
        for entry in entries:
            detector = entry["detector"]
            if detector not in detectors_data:
                detectors_data[detector] = {
                    "cross_fold_scores": [],
                    "gaps": [],
                    "fold_selections": []
                }

            detectors_data[detector]["cross_fold_scores"].append(entry["cross_fold_f3"])
            detectors_data[detector]["gaps"].append(entry["generalization_gap"])
            detectors_data[detector]["fold_selections"].append(entry["selected_fold"])

    print("\n" + "="*100)
    print("ROBUSTNESS RANKING (Generalization across Datasets)")
    print("="*100)
    print(f"{'Detector':<15} {'Avg Cross-Fold F3':<20} {'Avg Gap':<15} {'Fold-A %':<12} {'Robust?':<10}")
    print("-"*100)

    # Sort by average gap (smaller = better)
    sorted_detectors = sorted(
        detectors_data.items(),
        key=lambda x: sum(x[1]["gaps"]) / len(x[1]["gaps"])
    )

    for detector, data in sorted_detectors:
        avg_cross = sum(data["cross_fold_scores"]) / len(data["cross_fold_scores"])
        avg_gap = sum(data["gaps"]) / len(data["gaps"])
        fold_a_pct = (data["fold_selections"].count("fold_a") / len(data["fold_selections"])) * 100

        # Robust if avg_gap < 0.05
        robust = "✅ YES" if avg_gap < 0.05 else "⚠️  MEDIUM" if avg_gap < 0.10 else "❌ NO"

        print(f"{detector:<15} {avg_cross:<20.4f} {avg_gap:<15.4f} {fold_a_pct:<12.1f}% {robust:<10}")

    print("="*100)


def generate_dataset_comparison_table(aggregated: Dict[str, List[Dict]]) -> None:
    """
    Generate dataset-by-dataset comparison table.

    Shows for each detector × dataset, the cross-fold F3 score.
    Highlights which detector generalizes best per dataset.
    """
    print("\n" + "="*100)
    print("CROSS-FOLD PERFORMANCE BY DATASET")
    print("="*100)

    datasets = list(aggregated.keys())

    for dataset in datasets:
        entries = aggregated[dataset]
        entries_sorted = sorted(entries, key=lambda x: x["cross_fold_f3"], reverse=True)

        print(f"\n📊 Dataset: {dataset}")
        print(f"{'Detector':<15} {'Cross-Fold F3':<18} {'Intra-Fold F3':<18} {'Gap':<12} {'Rank':<6}")
        print("-"*75)

        for rank, entry in enumerate(entries_sorted, 1):
            detector = entry["detector"]
            cross = entry["cross_fold_f3"]
            intra = entry["intra_fold_f3"]
            gap = entry["generalization_gap"]

            print(f"{detector:<15} {cross:<18.4f} {intra:<18.4f} {gap:<12.4f} {rank:<6}")


def generate_generalization_gap_analysis(aggregated: Dict[str, List[Dict]]) -> None:
    """
    Show which detectors have smallest generalization gap (most robust).
    """
    print("\n" + "="*100)
    print("GENERALIZATION GAP ANALYSIS (Lower = More Robust)")
    print("="*100)

    all_entries = []
    for dataset, entries in aggregated.items():
        for entry in entries:
            all_entries.append({
                **entry,
                "dataset": dataset
            })

    # Group by detector and show per-dataset gaps
    detectors = set(e["detector"] for e in all_entries)

    for detector in sorted(detectors):
        entries = [e for e in all_entries if e["detector"] == detector]
        entries_sorted = sorted(entries, key=lambda x: x["generalization_gap"])

        print(f"\n🔍 {detector.upper()}")
        print(f"{'Dataset':<25} {'Gap':<12} {'Cross-Fold F3':<18}")
        print("-"*55)

        avg_gap = sum(e["generalization_gap"] for e in entries) / len(entries)

        for entry in entries_sorted:
            gap = entry["generalization_gap"]
            cross = entry["cross_fold_f3"]
            dataset = entry["dataset"]
            print(f"{dataset:<25} {gap:<12.4f} {cross:<18.4f}")

        print(f"{'AVERAGE':<25} {avg_gap:<12.4f}")


def export_csv_results(aggregated: Dict[str, List[Dict]]) -> None:
    """Export aggregated results to CSV for each dataset."""
    output_dir = Path("/home/franz/ts-segmentation/results/cross_dataset_analysis")
    output_dir.mkdir(exist_ok=True)

    for dataset, entries in aggregated.items():
        csv_path = output_dir / f"twofold_robustness_{dataset}.csv"

        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "detector",
                    "selected_fold",
                    "intra_fold_f3",
                    "cross_fold_f3",
                    "generalization_gap"
                ]
            )
            writer.writeheader()

            for entry in entries:
                writer.writerow({
                    "detector": entry["detector"],
                    "selected_fold": entry["selected_fold"],
                    "intra_fold_f3": entry["intra_fold_f3"],
                    "cross_fold_f3": entry["cross_fold_f3"],
                    "generalization_gap": entry["generalization_gap"]
                })

        print(f"✅ Exported: {csv_path}")


def generate_summary_report(aggregated: Dict[str, List[Dict]]) -> None:
    """Generate a markdown summary report."""
    output_path = Path("/home/franz/ts-segmentation/results/cross_dataset_analysis/twofold_analysis_summary.md")
    output_dir = output_path.parent
    output_dir.mkdir(exist_ok=True)

    with open(output_path, "w") as f:
        f.write("# Two-Fold Cross-Validation Analysis Summary\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        f.write("## Executive Summary\n\n")
        f.write("This analysis evaluates detector robustness by measuring how well hyperparameters\n")
        f.write("optimized in one data fold generalize to the opposite fold.\n\n")

        f.write("### Selection Methodology\n\n")
        f.write("For each detector×dataset:\n")
        f.write("1. Train on Fold A, evaluate on Fold A and Fold B → get cross-fold score A→B\n")
        f.write("2. Train on Fold B, evaluate on Fold B and Fold A → get cross-fold score B→A\n")
        f.write("3. **Select the fold with HIGHEST cross-fold score** (best generalization)\n")
        f.write("4. If tied, select the fold with **SMALLEST generalization gap**\n\n")

        f.write("---\n\n")

        # Robustness rankings
        detectors_data = {}
        for dataset, entries in aggregated.items():
            for entry in entries:
                detector = entry["detector"]
                if detector not in detectors_data:
                    detectors_data[detector] = {
                        "cross_fold_scores": [],
                        "gaps": [],
                    }
                detectors_data[detector]["cross_fold_scores"].append(entry["cross_fold_f3"])
                detectors_data[detector]["gaps"].append(entry["generalization_gap"])

        f.write("## Robustness Ranking\n\n")
        f.write("| Detector | Avg Cross-Fold F3 | Avg Gap | Robustness |\n")
        f.write("|----------|-------------------|---------|------------|\n")

        sorted_detectors = sorted(
            detectors_data.items(),
            key=lambda x: sum(x[1]["gaps"]) / len(x[1]["gaps"])
        )

        for detector, data in sorted_detectors:
            avg_cross = sum(data["cross_fold_scores"]) / len(data["cross_fold_scores"])
            avg_gap = sum(data["gaps"]) / len(data["gaps"])
            robust = "✅ Excellent" if avg_gap < 0.05 else "⚠️  Good" if avg_gap < 0.10 else "❌ Poor"
            f.write(f"| {detector} | {avg_cross:.4f} | {avg_gap:.4f} | {robust} |\n")

        f.write("\n---\n\n")

        # Per-dataset details
        f.write("## Per-Dataset Analysis\n\n")

        for dataset in sorted(aggregated.keys()):
            entries = aggregated[dataset]
            entries_sorted = sorted(entries, key=lambda x: x["cross_fold_f3"], reverse=True)

            f.write(f"### {dataset}\n\n")
            f.write("| Rank | Detector | Cross-Fold F3 | Intra-Fold F3 | Gap | Selected Fold |\n")
            f.write("|------|----------|---------------|---------------|-----|---------------|\n")

            for rank, entry in enumerate(entries_sorted, 1):
                f.write(
                    f"| {rank} | {entry['detector']} | {entry['cross_fold_f3']:.4f} | "
                    f"{entry['intra_fold_f3']:.4f} | {entry['generalization_gap']:.4f} | "
                    f"{entry['selected_fold']} |\n"
                )

            f.write("\n")

    print(f"✅ Report exported: {output_path}")


def generate_cross_dataset_generalization_report(aggregated: Dict[str, List[Dict]]) -> None:
    """
    Generate cross-dataset analysis using generalization (cross-fold) scores.

    This shows the "performance ceiling" when each detector is properly tuned
    per dataset, using cross-fold scores (more realistic than intra-fold).
    """
    import statistics

    output_path = Path("/home/franz/ts-segmentation/results/cross_dataset_analysis/cross_dataset_generalization_option1.md")
    output_dir = output_path.parent
    output_dir.mkdir(exist_ok=True)

    # Organize by detector
    detector_stats = {}
    detectors = ["adwin", "page_hinkley", "kswin", "hddm_a", "hddm_w", "floss"]

    for detector in detectors:
        cross_fold_scores = []
        intra_fold_scores = []
        gaps = []
        dataset_names = []

        for dataset, entries in aggregated.items():
            for entry in entries:
                if entry["detector"] == detector:
                    cross_fold_scores.append(entry["cross_fold_f3"])
                    intra_fold_scores.append(entry["intra_fold_f3"])
                    gaps.append(entry["generalization_gap"])
                    dataset_names.append(dataset)

        if cross_fold_scores:
            detector_stats[detector] = {
                "cross_fold_scores": cross_fold_scores,
                "intra_fold_scores": intra_fold_scores,
                "gaps": gaps,
                "datasets": dataset_names,
                "mean_cross": statistics.mean(cross_fold_scores),
                "median_cross": statistics.median(cross_fold_scores),
                "std_cross": statistics.stdev(cross_fold_scores) if len(cross_fold_scores) > 1 else 0,
                "min_cross": min(cross_fold_scores),
                "max_cross": max(cross_fold_scores),
                "mean_gap": statistics.mean(gaps),
                "cv_cross": (statistics.stdev(cross_fold_scores) / statistics.mean(cross_fold_scores) * 100) if len(cross_fold_scores) > 1 and statistics.mean(cross_fold_scores) > 0 else 0
            }

    with open(output_path, "w") as f:
        f.write("# Cross-Dataset Generalization Analysis (Option 1)\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        f.write("## Executive Summary\n\n")
        f.write("This analysis shows the **performance ceiling** of each detector when properly tuned ")
        f.write("per dataset, using **cross-fold F3 scores** (generalization metric from 2-fold validation).\n\n")

        f.write("### Key Concept\n\n")
        f.write("- Each detector was optimized **independently** on each dataset (using 2-fold CV)\n")
        f.write("- We use the **cross-fold F3 score** (performance on opposite fold) as the metric\n")
        f.write("- Cross-fold scores are more realistic than intra-fold (test on unseen data)\n")
        f.write("- This shows: **\"What's the best each detector can do when properly tuned?\"**\n\n")

        f.write("**Different from Option 2**: This does NOT test parameter portability. ")
        f.write("Each dataset uses its own best parameters.\n\n")

        f.write("---\n\n")

        # Overall ranking
        f.write("## Overall Ranking (by Mean Cross-Fold F3)\n\n")
        f.write("| Rank | Detector | Mean F3 | Median F3 | Std Dev | Min | Max | CV% | Avg Gap |\n")
        f.write("|------|----------|---------|-----------|---------|-----|-----|-----|----------|\n")

        sorted_detectors = sorted(
            detector_stats.items(),
            key=lambda x: x[1]["mean_cross"],
            reverse=True
        )

        for rank, (detector, stats) in enumerate(sorted_detectors, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}"
            f.write(
                f"| {medal} | {detector} | {stats['mean_cross']:.4f} | {stats['median_cross']:.4f} | "
                f"{stats['std_cross']:.4f} | {stats['min_cross']:.4f} | {stats['max_cross']:.4f} | "
                f"{stats['cv_cross']:.1f}% | {stats['mean_gap']:.4f} |\n"
            )

        f.write("\n**Interpretation**:\n")
        f.write("- **Mean F3**: Average performance ceiling across 3 datasets (higher = better)\n")
        f.write("- **Std Dev**: Consistency across datasets (lower = more stable)\n")
        f.write("- **CV%**: Coefficient of variation (lower = more reliable)\n")
        f.write("- **Avg Gap**: Average generalization gap from 2-fold (lower = more robust)\n\n")

        f.write("---\n\n")

        # Consistency analysis
        f.write("## Consistency Analysis\n\n")
        f.write("### By Coefficient of Variation (CV%)\n\n")
        f.write("Lower CV% = more consistent performance across different datasets\n\n")

        sorted_by_cv = sorted(
            detector_stats.items(),
            key=lambda x: x[1]["cv_cross"]
        )

        f.write("| Rank | Detector | CV% | Interpretation |\n")
        f.write("|------|----------|-----|----------------|\n")

        for rank, (detector, stats) in enumerate(sorted_by_cv, 1):
            cv = stats['cv_cross']
            interpretation = "Excellent" if cv < 20 else "Good" if cv < 30 else "Moderate" if cv < 40 else "Variable"
            f.write(f"| {rank} | {detector} | {cv:.1f}% | {interpretation} |\n")

        f.write("\n---\n\n")

        # Per-detector details
        f.write("## Detailed Breakdown by Detector\n\n")

        for detector in sorted(detector_stats.keys()):
            stats = detector_stats[detector]
            f.write(f"### {detector.upper()}\n\n")

            f.write(f"**Summary Statistics**:\n")
            f.write(f"- Mean Cross-Fold F3: **{stats['mean_cross']:.4f}**\n")
            f.write(f"- Median: {stats['median_cross']:.4f}\n")
            f.write(f"- Std Dev: {stats['std_cross']:.4f}\n")
            f.write(f"- Range: [{stats['min_cross']:.4f}, {stats['max_cross']:.4f}]\n")
            f.write(f"- CV%: {stats['cv_cross']:.1f}%\n")
            f.write(f"- Avg Generalization Gap: {stats['mean_gap']:.4f}\n\n")

            f.write("**Per-Dataset Performance**:\n\n")
            f.write("| Dataset | Cross-Fold F3 | Intra-Fold F3 | Gap |\n")
            f.write("|---------|---------------|---------------|-----|\n")

            for i, dataset in enumerate(stats['datasets']):
                cross = stats['cross_fold_scores'][i]
                intra = stats['intra_fold_scores'][i]
                gap = stats['gaps'][i]
                f.write(f"| {dataset} | {cross:.4f} | {intra:.4f} | {gap:.4f} |\n")

            # Insights
            f.write("\n**Insights**:\n")
            best_dataset_idx = stats['cross_fold_scores'].index(stats['max_cross'])
            worst_dataset_idx = stats['cross_fold_scores'].index(stats['min_cross'])
            f.write(f"- Best on: **{stats['datasets'][best_dataset_idx]}** (F3={stats['max_cross']:.4f})\n")
            f.write(f"- Weakest on: {stats['datasets'][worst_dataset_idx]} (F3={stats['min_cross']:.4f})\n")

            performance_drop = (stats['max_cross'] - stats['min_cross']) / stats['max_cross'] * 100
            f.write(f"- Performance variation: {performance_drop:.1f}% between best and worst dataset\n\n")

        f.write("---\n\n")

        # Key findings
        f.write("## Key Findings\n\n")

        best_detector = sorted_detectors[0][0]
        best_mean = sorted_detectors[0][1]["mean_cross"]

        most_consistent = sorted_by_cv[0][0]
        lowest_cv = sorted_by_cv[0][1]["cv_cross"]

        f.write(f"1. **Highest Average Performance**: {best_detector.upper()} (mean F3={best_mean:.4f})\n")
        f.write(f"   - This detector achieves the best performance when properly tuned per dataset\n\n")

        f.write(f"2. **Most Consistent**: {most_consistent.upper()} (CV={lowest_cv:.1f}%)\n")
        f.write(f"   - This detector shows most stable performance across different datasets\n\n")

        # Check if best performer is also most consistent
        if best_detector == most_consistent:
            f.write(f"3. **Winner**: {best_detector.upper()} dominates both performance AND consistency ✅\n\n")
        else:
            f.write(f"3. **Trade-off**: Best performance ({best_detector}) vs best consistency ({most_consistent})\n\n")

        # Generalization insights
        best_gap_detector = min(detector_stats.items(), key=lambda x: x[1]["mean_gap"])[0]
        f.write(f"4. **Best Generalization**: {best_gap_detector.upper()} ")
        f.write(f"(avg gap={detector_stats[best_gap_detector]['mean_gap']:.4f})\n")
        f.write(f"   - Smallest average gap between intra-fold and cross-fold scores\n\n")

        f.write("---\n\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("### When to Use Each Detector\n\n")

        for detector, stats in sorted_detectors:
            f.write(f"**{detector.upper()}**:\n")
            if stats['mean_cross'] > 0.4:
                f.write(f"- ✅ **Recommended**: Excellent average performance (F3={stats['mean_cross']:.4f})\n")
            elif stats['mean_cross'] > 0.3:
                f.write(f"- ⚠️  Good option: Solid performance (F3={stats['mean_cross']:.4f})\n")
            else:
                f.write(f"- 🔻 Consider alternatives: Lower performance (F3={stats['mean_cross']:.4f})\n")

            if stats['cv_cross'] < 25:
                f.write(f"- ✅ Consistent across datasets (CV={stats['cv_cross']:.1f}%)\n")
            else:
                f.write(f"- ⚠️  Variable across datasets (CV={stats['cv_cross']:.1f}%)\n")

            f.write(f"- Best use case: {stats['datasets'][stats['cross_fold_scores'].index(stats['max_cross'])]}\n\n")

        f.write("---\n\n")

        # Methodology note
        f.write("## Methodology Notes\n\n")
        f.write("1. **Cross-Fold F3**: Performance on opposite fold from 2-fold cross-validation\n")
        f.write("2. **Independent Tuning**: Each detector was optimized separately per dataset\n")
        f.write("3. **No Parameter Transfer**: This analysis does NOT test portability\n")
        f.write("4. **Represents Ceiling**: Shows best achievable with proper tuning\n\n")

        f.write("**Next Steps**: See Option 2 analysis for parameter portability testing.\n\n")

    print(f"✅ Cross-dataset generalization report (Option 1): {output_path}")

    # Export CSV
    csv_path = output_dir / "cross_dataset_generalization_option1.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["detector", "mean_cross_fold_f3", "median_cross_fold_f3", "std_dev",
                       "min", "max", "cv_percent", "avg_gap"]
        )
        writer.writeheader()

        for detector, stats in sorted(detector_stats.items()):
            writer.writerow({
                "detector": detector,
                "mean_cross_fold_f3": round(stats["mean_cross"], 4),
                "median_cross_fold_f3": round(stats["median_cross"], 4),
                "std_dev": round(stats["std_cross"], 4),
                "min": round(stats["min_cross"], 4),
                "max": round(stats["max_cross"], 4),
                "cv_percent": round(stats["cv_cross"], 2),
                "avg_gap": round(stats["mean_gap"], 4)
            })

    print(f"✅ CSV exported: {csv_path}")


def main():
    """Main execution."""
    print("\n" + "="*100)
    print("TWO-FOLD CROSS-VALIDATION AGGREGATION")
    print("="*100)

    # Process all reports
    print("\n🔍 Processing two-fold reports...")
    aggregated = process_all_twofold_reports()

    # Display summaries
    generate_robustness_table(aggregated)
    generate_dataset_comparison_table(aggregated)
    generate_generalization_gap_analysis(aggregated)

    # Export results
    print("\n" + "="*100)
    print("EXPORTING RESULTS")
    print("="*100)
    export_csv_results(aggregated)
    generate_summary_report(aggregated)

    # Generate Option 1 analysis
    print("\n" + "="*100)
    print("OPTION 1: CROSS-DATASET GENERALIZATION ANALYSIS")
    print("="*100)
    generate_cross_dataset_generalization_report(aggregated)

    print("\n✅ Two-fold analysis complete!")


if __name__ == "__main__":
    main()
