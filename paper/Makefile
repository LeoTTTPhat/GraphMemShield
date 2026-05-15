# Build the self-contained paper.pdf.
# Requires: pdflatex (TeX Live), with IEEEtran, tikz, and pgfplots.

PAPER  = paper

.PHONY: all paper clean

all: paper

paper: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex
	pdflatex -interaction=nonstopmode $(PAPER).tex
	pdflatex -interaction=nonstopmode $(PAPER).tex

clean:
	rm -f $(PAPER).aux $(PAPER).log $(PAPER).out $(PAPER).toc \
	      $(PAPER).bbl $(PAPER).blg
