import importlib.metadata
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiohttp
import krcg
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from krcg import twda

from . import api

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # one shared aiohttp session: loads the v5 data and serves the deck providers
    async with aiohttp.ClientSession() as session:
        app.state.http = session
        app.state.cards = await krcg.load_online(session)
        app.state.twda = await twda.load_online(session)
        logger.info("launching app")
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="KRCG API",
        description=(
            "**V:tES** cards and decks based on VEKN resources, "
            "including the [TWDA](http://www.vekn.fr/decks/twd.htm).\n\n"
            "Cards and decks are served in the "
            "[KRCG v5](https://github.com/lionel-panhaleux/krcg) JSON format."
        ),
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
    app.include_router(api.router)
    return app


application = create_app()


def main() -> None:
    uvicorn.run("krcg_api:application", host="0.0.0.0", port=5000)
