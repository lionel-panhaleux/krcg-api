.PHONY: quality test serve release update clean

quality:
	black --check .
	flake8

test: quality
	pytest -vvs

serve:
	run-krcg-api

release:
	fullrelease
	pip install -e ".[dev]"

update:
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"

clean:
	rm -rf dist
	rm -rf .pytest_cache
