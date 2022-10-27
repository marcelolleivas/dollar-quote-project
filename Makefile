SHELL := /bin/bash

.pip:
	pip install --upgrade 'pip<22'

.install-dependencies:
	pip install pipenv pre-commit &&\
    pipenv install &&\
    pipenv shell

.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/

.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts

install-dev: .pip .install-dependencies

test:
	coverage run -m pytest &&\
	coverage report --fail-under=95

code-convention:
	pre-commit run --all-files
