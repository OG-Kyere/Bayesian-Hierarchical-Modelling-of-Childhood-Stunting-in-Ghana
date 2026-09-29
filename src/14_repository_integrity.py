"""Repository integrity checks that do not require DHS microdata."""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "thesis/references.bib"
BLINDED = ROOT / "manuscript/targets/mcn/main_blinded.tex"
TMIH = ROOT / "manuscript/targets/tmih/main.tex"
TMIH_SUPP = ROOT / "manuscript/targets/tmih/supplement.tex"
GENERIC = ROOT / "manuscript/main.tex"
GENERIC_SUPP = ROOT / "manuscript/supplement.tex"
CONFIG = ROOT / "thesis/config.tex"
CITATION = ROOT / "CITATION.cff"

RAW_SUFFIXES = {
    ".dta", ".sav", ".sas7bdat", ".por", ".zip", ".nc", ".pkl", ".pickle", ".joblib"
}
FIGURE_SUFFIXES = [".svg", ".png", ".pdf", ".jpg", ".jpeg"]

BLINDED_FORBIDDEN = [
    "Gideon Ofosu Kyere",
    "Kyere Ofosu Gideon",
    "OG-Kyere",
    "[INSERT",
    "INSERT AFFILIATION",
    "INSERT EMAIL",
]

ACTIVE_PLACEHOLDERS = [
    "[INSERT",
    "[FINAL",
    "CONFIRM BEFORE SUBMISSION",
    "Not yet available",
]


def tex_files() -> list[Path]:
    paths: list[Path] = []
    for base in [ROOT / "thesis", ROOT / "manuscript"]:
        if base.exists():
            paths.extend(base.rglob("*.tex"))
    return sorted(set(paths))


def bib_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)


def citation_keys(text: str) -> list[str]:
    keys: list[str] = []
    for match in re.finditer(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}", text):
        keys.extend(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def figure_refs(text: str) -> list[str]:
    refs: list[str] = []
    for pattern in [
        r"\\includesvg(?:\[[^\]]*\])?\{([^}]+)\}",
        r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
    ]:
        refs.extend(re.findall(pattern, text))
    return refs


def figure_exists(tex: Path, ref: str) -> bool:
    ref_path = Path(ref)
    candidates: list[Path] = []
    if ref_path.suffix:
        candidates.extend([tex.parent / ref_path, ROOT / ref_path, ROOT / "results/figures" / ref_path.name])
    else:
        for suffix in FIGURE_SUFFIXES:
            candidates.extend([
                tex.parent / ref_path.with_suffix(suffix),
                ROOT / ref_path.with_suffix(suffix),
                ROOT / "results/figures" / (ref_path.name + suffix),
            ])
    return any(candidate.exists() for candidate in candidates)


def main() -> int:
    failures: list[str] = []

    bib_text = BIB.read_text(encoding="utf-8")
    keys = bib_keys(bib_text)
    counts = Counter(keys)
    for key, count in counts.items():
        if count > 1:
            failures.append(f"duplicate BibTeX key: {key}")
    available = set(keys)

    for tex in tex_files():
        text = tex.read_text(encoding="utf-8")
        for key in citation_keys(text):
            if key not in available:
                failures.append(f"{tex.relative_to(ROOT)}: missing citation key '{key}'")
        for ref in figure_refs(text):
            if not figure_exists(tex, ref):
                failures.append(f"{tex.relative_to(ROOT)}: referenced figure not found: '{ref}'")

    try:
        tracked = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
        ).stdout.decode("utf-8").split("\0")
    except (subprocess.CalledProcessError, FileNotFoundError, UnicodeDecodeError) as exc:
        failures.append(f"could not inspect Git-tracked files: {exc}")
        tracked = []

    for rel_text in tracked:
        if not rel_text:
            continue
        rel = Path(rel_text)
        if rel.suffix.lower() in RAW_SUFFIXES:
            failures.append(f"restricted/large data-like file is tracked: {rel}")
        if len(rel.parts) >= 2 and rel.parts[0] == "data" and rel.parts[1] == "raw":
            failures.append(f"file is tracked under data/raw: {rel}")

    blinded_text = BLINDED.read_text(encoding="utf-8")
    for token in BLINDED_FORBIDDEN:
        if token.lower() in blinded_text.lower():
            failures.append(f"blinded manuscript contains forbidden text: '{token}'")
    if not re.search(r"\\author\{\s*\}", blinded_text):
        failures.append("blinded manuscript does not have an empty \\author{} field")

    tmih_text = TMIH.read_text(encoding="utf-8")
    canonical_affiliation = "Kwame Nkrumah University of Science and Technology, Kumasi-Ghana"
    if canonical_affiliation not in tmih_text:
        failures.append("active TMIH manuscript is missing the canonical KNUST affiliation")
    if "Independent Researcher, Ghana" in tmih_text:
        failures.append("active TMIH manuscript contains the superseded independent-researcher affiliation")
    if "Maternal & Child Nutrition".lower() in tmih_text.lower():
        failures.append("active TMIH manuscript contains stale target text: 'Maternal & Child Nutrition'")

    tmih_required = [
        "community was operationalized as the DHS survey cluster",
        "household-versus-community contrast remained clearly apparent",
        "commonly used 1.01 guideline",
    ]
    for token in tmih_required:
        if token.lower() not in tmih_text.lower():
            failures.append(f"active TMIH manuscript is missing required clarification: '{token}'")

    for stale in [
        "became, if anything, more apparent",
        "author list and contribution statement should be revisited",
        "Editorial Information (for submission only)",
    ]:
        if stale.lower() in tmih_text.lower():
            failures.append(f"active TMIH manuscript contains stale editorial wording: '{stale}'")

    tmih_supp_text = TMIH_SUPP.read_text(encoding="utf-8")
    generic_supp_text = GENERIC_SUPP.read_text(encoding="utf-8")
    for required in [
        "Lower 95\\% CI",
        "Upper 95\\% CI",
        "Model 2 harmonized",
        "commonly used 1.01 guideline",
    ]:
        if required.lower() not in tmih_supp_text.lower():
            failures.append(f"TMIH supplement is missing required clarification: '{required}'")
    for required in [
        "Model 2 harmonized (same 4,503-child sample as Model 3)",
        "commonly used 1.01 guideline",
        "4,503-child complete-case Model 3 sample",
        "distinct from the survey-weighted prevalence",
    ]:
        if required.lower() not in generic_supp_text.lower():
            failures.append(f"generic supplement is missing required clarification: '{required}'")

    gee_start = tmih_supp_text.lower().find("selected independent gee robustness checks")
    if gee_start >= 0:
        gee_block = tmih_supp_text[gee_start:gee_start + 1200]
        if "2.5th percentile" in gee_block or "97.5th percentile" in gee_block:
            failures.append("TMIH GEE table incorrectly labels frequentist confidence limits as posterior percentiles")

    for path in [TMIH, TMIH_SUPP, GENERIC, GENERIC_SUPP, CONFIG, CITATION]:
        text = path.read_text(encoding="utf-8")
        if "Kyere Ofosu Gideon" in text:
            failures.append(f"{path.relative_to(ROOT)}: stale author-name order")
        for token in ACTIVE_PLACEHOLDERS:
            if token.lower() in text.lower():
                failures.append(f"{path.relative_to(ROOT)}: unresolved active placeholder '{token}'")

    if "Gideon Ofosu Kyere" not in GENERIC.read_text(encoding="utf-8"):
        failures.append("generic manuscript is missing confirmed author name")
    if "Gideon Ofosu Kyere" not in CONFIG.read_text(encoding="utf-8"):
        failures.append("thesis config is missing confirmed author name")

    canonical_affiliation = "Kwame Nkrumah University of Science and Technology, Kumasi-Ghana"
    for path in [TMIH, TMIH_SUPP, GENERIC, GENERIC_SUPP, CONFIG]:
        if canonical_affiliation not in path.read_text(encoding="utf-8"):
            failures.append(f"{path.relative_to(ROOT)}: canonical KNUST affiliation is missing")

    citation_text = CITATION.read_text(encoding="utf-8")
    if 'given-names: "Gideon Ofosu"' not in citation_text:
        failures.append("CITATION.cff: given-names are not standardized")
    if "0009-0003-9848-8437" not in citation_text:
        failures.append("CITATION.cff: ORCID is missing")

    if failures:
        print("Repository integrity check FAILED:\n")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Repository integrity check passed.")
    print(f"- BibTeX entries: {len(keys)}")
    print(f"- LaTeX files checked: {len(tex_files())}")
    print("- citation keys: complete")
    print("- duplicate BibTeX keys: none")
    print("- referenced figures: present")
    print("- tracked restricted/raw data files: none")
    print("- blinded manuscript identity check: passed")
    print("- active manuscript/report metadata: synchronized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
