import importlib.metadata
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from krcg import twda, vtes

from . import api

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    vtes.VTES.load()
    twda.TWDA.load()
    logger.info("launching app")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="KRCG API",
        description=(
            "**V:tES** cards and decks based on VEKN resources, "
            "including the [TWDA](http://www.vekn.fr/decks/twd.htm)."
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
