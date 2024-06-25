SHELL := $(shell which bash)
MICRO_MAMBA := $(CURDIR)/.micromamba
MAMBA := $(MICRO_MAMBA)/micromamba
VENV := $(PWD)/.venv
DEPS := $(VENV)/.deps
PYTHON=$(VENV)/bin/python
PYTHON_CMD := PYTHONPATH=$(shell pwd) $(PYTHON)
PLATFORM=$(shell uname | tr '[:upper:]' '[:lower:]' | sed 's/darwin/osx/g')
ARCH := $(shell uname -m | sed 's/x86_64/64/g')

ifndef VERBOSE
.SILENT:
endif

FORCE:

help:
	grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(MAMBA):
	echo "Installing Mamba..."
	mkdir -p "$(MICRO_MAMBA)"
	curl -Ls https://micro.mamba.pm/api/micromamba/$(PLATFORM)-$(ARCH)/latest | tar -xj -C "$(MICRO_MAMBA)" --strip-components=1 bin/micromamba

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
test: $(DEPS) ## Run tests and linters
	$(PYTHON_CMD) -m pytest -vv

.PHONY: watch
watch: $(DEPS) ## Run tests continuously
	$(PYTHON_CMD) -m pytest_watch --runner $(VENV)/bin/pytest --ignore $(VENV) --ignore $(MICRO_MAMBA)

.PHONY: putting_chart
putting_chart: deps ## Generate a CSV file scaling distance by slope and green speed
	$(PYTHON_CMD) putting/putting_factors.py | tee putting.csv

SkytrakData/%.csv: FORCE
	$(PYTHON_CMD) skytrak/parser.py $@