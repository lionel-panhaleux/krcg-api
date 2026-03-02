import urllib.request

import pytest

from krcg import config
from krcg_api import create_app

from fastapi.testclient import TestClient


def pytest_sessionstart(session):
    # Do not launch tests is there is no proper Internet connection.
    try:
        urllib.request.urlopen("http://www.google.com", timeout=1)
    except OSError:
        pytest.fail("No internet connection")
    try:
        urllib.request.urlopen(config.KRCG_STATIC_SERVER, timeout=1)
    except OSError:
        pytest.fail("KRCG website not available")


@pytest.fixture(scope="session")
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client
