# Thesis

Working title: **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**

Planned structure:
1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion, Conclusions, and Recommendations

The thesis will contain the full methodological detail and complete sensitivity-analysis record.


## Overleaf workflow

The thesis is written in LaTeX and is designed for a full-repository Overleaf sync. Select the **root-level `main.tex`** as the Overleaf main document. It includes the chapter files under `thesis/` and accesses the aggregate figures under `results/figures/`. The older `thesis/main.tex` is retained as a local-folder entry point, but the root `main.tex` is the recommended Overleaf entry point.

Current chapter files:
- `chapter1_introduction.tex`
- `chapter2_literature_review.tex`
- `chapter3_methodology.tex`
- `chapter4_results.tex`

The repository now applies the current KNUST Graduate School guide for A4 paper, 12-point Times-style text, a 4 cm gutter/inner margin with 2.5 cm remaining margins, one-and-a-half spacing in the main text, single spacing for the abstract/references/captions, Roman-numbered preliminary pages, centred bottom page numbers, and separate lists of tables and figures.

The root-level `main.tex` is the recommended Overleaf entry point.

### Metadata that must be completed before submission

Edit `thesis/config.tex` and replace:
- `[INSERT OFFICIAL DEGREE NAME]`
- `[INSERT SUPERVISOR NAME]`
- `[INSERT HEAD OF DEPARTMENT NAME]`
- submission month/year if they change.

The current abstract is 264 words, below the KNUST 350-word Master's limit.

### Font note

The KNUST guide specifies Times New Roman 12 pt. The current Overleaf setup uses `newtxtext/newtxmath`, a high-quality Times-compatible TeX family that compiles reliably without proprietary font files. If the Department requires literal Microsoft Times New Roman, switch the final project to XeLaTeX/LuaLaTeX and use an institution-approved Times New Roman font installation. Do not upload or redistribute proprietary font files through this repository.

### Declaration

The KNUST Graduate School guide places the authorship declaration immediately after the Table of Contents. The repository follows that order. The declaration text is a close paraphrase; compare it with the current Appendix 2 specimen before final submission if the Department requires verbatim institutional wording.
