.PHONY: quality test serve release update clean

quality:
	black --check .
	flake8

test: quality
	pytest -vvs

serve:
	source .env && uwsgi --socket 127.0.0.1:8000 --protocol=http  --module krcg_api.wsgi:application

release:
	fullrelease
	pip install -e ".[dev]"

update:
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"

clean:
	rm -rf dist
	rm -rf .pytest_cache
