"""Repository integrity checks that do not require DHS microdata.

Checks:
- every LaTeX citation key exists in thesis/references.bib;
- BibTeX keys are unique;
- figure files referenced by LaTeX exist;
- restricted/raw data formats are not committed;
- the blinded manuscript does not expose author identity or submission placeholders.

Only the Python standard library is required.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "thesis/references.bib"
BLINDED = ROOT / "manuscript/targets/mcn/main_blinded.tex"

RAW_SUFFIXES = {
    ".dta", ".sav", ".sas7bdat", ".por", ".zip", ".nc", ".pkl", ".pickle", ".joblib"
}

FIGURE_SUFFIXES = [".svg", ".png", ".pdf", ".jpg", ".jpeg"]

# Author/institution strings that must not appear in the double-blind manuscript.
BLINDED_FORBIDDEN = [
    "Kyere Ofosu Gideon",
    "OG-Kyere",
    "[INSERT",
    "INSERT AFFILIATION",
    "INSERT EMAIL",
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
    # Matches \cite{}, \citep{}, \citet{}, \citealp{}, etc.
    for match in re.finditer(r"\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*)*\{([^}]+)\}", text):
        keys.extend(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def figure_refs(text: str) -> list[str]:
    refs: list[str] = []
    patterns = [
        r"\\includesvg(?:\[[^\]]*\])?\{([^}]+)\}",
        r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
    ]
    for pattern in patterns:
        refs.extend(re.findall(pattern, text))
    return refs


def figure_exists(tex: Path, ref: str) -> bool:
    ref_path = Path(ref)
    candidates: list[Path] = []

    if ref_path.suffix:
        candidates.extend([
            tex.parent / ref_path,
            ROOT / ref_path,
            ROOT / "results/figures" / ref_path.name,
        ])
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

    # BibTeX uniqueness.
    bib_text = BIB.read_text(encoding="utf-8")
    keys = bib_keys(bib_text)
    counts = Counter(keys)
    duplicates = sorted(key for key, count in counts.items() if count > 1)
    for key in duplicates:
        failures.append(f"duplicate BibTeX key: {key}")

    available = set(keys)

    # Citation completeness and figure existence.
    for tex in tex_files():
        text = tex.read_text(encoding="utf-8")

        for key in citation_keys(text):
            if key not in available:
                failures.append(f"{tex.relative_to(ROOT)}: missing citation key '{key}'")

        for ref in figure_refs(text):
            if not figure_exists(tex, ref):
                failures.append(
                    f"{tex.relative_to(ROOT)}: referenced figure not found: '{ref}'"
                )

    # Restricted/raw file types must never be tracked in this repository.
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if path.suffix.lower() in RAW_SUFFIXES:
            failures.append(f"restricted/large data-like file is tracked: {rel}")
        if len(rel.parts) >= 2 and rel.parts[0] == "data" and rel.parts[1] == "raw":
            failures.append(f"file is tracked under data/raw: {rel}")

    # Double-blind manuscript should not identify the author or retain placeholders.
    blinded_text = BLINDED.read_text(encoding="utf-8")
    for token in BLINDED_FORBIDDEN:
        if token.lower() in blinded_text.lower():
            failures.append(f"blinded manuscript contains forbidden text: '{token}'")

    # Require an empty author field in the blinded manuscript.
    if not re.search(r"\\author\{\s*\}", blinded_text):
        failures.append("blinded manuscript does not have an empty \\author{} field")

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
