MINICONDA=$(CURDIR)/.miniconda3
CONDA=$(MINICONDA)/bin/conda
VENV=$(CURDIR)/.venv
PYTHON=$(VENV)/bin/python

.SILENT:

$(CONDA):
	curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > $(CURDIR)/miniconda.sh
	bash $(CURDIR)/miniconda.sh -u -b -p $(MINICONDA)
	rm miniconda.sh

$(PYTHON): $(CONDA)
	echo "Installing python to $(PYTHON)"
	$(CONDA) env create -p $(VENV)

.PHONY: deps
deps: $(PYTHON)

run: deps
	$(PYTHON) stimpmeter.py 2 10