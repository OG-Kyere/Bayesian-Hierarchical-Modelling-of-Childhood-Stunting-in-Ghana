"""Regenerate the public Bayesian figures from version-controlled aggregate tables.

This script does not access DHS microdata and does not refit any model. Its
purpose is to keep the public SVG figures synchronized with the locked result
tables used by the thesis and manuscript.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

TERM_LABELS = {
    "male": "Male vs female",
    "age_24-35": "Age 24-35 vs 0-5 months",
    "wealth_richest": "Richest vs poorest",
    "rural": "Rural vs urban",
    "water_unimproved": "Unimproved water source",
    "sanitation_unimproved": "Unimproved/no sanitation",
    "maternal_education_primary": "Maternal primary vs none",
    "maternal_education_secondary": "Maternal secondary vs none",
    "maternal_education_higher": "Maternal higher vs none",
}
TERM_ORDER = list(TERM_LABELS)


def forest_plot() -> None:
    d = pd.read_csv(TABLES / "model3_final_8chain_key_or.csv").set_index("term")
    d = d.loc[TERM_ORDER].reset_index()

    y = np.arange(len(d))[::-1]
    med = d["median"].to_numpy(float)
    lo = d["q2_5"].to_numpy(float)
    hi = d["q97_5"].to_numpy(float)

    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    ax.errorbar(
        med,
        y,
        xerr=np.vstack([med - lo, hi - med]),
        fmt="o",
        capsize=3,
    )
    ax.axvline(1.0, linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yticks(y, [TERM_LABELS[t] for t in d["term"]])
    ax.set_xlabel("Odds ratio (log scale)")
    ax.set_title("Model 3 posterior odds ratios with 95% posterior intervals")

    for x, yy, lower, upper in zip(med, y, lo, hi):
        ax.text(
            upper * 1.04,
            yy,
            f"{x:.2f} ({lower:.2f}-{upper:.2f})",
            va="center",
            fontsize=8,
        )
    fig.tight_layout()
    fig.savefig(FIGURES / "model3_posterior_or_forest.svg", format="svg")
    plt.close(fig)


def _variance_row(path: str, label: str) -> dict[str, float | str]:
    d = pd.read_csv(TABLES / path).set_index("quantity")
    row: dict[str, float | str] = {"model": label}
    for level, key in [("community", "tau_community"), ("household", "tau_household")]:
        row[f"{level}_median"] = float(d.loc[key, "median"])
        row[f"{level}_lo"] = float(d.loc[key, "q2_5"])
        row[f"{level}_hi"] = float(d.loc[key, "q97_5"])
    return row


def variance_plot() -> None:
    rows = [
        _variance_row("model1_variance_summary.csv", "Model 1"),
        _variance_row("model2_variance_summary.csv", "Model 2 full"),
        _variance_row("model2_harm_variance_summary.csv", "Model 2 harmonized"),
        _variance_row("model3_final_8chain_variance_summary.csv", "Model 3"),
    ]
    d = pd.DataFrame(rows)
    y = np.arange(len(d))[::-1]

    fig, ax = plt.subplots(figsize=(8.7, 5.3))
    offset = 0.15
    for label, prefix, shift in [
        ("Community SD", "community", offset),
        ("Household SD", "household", -offset),
    ]:
        med = d[f"{prefix}_median"].to_numpy(float)
        lo = d[f"{prefix}_lo"].to_numpy(float)
        hi = d[f"{prefix}_hi"].to_numpy(float)
        ax.errorbar(
            med,
            y + shift,
            xerr=np.vstack([med - lo, hi - med]),
            fmt="o",
            capsize=3,
            label=label,
        )

    ax.set_yticks(y, d["model"])
    ax.set_xlabel("Latent-scale random-effect standard deviation")
    ax.set_title("Household and community heterogeneity across models")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "model_variance_comparison.svg", format="svg")
    plt.close(fig)


def ppc_plot() -> None:
    d = pd.read_csv(TABLES / "model3_ppc_summary.csv")
    y = np.arange(len(d))[::-1]
    rep = 100 * d["rep_mean"].to_numpy(float)
    lo = 100 * d["rep_l95"].to_numpy(float)
    hi = 100 * d["rep_u95"].to_numpy(float)
    obs = 100 * d["observed"].to_numpy(float)

    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    ax.errorbar(
        rep,
        y,
        xerr=np.vstack([rep - lo, hi - rep]),
        fmt="o",
        capsize=3,
        label="Posterior predictive",
    )
    ax.scatter(obs, y, marker="x", label="Observed")
    ax.set_yticks(y, d["group"])
    ax.set_xlabel("Stunting prevalence (%)")
    ax.set_title("Model 3 posterior predictive check")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "model3_ppc_age.svg", format="svg")
    plt.close(fig)


def main() -> None:
    forest_plot()
    variance_plot()
    ppc_plot()
    print("Regenerated public Bayesian figures from aggregate tables.")


if __name__ == "__main__":
    main()
