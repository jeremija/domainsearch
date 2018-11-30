PATH := $(CURDIR)/env/bin:$(PATH)
SHELL := sh

test: FORCE
	pytest

test-watch: FORCE
	pytest-watch domainsearch/

lint: FORCE
	flake8 domainsearch/

env:
	python3 -m venv env/

deps: env FORCE
	env/bin/pip3 install -r requirements.dev.txt

build: FORCE
	python3 setup.py sdist bdist_wheel

publish: FORCE
	twine upload dist/*

FORCE:
