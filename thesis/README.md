# Independent research report

Compile root `main.tex` in Overleaf. The `thesis/` directory name is retained for compatibility; this is an independent research report, not a degree submission.

Chapters 4–5 retain explicitly marked legacy exploratory estimates for traceability. The abstract deliberately withholds those estimates until the repaired workflow establishes adequate diagnostics and sensitivity validation. No supervisor, institution, or degree affiliation is asserted.

Use `pdflatex -shell-escape main.tex`, `bibtex main`, then two LaTeX passes locally; the SVG package requires Inkscape. The journal manuscript starts at `manuscript/main.tex` and uses a narrower research question.
