PATH := $(CURDIR)/env/bin:$(PATH)
SHELL := sh

lint:
	flake8 domainsearch/

test:
	pytest domainsearch/
