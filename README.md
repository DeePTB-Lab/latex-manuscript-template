# LaTeX Manuscript Template

[English](README.md) | [中文](README.zh-CN.md)

Reusable LaTeX manuscript template for DeePTB-Lab papers.

This repository is intended to serve as a starting point for scientific writing projects. It includes a REVTeX 4.2 manuscript skeleton, bibliography and figure conventions, local build commands, and pull-request checks for common LaTeX and bibliography issues.

## Repository Layout

- `main.tex`: manuscript source.
- `ref.bib`: bibliography database.
- `figs/`: figure assets referenced by `main.tex`.
- `Makefile`: local build shortcuts and TeX engine selection.
- `.latexmkrc`: shared `latexmk` defaults.
- `scripts/detect_tex_engine.py`: TeX engine detector used by `make`.
- `scripts/check_bib.py`: bibliography duplicate checker used by local and CI checks.
- `scripts/check_author_comments.py`: temporary author-comment checker.
- `scripts/check_latex_log.py`: LaTeX log checker for unresolved references and citations.
- `.github/workflows/latex.yml`: pull-request and push checks with PDF artifact upload.

## Build

Install a TeX distribution with `latexmk`, the needed TeX engine, required packages, and the REVTeX 4.2 class, then run:

```sh
make
```

Useful commands:

```sh
make                  # compile main.tex -> main.pdf
make check            # check bibliography, author comments, compile, and check the log
make check-bib        # check duplicate BibTeX entries
make check-comments   # check for unresolved temporary author comments
make watch            # rebuild when sources change
make clean            # remove intermediate LaTeX files
make distclean        # remove intermediates and main.pdf
```

The Makefile detects the TeX engine from `main.tex`: CJK text, `ctex`, `xeCJK`, or `fontspec` selects XeLaTeX; LuaLaTeX-specific packages select LuaLaTeX; otherwise it defaults to pdfLaTeX. Override when needed:

```sh
make ENGINE=xelatex
make ENGINE=pdflatex
make ENGINE=lualatex
```

The current example uses Chinese text through `ctex`, so it builds with XeLaTeX automatically.

## Using This Template

This repository is meant to support one GitHub repository per manuscript. Use the template repository for new papers, and import only the shared infrastructure for existing paper repositories.

### Starting a new manuscript repository

The recommended workflow is to enable **Template repository** in this repository's GitHub settings and create each new paper with **Use this template**.

After creating the new manuscript repository:

1. Replace the example content in `main.tex`.
2. Replace or extend `ref.bib` with the paper's bibliography.
3. Replace `figs/placeholder.pdf` with the paper's figures under `figs/`.
4. Rewrite this README so it describes the specific manuscript rather than the template.
5. Run `make check` before opening the first pull request.

The shared infrastructure copied from the template includes `.github/`, `scripts/`, `.latexmkrc`, `Makefile`, `.gitignore`, and `.editorconfig`.

### Adding template infrastructure to an existing manuscript repository

For an existing manuscript repository, do not copy files manually from a local checkout of this template. Instead, add this repository as a temporary remote and import only the shared infrastructure:

```sh
git remote add template https://github.com/DeePTB-Lab/latex-manuscript-template.git
git fetch template
git checkout template/master -- .github scripts .latexmkrc .gitignore .editorconfig
git remote remove template
```

This intentionally avoids overwriting article-specific files such as `main.tex`, `ref.bib`, `figs/`, and manuscript-specific README content.

If the existing manuscript repository does not have a `Makefile`, import the template Makefile too:

```sh
git checkout template/master -- Makefile
```

If the existing manuscript already has a `Makefile`, merge the relevant targets manually rather than overwriting it.

## Pull-Request Checks

Pull requests run the `LaTeX` GitHub Actions workflow. The workflow executes:

```sh
make check
```

This verifies that:

- the bibliography does not contain duplicate keys;
- the bibliography does not appear to contain repeated entries with the same DOI or title/year;
- temporary author comments such as `\ZH{}`, `\LZ{}`, `\TODO{}`, or `\todo{}` are not left in manuscript text;
- `main.tex` compiles through `latexmk` with the detected or explicitly selected TeX engine;
- LaTeX compilation stops on syntax errors because `.latexmkrc` enables `-halt-on-error`.
- unresolved references, unresolved citations, and selected BibTeX warnings fail the check.

The workflow uploads `main.pdf` as a GitHub Actions artifact when compilation produces it. Run `make check` locally before opening or updating a pull request.

## Version-Control Notes

The repository tracks manuscript sources, bibliography files, and source assets such as `figs/*.pdf`. Generated LaTeX artifacts such as `*.aux`, `*.bbl`, `*.log`, `*.synctex.gz`, and the generated `/main.pdf` are ignored by default.

If a journal submission or arXiv package needs generated files, create them locally and add the required files intentionally with `git add -f`.

## Manuscript Notes

`main.tex` currently contains template text, example equations, placeholder citations, and a placeholder figure. Replace these examples with the manuscript content before submission.
