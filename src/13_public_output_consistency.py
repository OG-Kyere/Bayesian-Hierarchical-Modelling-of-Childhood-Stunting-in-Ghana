"""Check public prose, summary tables, and figures against locked aggregate results.

This script uses only the Python standard library. It does not require DHS
microdata or the Bayesian modelling environment.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"

KEY_OR = TABLES / "model3_final_8chain_key_or.csv"
VAR = TABLES / "model3_final_8chain_variance_summary.csv"
LOO = TABLES / "loo_model_compare_final.csv"
DESC = TABLES / "descriptive_all.csv"

PUBLIC_TEXT = [
    ROOT / "README.md",
    ROOT / "manuscript/main.tex",
    ROOT / "manuscript/targets/mcn/main_blinded.tex",
    ROOT / "manuscript/targets/tmih/main.tex",
]
LONG_FORM_TEXT = [
    ROOT / "thesis/frontmatter/abstract.tex",
    ROOT / "thesis/chapter4_results.tex",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize(text: str) -> str:
    text = text.replace("--", "–").replace("—", "–")
    text = text.replace("\\%", "%")
    text = re.sub(r"\\[A-Za-z]+\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)
    return " ".join(text.split())


def rounded(value: str | float, digits: int = 2) -> str:
    return f"{float(value):.{digits}f}"


def interval(row: dict[str, str]) -> str:
    return f"{rounded(row['q2_5'])}–{rounded(row['q97_5'])}"


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise AssertionError(f"Could not find {key}={value}")


def expect_in(text: str, fragment: str, label: str, failures: list[str]) -> None:
    if normalize(fragment) not in normalize(text):
        failures.append(f"{label}: missing '{fragment}'")


def close(a: str | float, b: str | float, tol: float = 5e-6) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)
    except (TypeError, ValueError):
        return False


def compare_or_summary(locked: list[dict[str, str]], failures: list[str]) -> None:
    public = read_csv(TABLES / "key_posterior_odds_ratios.csv")
    mapping = {
        "male": "Male vs female",
        "age_24-35": "Age 24-35 vs 0-5",
        "wealth_richest": "Richest vs poorest",
        "rural": "Rural vs urban",
        "water_unimproved": "Unimproved water",
        "sanitation_unimproved": "Unimproved/no sanitation",
        "maternal_education_primary": "Primary vs no maternal education",
        "maternal_education_secondary": "Secondary vs no maternal education",
        "maternal_education_higher": "Higher vs no maternal education",
    }
    for term, label in mapping.items():
        src = find_row(locked, "term", term)
        matches = [r for r in public if r["model"] == "Model 3" and r["term"] == label]
        if len(matches) != 1:
            failures.append(f"key_posterior_odds_ratios.csv: expected one Model 3 row for {label}")
            continue
        dst = matches[0]
        for a, b, field in [
            (dst["median_or"], src["median"], "median"),
            (dst["ci95_lower"], src["q2_5"], "lower"),
            (dst["ci95_upper"], src["q97_5"], "upper"),
        ]:
            if not close(a, b):
                failures.append(f"key_posterior_odds_ratios.csv: {label} {field} is stale")


def compare_variance_summary(locked: list[dict[str, str]], failures: list[str]) -> None:
    public = read_csv(TABLES / "model_comparison_variance.csv")
    m3 = find_row(public, "model", "Model 3")
    checks = {
        "tau_community_median": ("tau_community", "median"),
        "tau_community_l95": ("tau_community", "q2_5"),
        "tau_community_u95": ("tau_community", "q97_5"),
        "tau_household_median": ("tau_household", "median"),
        "tau_household_l95": ("tau_household", "q2_5"),
        "tau_household_u95": ("tau_household", "q97_5"),
        "icc_community_median": ("icc_community", "median"),
        "vpc_household_median": ("vpc_household", "median"),
        "icc_same_household_median": ("icc_same_household", "median"),
        "mor_community_median": ("mor_community", "median"),
        "mor_household_median": ("mor_household", "median"),
    }
    for public_field, (quantity, locked_field) in checks.items():
        src = find_row(locked, "quantity", quantity)
        if not close(m3[public_field], src[locked_field]):
            failures.append(f"model_comparison_variance.csv: Model 3 {public_field} is stale")


def compare_sensitivity_comparators(locked: list[dict[str, str]], failures: list[str]) -> None:
    by_term = {r["term"]: r for r in locked}

    prior = read_csv(TABLES / "prior_sensitivity_key_effects.csv")
    for row in prior:
        if row["prior"] != "primary" or row["term"] not in by_term:
            continue
        src = by_term[row["term"]]
        for field, locked_field in [("median_or", "median"), ("l95", "q2_5"), ("u95", "q97_5")]:
            if not close(row[field], src[locked_field]):
                failures.append(f"prior_sensitivity_key_effects.csv: primary {row['term']} {field} is stale")

    weighted = read_csv(TABLES / "survey_weight_sensitivity_key_effects.csv")
    for row in weighted:
        if row["term"] not in by_term:
            continue
        src = by_term[row["term"]]
        for field, locked_field in [
            ("primary_median_or", "median"),
            ("primary_l95", "q2_5"),
            ("primary_u95", "q97_5"),
        ]:
            if not close(row[field], src[locked_field]):
                failures.append(f"survey_weight_sensitivity_key_effects.csv: primary {row['term']} {field} is stale")


def check_figures(locked: list[dict[str, str]], failures: list[str]) -> None:
    forest = (FIGURES / "model3_posterior_or_forest.svg").read_text(encoding="utf-8")
    for term in [
        "male", "age_24-35", "wealth_richest", "rural", "water_unimproved",
        "sanitation_unimproved", "maternal_education_primary",
        "maternal_education_secondary", "maternal_education_higher",
    ]:
        row = find_row(locked, "term", term)
        expected = f"{rounded(row['median'])} ({rounded(row['q2_5'])}–{rounded(row['q97_5'])})"
        if expected not in forest:
            failures.append(f"model3_posterior_or_forest.svg: missing locked label {expected}")

    stale_forest = [
        "2.98 (2.00–4.35)",
        "1.50 (1.14–2.00)",
        "0.38 (0.19–0.70)",
        "95% credible intervals",
    ]
    for value in stale_forest:
        if value in forest:
            failures.append(f"model3_posterior_or_forest.svg: stale content '{value}'")

    variance = (FIGURES / "model_variance_comparison.svg").read_text(encoding="utf-8")
    if ">0.41<" in variance:
        failures.append("model_variance_comparison.svg: stale Model 3 community SD label 0.41")
    for expected in [">0.39<", ">1.23<", "95% posterior intervals"]:
        if expected not in variance:
            failures.append(f"model_variance_comparison.svg: missing '{expected}'")


def main() -> int:
    key = read_csv(KEY_OR)
    var = read_csv(VAR)
    loo = read_csv(LOO)[0]
    desc = read_csv(DESC)
    failures: list[str] = []

    male = find_row(key, "term", "male")
    age = find_row(key, "term", "age_24-35")
    wealth = find_row(key, "term", "wealth_richest")
    water = find_row(key, "term", "water_unimproved")
    sanitation = find_row(key, "term", "sanitation_unimproved")
    higher = find_row(key, "term", "maternal_education_higher")

    community_sd = find_row(var, "quantity", "tau_community")
    household_sd = find_row(var, "quantity", "tau_household")
    community_icc = find_row(var, "quantity", "icc_community")
    household_vpc = find_row(var, "quantity", "vpc_household")
    community_mor = find_row(var, "quantity", "mor_community")
    household_mor = find_row(var, "quantity", "mor_household")

    overall = next(r for r in desc if r["variable"] == "overall" and r["category"] == "All")

    expected_common = {
        "male OR": [rounded(male["median"]), interval(male)],
        "age 24–35 OR": [rounded(age["median"]), interval(age)],
        "richest OR": [rounded(wealth["median"]), interval(wealth)],
        "water OR": [rounded(water["median"]), interval(water)],
        "sanitation OR": [rounded(sanitation["median"]), interval(sanitation)],
        "higher education OR": [rounded(higher["median"]), interval(higher)],
        "household SD": [rounded(household_sd["median"])],
        "community SD": [rounded(community_sd["median"])],
        "household VPC": [rounded(household_vpc["median"])],
        "community ICC": [rounded(community_icc["median"])],
        "household MOR": [rounded(household_mor["median"])],
        "community MOR": [rounded(community_mor["median"])],
    }

    for path in PUBLIC_TEXT:
        text = path.read_text(encoding="utf-8")
        for label, fragments in expected_common.items():
            for fragment in fragments:
                expect_in(text, fragment, f"{path}: {label}", failures)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    prevalence = f"{100 * float(overall['weighted_prevalence']):.2f}%"
    expect_in(readme, prevalence, "README weighted prevalence", failures)
    expect_in(readme, overall["n_unweighted"], "README sample size", failures)
    expect_in(readme, overall["stunted_unweighted"], "README stunted count", failures)

    delta = f"{float(loo['delta_model3_minus_model2']):.2f}"
    se_delta = f"{float(loo['se_delta']):.2f}"
    for target in [
        ROOT / "manuscript/targets/mcn/main_blinded.tex",
        ROOT / "manuscript/targets/tmih/main.tex",
        ROOT / "thesis/chapter4_results.tex",
        ROOT / "thesis/chapter5_discussion_conclusion.tex",
    ]:
        target_text = target.read_text(encoding="utf-8")
        expect_in(target_text, delta, f"{target}: LOO ELPD difference", failures)
        expect_in(target_text, se_delta, f"{target}: LOO SE", failures)

    long_form_expected = {
        "male OR": [rounded(male["median"]), interval(male)],
        "age 24–35 OR": [rounded(age["median"]), interval(age)],
        "water OR": [rounded(water["median"]), interval(water)],
        "sanitation OR": [rounded(sanitation["median"]), interval(sanitation)],
        "higher education OR": [rounded(higher["median"]), interval(higher)],
        "household SD": [rounded(household_sd["median"])],
        "community SD": [rounded(community_sd["median"])],
        "household VPC": [rounded(household_vpc["median"])],
        "community ICC": [rounded(community_icc["median"])],
    }
    for path in LONG_FORM_TEXT:
        text = path.read_text(encoding="utf-8")
        for label, fragments in long_form_expected.items():
            for fragment in fragments:
                expect_in(text, fragment, f"{path}: {label}", failures)

    stale = ["1.14–2.00", "0.38 (0.19–0.70)", "WAIC difference was negligible"]
    for path in PUBLIC_TEXT + LONG_FORM_TEXT + [ROOT / "thesis/chapter5_discussion_conclusion.tex"]:
        text = normalize(path.read_text(encoding="utf-8"))
        for old in stale:
            if normalize(old) in text:
                failures.append(f"{path}: stale value/wording found: '{old}'")

    compare_or_summary(key, failures)
    compare_variance_summary(var, failures)
    compare_sensitivity_comparators(key, failures)
    check_figures(key, failures)

    if failures:
        print("Public-output consistency check FAILED:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Public-output consistency check passed.")
    print(f"- weighted prevalence: {prevalence}")
    print(f"- male OR: {rounded(male['median'])} ({interval(male)})")
    print(f"- water OR: {rounded(water['median'])} ({interval(water)})")
    print(f"- household SD: {rounded(household_sd['median'])}")
    print(f"- community SD: {rounded(community_sd['median'])}")
    print(f"- LOO delta: {delta} (SE {se_delta})")
    print("- public summary CSVs: synchronized")
    print("- public Bayesian SVGs: synchronized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
