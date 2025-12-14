#!/usr/bin/env python3
"""
Create a single visualization combining Options 1, 2, and 3:
- x-axis: Option 1 ceiling F3 (mean cross-fold F3)
- y-axis: Option 2 average transferability ratio
- color: Option 3 unified robustness score
- size: Option 3 unified robustness score (scaled)

Outputs PNG to results/cross_dataset_analysis/option123_summary.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# Ensure readable fonts
mpl.rcParams.update({
    "figure.dpi": 120,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
})

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results" / "cross_dataset_analysis"


def load_option1() -> pd.DataFrame:
    path = RESULTS_DIR / "cross_dataset_generalization_option1.csv"
    df = pd.read_csv(path)
    return df.set_index("detector")[["mean_cross_fold_f3"]]


def load_option2() -> pd.DataFrame:
    path = RESULTS_DIR / "parameter_portability_option2.csv"
    df = pd.read_csv(path)
    grouped = df.groupby("detector")["transferability_ratio"].agg(["mean", "min", "max", "count"])
    grouped = grouped.rename(columns={"mean": "avg_transferability"})
    return grouped


def load_option3() -> pd.DataFrame:
    path = RESULTS_DIR / "unified_robustness_option3.csv"
    df = pd.read_csv(path)
    return df.set_index("detector")[["unified_score"]]


def build_merged() -> pd.DataFrame:
    opt1 = load_option1()
    opt2 = load_option2()
    opt3 = load_option3()
    merged = opt1.join(opt2, how="inner").join(opt3, how="inner")
    merged = merged.reset_index()
    merged = merged.rename(columns={"mean_cross_fold_f3": "ceiling_f3"})
    return merged


def plot_option123(df: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))

    sizes = 400 * df["unified_score"]  # scale sizes for visibility
    scatter = ax.scatter(
        df["ceiling_f3"],
        df["avg_transferability"],
        c=df["unified_score"],
        s=sizes,
        cmap="viridis",
        alpha=0.85,
        edgecolor="black",
        linewidth=0.8,
    )

    for _, row in df.iterrows():
        ax.text(
            row["ceiling_f3"] + 0.005,
            row["avg_transferability"] + 0.005,
            row["detector"],
            fontsize=9,
            weight="bold",
        )

    ax.set_xlabel("Ceiling performance (Option 1) - mean cross-fold F3")
    ax.set_ylabel("Portability (Option 2) - avg transferability ratio")
    ax.set_title("Unified View: Performance vs Portability vs Robustness (Option 3)")
    ax.grid(True, linestyle="--", alpha=0.4)

    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Unified robustness score (Option 3)")

    ax.set_xlim(0.12, 0.46)
    ax.set_ylim(0.45, 1.02)

    ax.axhline(0.95, color="green", linestyle=":", alpha=0.6, label="95% transferability")
    ax.axvline(0.35, color="orange", linestyle=":", alpha=0.6, label="High ceiling threshold")
    ax.legend(loc="lower right")

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def main() -> None:
    df = build_merged()
    output = RESULTS_DIR / "option123_summary.png"
    plot_option123(df, output)
    print(f"✅ Visualization saved to: {output}")


if __name__ == "__main__":
    main()
