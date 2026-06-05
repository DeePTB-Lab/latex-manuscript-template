MAIN := main
PDF := $(MAIN).pdf
BIB_FILES := $(filter-out mainNotes.bib,$(wildcard *.bib))
TEX_FILES := $(wildcard *.tex)
ENGINE ?= $(shell python3 scripts/detect_tex_engine.py $(MAIN).tex)
LATEXMK_ENGINE := $(if $(filter pdflatex,$(ENGINE)),pdf,$(ENGINE))

.PHONY: all pdf watch check check-bib check-comments check-log clean distclean

all: pdf

pdf:
	latexmk -$(LATEXMK_ENGINE) $(MAIN).tex

check: check-bib check-comments pdf check-log

check-bib:
	python3 scripts/check_bib.py $(BIB_FILES)

check-comments:
	python3 scripts/check_author_comments.py $(TEX_FILES)

check-log:
	python3 scripts/check_latex_log.py $(MAIN).log

watch:
	latexmk -$(LATEXMK_ENGINE) -pvc $(MAIN).tex

clean:
	latexmk -c $(MAIN).tex

distclean:
	latexmk -C $(MAIN).tex
	rm -f $(PDF)
