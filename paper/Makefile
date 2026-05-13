# Build paper.pdf and standalone figure previews.
# Requires: pdflatex (TeX Live), with IEEEtran, tikz, pgfplots, standalone.

PAPER  = paper
FIGDIR = figures
FIGS   = fig_architecture fig_threat_model fig_leakage_results \
         fig_query_budget fig_session_link fig_edge_admission

.PHONY: all paper figures clean

all: paper figures

paper: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).tex $(addprefix $(FIGDIR)/, $(addsuffix .tex,$(FIGS)))
	pdflatex -interaction=nonstopmode $(PAPER).tex
	pdflatex -interaction=nonstopmode $(PAPER).tex

figures:
	@for f in $(FIGS); do \
	    cd $(FIGDIR) && \
	    pdflatex -interaction=nonstopmode -jobname=$$f \
	        "\def\figfile{$$f.tex}\input{standalone_preamble.tex}" \
	    && cd .. ; \
	done

clean:
	rm -f $(PAPER).aux $(PAPER).log $(PAPER).out $(PAPER).toc \
	      $(PAPER).bbl $(PAPER).blg
	cd $(FIGDIR) && rm -f *.aux *.log *.out
