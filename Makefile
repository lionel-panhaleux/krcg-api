.PHONY: quality test serve release update clean

quality:
	black --check .
	ruff check
	openapi-spec-validator krcg_api/templates/openapi.yaml

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
