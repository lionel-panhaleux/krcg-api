import importlib.metadata
import logging
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from typing import Any

import aiohttp
import krcg
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from krcg import collections as krcg_collections
from krcg import twda
from scalar_fastapi import get_scalar_api_reference

from . import api

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")

DESCRIPTION = """
**V:tES** cards and decks, based on the VEKN official card texts and the
[Tournament Winning Deck Archive (TWDA)](http://www.vekn.fr/decks/twd.htm).
Cards and decks are served in the
[krcg v5](https://github.com/lionel-panhaleux/krcg) JSON format.

The raw schema is at [`/openapi.json`](/openapi.json) — feed it to any
OpenAPI client generator to get a typed SDK.

### Conventions

- **Discovery first:** call `GET /card_search` to list every valid value for
  every card filter (types, clans, disciplines, sets, artists…). Those values
  are also enumerated inline on the `POST /card_search` request body below.
- **`mode` parameter:** `/card_search` and `/candidates` return plain card
  names by default, or full card objects when `mode` is set to `full`.
- **Card identifiers:** wherever a card is accepted you can pass its numeric ID
  or its name (English or a supported translation, URL-encoded in path params).
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # one shared aiohttp session: loads the v5 data and serves the deck providers
    async with aiohttp.ClientSession() as session:
        app.state.http = session
        app.state.cards = await krcg.load_online(session)
        app.state.twda = await twda.load_online(session)
        logger.info("launching app")
        yield


def _unique_operation_id(route: APIRoute) -> str:
    """Use the handler name as the operationId for clean generated SDKs."""
    return route.name


def _sorted_values(values: Iterable[Any]) -> list[str]:
    """Sort dimension values, numerically when they are all digit strings."""
    vals = [str(v) for v in values]
    if all(v.lstrip("-").isdigit() for v in vals):
        return sorted(vals, key=lambda v: int(v))
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


def _inject_search_enums(
    schema: dict[str, Any], cards: krcg_collections.CardDict
) -> None:
    """Enumerate the live card-search dimensions on the request schema.

    The valid values for every (non-text) card filter come from the loaded
    data, so they cannot be hard-coded as static enums. Injecting them into
    the generated OpenAPI ``CardSearchRequest`` makes every value
    self-documented in the docs UIs and in any generated client.
    """
    props = (
        schema.get("components", {})
        .get("schemas", {})
        .get("CardSearchRequest", {})
        .get("properties", {})
    )
    for dimension, values in cards.search_dimensions.items():
        prop = props.get(dimension)
        if prop:
            _set_array_enum(prop, _sorted_values(values))


def create_app() -> FastAPI:
    app = FastAPI(
        title="KRCG API",
        description=DESCRIPTION,
        # Scalar (served at /scalar) is the only docs UI
        docs_url=None,
        redoc_url=None,
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
    # CORS is not handled here: the production reverse proxy serves permissive
    # CORS headers for the whole site (nginx_site role, open_api_paths)
    app.include_router(api.router, generate_unique_id_function=_unique_operation_id)

    original_openapi = app.openapi

    def openapi_with_enums() -> dict[str, Any]:
        if app.openapi_schema is not None:
            return app.openapi_schema
        schema = original_openapi()  # builds and caches the schema
        cards = getattr(app.state, "cards", None)
        if cards is None:
            # data not loaded yet — serve uncached so enums land once it is
            app.openapi_schema = None
            return schema
        _inject_search_enums(schema, cards)
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
