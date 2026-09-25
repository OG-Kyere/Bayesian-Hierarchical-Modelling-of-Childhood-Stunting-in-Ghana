"""Check that public prose is synchronized with the saved aggregate results.

This script uses only the Python standard library so it can run on GitHub
without DHS microdata or the Bayesian modelling environment.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEY_OR = ROOT / "results/tables/model3_final_8chain_key_or.csv"
VAR = ROOT / "results/tables/model3_final_8chain_variance_summary.csv"
LOO = ROOT / "results/tables/loo_model_compare_final.csv"
DESC = ROOT / "results/tables/descriptive_all.csv"

PUBLIC_TEXT = [
    ROOT / "README.md",
    ROOT / "manuscript/main.tex",
    ROOT / "manuscript/targets/mcn/main_blinded.tex",  # archived target, kept consistent
    ROOT / "manuscript/targets/tmih/main.tex",        # active journal target
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


def rounded(x: str, digits: int = 2) -> str:
    return f"{float(x):.{digits}f}"


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


def main() -> int:
    key = read_csv(KEY_OR)
    var = read_csv(VAR)
    loo = read_csv(LOO)[0]
    desc = read_csv(DESC)

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

    overall = next(
        row for row in desc
        if row["variable"] == "overall" and row["category"] == "All"
    )

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

    failures: list[str] = []

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

    stale = [
        "1.14–2.00",
        "0.38 (0.19–0.70)",
        "WAIC difference was negligible",
    ]
    for path in PUBLIC_TEXT + LONG_FORM_TEXT + [ROOT / "thesis/chapter5_discussion_conclusion.tex"]:
        text = normalize(path.read_text(encoding="utf-8"))
        for old in stale:
            if normalize(old) in text:
                failures.append(f"{path}: stale value/wording found: '{old}'")

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
