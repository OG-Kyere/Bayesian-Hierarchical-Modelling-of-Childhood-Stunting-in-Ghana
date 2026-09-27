"""Regenerate compact public Bayesian SVG figures from locked aggregate tables.

No DHS microdata are read and no model is refitted. The figures are derived
only from version-controlled aggregate result tables.
"""
from __future__ import annotations
from html import escape
from math import log
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)
STYLE = '<style>text{font-family:Arial,sans-serif;fill:#222}.t{font-size:20px;font-weight:700}.l{font-size:12px}.v{font-size:11px}</style>'


def svg_text(x, y, value, cls="l"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}">{escape(str(value))}</text>'


def forest_plot():
    labels = {
        "male": "Male vs female",
        "age_24-35": "Age 24–35 vs 0–5 months",
        "wealth_richest": "Richest vs poorest",
        "rural": "Rural vs urban",
        "water_unimproved": "Unimproved water source",
        "sanitation_unimproved": "Unimproved/no sanitation",
        "maternal_education_primary": "Maternal primary vs none",
        "maternal_education_secondary": "Maternal secondary vs none",
        "maternal_education_higher": "Maternal higher vs none",
    }
    order = list(labels)
    d = pd.read_csv(TABLES / "model3_final_8chain_key_or.csv").set_index("term").loc[order]
    x0, x1, xmin, xmax = 320, 720, 0.15, 5.0

    def xpos(v):
        return x0 + (log(float(v)) - log(xmin)) / (log(xmax) - log(xmin)) * (x1 - x0)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="470" viewBox="0 0 900 470">{STYLE}',
        svg_text(20, 28, "Model 3 posterior odds ratios with 95% posterior intervals", "t"),
    ]
    ref = xpos(1.0)
    parts.append(f'<line x1="{ref:.1f}" y1="42" x2="{ref:.1f}" y2="420" stroke="#777" stroke-dasharray="5 4"/>')

    for i, term in enumerate(order):
        row = d.loc[term]
        y = 58 + i * 42
        med, lo, hi = float(row["median"]), float(row["q2_5"]), float(row["q97_5"])
        xl, xm, xu = xpos(lo), xpos(med), xpos(hi)
        parts += [
            svg_text(20, y + 4, labels[term]),
            f'<line x1="{xl:.1f}" y1="{y}" x2="{xu:.1f}" y2="{y}" stroke="#222" stroke-width="1.5"/>',
            f'<line x1="{xl:.1f}" y1="{y-5}" x2="{xl:.1f}" y2="{y+5}" stroke="#222"/>',
            f'<line x1="{xu:.1f}" y1="{y-5}" x2="{xu:.1f}" y2="{y+5}" stroke="#222"/>',
            f'<circle cx="{xm:.1f}" cy="{y}" r="4"/>',
            svg_text(735, y + 4, f"{med:.2f} ({lo:.2f}–{hi:.2f})", "v"),
        ]
    parts += [svg_text(320, 455, "Odds ratio (log scale); reference line = 1"), "</svg>"]
    (FIGURES / "model3_posterior_or_forest.svg").write_text("".join(parts), encoding="utf-8")


def variance_row(filename, label):
    d = pd.read_csv(TABLES / filename).set_index("quantity")
    row = {"model": label}
    for level, key in [("community", "tau_community"), ("household", "tau_household")]:
        row[f"{level}_median"] = float(d.loc[key, "median"])
        row[f"{level}_lo"] = float(d.loc[key, "q2_5"])
        row[f"{level}_hi"] = float(d.loc[key, "q97_5"])
    return row


def variance_plot():
    rows = [
        variance_row("model1_variance_summary.csv", "Model 1"),
        variance_row("model2_variance_summary.csv", "Model 2 full"),
        variance_row("model2_harm_variance_summary.csv", "Model 2 harmonized"),
        variance_row("model3_final_8chain_variance_summary.csv", "Model 3"),
    ]
    x0, x1, xmax = 230, 760, 1.7

    def xpos(v):
        return x0 + float(v) / xmax * (x1 - x0)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390" viewBox="0 0 900 390">{STYLE}',
        svg_text(20, 28, "Household and community heterogeneity across models", "t"),
    ]
    for i, row in enumerate(rows):
        base = 78 + i * 72
        parts.append(svg_text(20, base + 3, row["model"]))
        for j, (prefix, label) in enumerate([("community", "Community SD"), ("household", "Household SD")]):
            y = base - 12 + j * 30
            med, lo, hi = row[f"{prefix}_median"], row[f"{prefix}_lo"], row[f"{prefix}_hi"]
            xl, xm, xu = xpos(lo), xpos(med), xpos(hi)
            parts += [
                svg_text(145, y + 4, label, "v"),
                f'<line x1="{xl:.1f}" y1="{y}" x2="{xu:.1f}" y2="{y}" stroke="#222" stroke-width="1.5"/>',
                f'<line x1="{xl:.1f}" y1="{y-5}" x2="{xl:.1f}" y2="{y+5}" stroke="#222"/>',
                f'<line x1="{xu:.1f}" y1="{y-5}" x2="{xu:.1f}" y2="{y+5}" stroke="#222"/>',
                f'<circle cx="{xm:.1f}" cy="{y}" r="4"/>',
                svg_text(775, y + 4, f"{med:.2f}", "v"),
            ]
    parts += [svg_text(230, 378, "Latent-scale random-effect standard deviation; lines show 95% posterior intervals."), "</svg>"]
    (FIGURES / "model_variance_comparison.svg").write_text("".join(parts), encoding="utf-8")


def ppc_plot():
    d = pd.read_csv(TABLES / "model3_ppc_summary.csv")
    x0, x1, maxv = 160, 790, 32.0

    def xpos(v):
        return x0 + (100 * float(v)) / maxv * (x1 - x0)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="410" viewBox="0 0 900 410">{STYLE}',
        svg_text(20, 28, "Model 3 posterior predictive check", "t"),
    ]
    for i, row in d.iterrows():
        y = 58 + i * 43
        xl, xm, xu = xpos(row["rep_l95"]), xpos(row["rep_mean"]), xpos(row["rep_u95"])
        xo = xpos(row["observed"])
        parts += [
            svg_text(20, y + 4, row["group"]),
            f'<line x1="{xl:.1f}" y1="{y}" x2="{xu:.1f}" y2="{y}" stroke="#222" stroke-width="2"/>',
            f'<circle cx="{xm:.1f}" cy="{y}" r="4"/>',
            f'<line x1="{xo-4:.1f}" y1="{y-4}" x2="{xo+4:.1f}" y2="{y+4}" stroke="#555" stroke-width="2"/>',
            f'<line x1="{xo-4:.1f}" y1="{y+4}" x2="{xo+4:.1f}" y2="{y-4}" stroke="#555" stroke-width="2"/>',
            svg_text(800, y + 4, f'obs {100 * float(row["observed"]):.1f}%', "v"),
        ]
    parts += [svg_text(160, 386, "Circle: replicated mean and 95% predictive interval; ×: observed prevalence", "v"), "</svg>"]
    (FIGURES / "model3_ppc_age.svg").write_text("".join(parts), encoding="utf-8")


def main():
    forest_plot()
    variance_plot()
    ppc_plot()
    print("Regenerated compact Bayesian SVG figures from aggregate tables.")


if __name__ == "__main__":
    main()
