MINICONDA=$(CURDIR)/.miniconda3
CONDA=$(MINICONDA)/bin/conda
VENV=$(CURDIR)/.venv
ENVIRONMENT=$(VENV)/environment.yml
PYTHON=$(VENV)/bin/python

.SILENT:

help:
	grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(CONDA):
	curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > $(CURDIR)/miniconda.sh
	bash $(CURDIR)/miniconda.sh -u -b -p $(MINICONDA)
	rm miniconda.sh

$(PYTHON): $(CONDA)
	echo "Installing python to $(PYTHON)"
	$(CONDA) env create -p $(VENV)

$(ENVIRONMENT): $(PYTHON) environment.yml
	$(CONDA) env update --prune --quiet -p $(VENV) -f environment.yml
	cp environment.yml $(ENVIRONMENT)

.PHONY: deps
deps: $(ENVIRONMENT) ## Install dependencies

run: deps ## Run the stimpmeter example
	$(PYTHON) stimpmeter.py 2 10