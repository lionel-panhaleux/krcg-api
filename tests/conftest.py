from unittest.mock import patch

import pytest

import krcg
from krcg import twda

from fastapi.testclient import TestClient
from krcg_api import create_app


@pytest.fixture(scope="session")
def cards():
    """The cards library, loaded from the bundled snapshot (offline, deterministic)."""
    return krcg.load_local()


@pytest.fixture(scope="session")
def TWDA():
    """The TWDA, loaded from the bundled snapshot (offline, deterministic)."""
    return twda.load_local()


@pytest.fixture(scope="session")
def client():
    """A TestClient backed by the bundled snapshot (no network at startup)."""

    async def _load_cards(session):
        return krcg.load_local()

    async def _load_twda(session):
        return twda.load_local()

    with (
        patch("krcg.load_online", _load_cards),
        patch("krcg.twda.load_online", _load_twda),
    ):
        app = create_app()
        with TestClient(app) as test_client:
            yield test_client
