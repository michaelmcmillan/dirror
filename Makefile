PYTHON=$(shell which python3)
test: unit-test

unit-test:
	@$(PYTHON) -m unittest test/test_dirror.py

.PHONY: test
