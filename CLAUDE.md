# CLAUDE.md

Flask REST API for VTES card game data (VEKN card texts + TWDA). Built on the `krcg` package. No database — all data loaded in-memory at startup.

## Commands

`uv` + `just`: `just install`, `just quality`, `just test`, `just serve`
Single test: `uv run pytest tests/test_card.py::test_card -vvs`
Tests require internet access.

## Code Quality

ruff (format+lint), ty (type checker, all rules set to error), OpenAPI spec validated on CI.

## Architecture

All routes in `krcg_api/api.py` on a single Blueprint (`base`). Custom `KRCG(flask.Flask)` subclass adds CORS headers. `create_app()` in `__init__.py` loads `vtes.VTES`/`twda.TWDA` data. WSGI entrypoint: `krcg_api.wsgi:application`. OpenAPI spec: `krcg_api/templates/openapi.yaml` (also serves Swagger UI at `/`).

New endpoints: add handler in `api.py`, tests in `tests/`, update `openapi.yaml`, run `just test`.
