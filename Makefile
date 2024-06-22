SHELL := $(shell which bash)
MICRO_MAMBA := $(CURDIR)/.micromamba
MAMBA := $(MICRO_MAMBA)/micromamba
VENV := $(PWD)/.venv
DEPS := $(VENV)/.deps
PYTHON=$(VENV)/bin/python

.SILENT:

help:
	grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(MAMBA):
	echo "Installing Mamba..."
	$(SHELL) ./install-micromamba.sh "$(MICRO_MAMBA)"

$(PYTHON): | $(MAMBA)
	echo "Installing Python..."
	$(MAMBA) create --quiet --yes -p $(VENV)

$(DEPS): environment.yml $(PYTHON)
	echo "Installing dependencies..."
	rm -rf $(VENV)
	$(MAMBA) create --quiet --yes -p $(VENV)
	$(MAMBA) install --quiet --yes -p $(VENV) -f environment.yml
	cp environment.yml $(DEPS)

.PHONY: deps
deps: $(DEPS) ## Install dependencies

.PHONY: test
test: $(DEPS)  ## Run tests and linters
	$(PYTHON) -m pytest -vv

putting_chart: deps ## Generate a CSV file scaling distance by slope and green speed
	$(PYTHON) putting/putting_factors.py | tee putting.csv