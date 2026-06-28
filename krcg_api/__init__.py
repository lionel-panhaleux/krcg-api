import importlib.metadata
import logging
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from krcg import twda, vtes
from scalar_fastapi import get_scalar_api_reference

from . import api

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")

DESCRIPTION = """
**V:tES** cards and decks, based on the VEKN official card texts and the
[Tournament Winning Deck Archive (TWDA)](http://www.vekn.fr/decks/twd.htm).

### Documentation flavors

This same API is documented three ways — pick whichever you prefer:

- [**Scalar**](/scalar) — modern reference with a built-in API client (default).
- [**Swagger UI**](/docs) — classic interactive "try it out" console.
- [**ReDoc**](/redoc) — clean three-pane reference for reading.

The raw schema is at [`/openapi.json`](/openapi.json) — feed it to any
OpenAPI client generator to get a typed SDK.

### Conventions

- **Discovery first:** call `GET /card_search` to list every valid value for
  every card filter (types, clans, disciplines, sets, artists…). Those values
  are also enumerated inline on the `POST /card_search` request body below.
- **`mode` parameter:** `/card_search` and `/candidates` return a plain list of
  card names by default, or full card objects when `mode` is set to `full`.
- **Card identifiers:** wherever a card is accepted you can pass its numeric ID
  or its name (English or a supported translation, URL-encoded in path params).
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    vtes.VTES.load()
    twda.TWDA.load()
    logger.info("launching app")
    yield


def _unique_operation_id(route: APIRoute) -> str:
    """Use the handler name as the operationId for clean generated SDKs."""
    return route.name


def _sorted_values(values: Iterable[Any]) -> list[str]:
    """Sort dimension values, numerically when they are all digit strings."""
    vals = [str(v) for v in values]
    if all(v.lstrip("-").isdigit() for v in vals):
        return sorted(vals, key=int)
    return sorted(vals)


def _set_array_enum(prop: dict[str, Any], values: list[str]) -> None:
    """Set ``enum`` on the array ``items`` of a (possibly optional) property."""
    candidates: list[dict[str, Any]] = []
    if prop.get("type") == "array":
        candidates.append(prop)
    for sub in prop.get("anyOf", []) + prop.get("oneOf", []):
        if isinstance(sub, dict) and sub.get("type") == "array":
            candidates.append(sub)
    for arr in candidates:
        items = arr.setdefault("items", {})
        if items.get("type") == "integer":
            items["enum"] = [int(v) for v in values]
        else:
            items["enum"] = list(values)


def _inject_search_enums(schema: dict[str, Any]) -> None:
    """Enumerate the live card-search dimensions on the request schema.

    The valid values for every (non-text) card filter are loaded from ``krcg``
    at startup, so they cannot be hard-coded as static enums. We inject them
    into the generated OpenAPI ``CardSearchRequest`` so every value is
    self-documented in the docs UIs and in any generated client.
    """
    try:
        dimensions = vtes.VTES.search_dimensions
    except Exception:  # pragma: no cover - data not loaded yet
        return
    props = (
        schema.get("components", {})
        .get("schemas", {})
        .get("CardSearchRequest", {})
        .get("properties", {})
    )
    for dimension, values in dimensions.items():
        prop = props.get(dimension)
        if prop:
            _set_array_enum(prop, _sorted_values(values))


def create_app() -> FastAPI:
    app = FastAPI(
        title="KRCG API",
        description=DESCRIPTION,
        version=importlib.metadata.version("krcg-api"),
        contact={
            "name": "KRCG API",
            "url": "https://github.com/lionel-panhaleux/krcg-api",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        lifespan=lifespan,
        openapi_tags=[
            {"name": "Card", "description": "Operations on VTES cards"},
            {"name": "Deck", "description": "Operations on VTES decks"},
        ],
    )
    app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type]
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api.router, generate_unique_id_function=_unique_operation_id)

    original_openapi = app.openapi

    def openapi_with_enums() -> dict[str, Any]:
        already_built = app.openapi_schema is not None
        schema = original_openapi()
        if not already_built:
            _inject_search_enums(schema)
        return schema

    app.openapi = openapi_with_enums  # ty: ignore[invalid-assignment]

    @app.get("/scalar", include_in_schema=False)
    def scalar_html() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url=app.openapi_url or "/openapi.json",
            title=app.title,
            telemetry=False,
        )

    return app


application = create_app()


def main() -> None:
    uvicorn.run("krcg_api:application", host="0.0.0.0", port=5000)
