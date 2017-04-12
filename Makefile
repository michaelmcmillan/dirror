PYTHON=$(shell which python3)
test: unit-test

unit-test:
	@$(PYTHON) -m unittest test/test_check_tests_mirror_source.py

.PHONY: test
