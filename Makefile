.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


### Clean

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache


### Linting

lint: ## check style with flake8
	flake8 hotshopper tests


### Test

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source hotshopper -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html


### Build

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/hotshopper.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ hotshopper
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds wheel package
	python -m build --wheel --outdir dist .
	ls -l dist


### Install

install: clean ## install the package to the active Python's site-packages
	python -m pip install .

install-e: clean ## install the package as editable to the active Python environment
	python -m pip -e install .

### Dependencies

verify-pip-tools:
	sh makefile_helper.sh verify-pip-tools

deps-pin-versions: verify-pip-tools ## Pin version for all dependencies
	pip-compile --strip-extras -o requirements.txt pyproject.toml
	pip-compile --strip-extras --extra=dev -o requirements_dev.txt pyproject.toml

deps-upgrade: verify-pip-tools
	pip-compile \
		--upgrade \
		--strip-extras \
		-o requirements.txt \
		pyproject.toml

deps-upgrade-dev: verify-pip-tools
	pip-compile \
		--extra=dev \
		--upgrade \
		--strip-extras \
		-o requirements_dev.txt \
		pyproject.toml

deps-upgrade-all: deps-upgrade deps-upgrade-dev ## Upgrade and pin version for all dependencies

deps-install: verify-pip-tools ## Install user dependencies
	pip-sync requirements.txt

deps-install-dev: verify-pip-tools ## Install dev dependencies
	pip-sync requirements_dev.txt

deps-install-all: deps-install deps-install-dev ## Install dev & user dependencies


# Generate PlantUML diagrams

plantuml:
	pyreverse -o plantuml --module-names yes -s 1 -d hotshopper \
	hotshopper/hotshopper.py hotshopper/model.py hotshopper/foodplan.py
	sed -i "" "s/set namespaceSeparator none/set namespaceSeparator ./g" hotshopper/classes.plantuml
	@echo "DONE!"
