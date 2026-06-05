# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A reusable LaTeX manuscript template (REVTeX 4.2, APS `pra` class) for DeePTB-Lab papers. It ships a manuscript skeleton plus the shared build/CI infrastructure that downstream manuscripts import. `main.tex`, `ref.bib`, and `figs/` hold example content meant to be replaced; `.latexmkrc`, `Makefile`, `scripts/`, and `.github/` are the reusable infrastructure.

## Build and check

```sh
make                  # compile main.tex -> main.pdf with the detected TeX engine
make check            # check-bib + check-comments + compile + check-log (this is what CI runs)
make check-bib        # reject duplicate bibliography entries
make check-comments   # reject unresolved temporary author comments
make watch            # rebuild on source change (latexmk -pvc)
make clean            # remove LaTeX intermediates
make distclean        # remove intermediates and main.pdf
```

`ENGINE` can be overridden when needed:

```sh
make ENGINE=xelatex
make ENGINE=pdflatex
make ENGINE=lualatex
```

Always run `make check` before opening or updating a pull request — CI runs exactly that via `.github/workflows/latex.yml` and uploads `main.pdf` as a workflow artifact when compilation succeeds.

## Critical build constraints

- **TeX engine is selected by `Makefile`, not `.latexmkrc`.** `scripts/detect_tex_engine.py` returns `xelatex` for CJK text, `ctex`, `xeCJK`, or `fontspec`; `lualatex` for LuaLaTeX-specific packages; otherwise `pdflatex`. Override with `make ENGINE=xelatex`, `make ENGINE=pdflatex`, or `make ENGINE=lualatex` when a manuscript needs a specific engine. `.latexmkrc` only centralizes shared `latexmk` command behavior and `-halt-on-error`.
- **The current example builds with XeLaTeX automatically.** It contains Chinese text and uses `ctex`, so plain `make` selects XeLaTeX without hard-coding the whole template to XeLaTeX.
- **`make check` is strict.** `scripts/check_latex_log.py` fails the build on unresolved `\ref`/`\cite`, "Rerun to get citations correct", and any BibTeX `Warning--`. `scripts/check_author_comments.py` fails on unresolved temporary comment macros such as `\ZH{}`, `\LZ{}`, `\TODO{}`, and `\todo{}` outside macro definitions. A manuscript that compiles but leaves dangling references, bib warnings, or temporary comments will fail CI.
- **`scripts/check_bib.py` rejects duplicates** by key, by DOI, and by title+year (case-insensitive) across all `.bib` files. When adding references, check for existing entries first.
- **`mainNotes.bib` is excluded** from the bib check (`BIB_FILES` filters it out in the Makefile) and is gitignored — it is REVTeX-generated, not a source file. Put real references in `ref.bib`.

## Conventions

- Figures go in `figs/` as committed source assets (e.g. `figs/*.pdf`); reference them with `\includegraphics{figs/...}`.
- Generated artifacts (`*.aux`, `*.bbl`, `*.log`, `/main.pdf`, etc.) are gitignored. If a submission needs them committed, force-add intentionally with `git add -f`.
- `main.tex` defines many custom math shortcut macros in the preamble (e.g. `\be`/`\ee`, `\bk`, `\br`, `\hh`, `\ket{}`, `\abo`) and review-comment color macros (`\ZH{}`, `\LZ{}`, etc.). Preserve these when editing manuscript content.

## Propagating template changes to downstream manuscripts

Existing manuscript repos must NOT copy files from a local checkout. They import only shared infrastructure via the template remote:

```sh
git remote add template https://github.com/DeePTB-Lab/latex-manuscript-template.git
git fetch template
git checkout template/master -- .github scripts .latexmkrc .gitignore .editorconfig
git remote remove template
```

Never overwrite article-specific files (`main.tex`, `ref.bib`, `figs/`, manuscript-specific README content) this way. `Makefile` must be merged manually if the downstream repo has its own targets.
