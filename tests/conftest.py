import pytest
import requests

from krcg import config
from krcg_api import api


def pytest_sessionstart(session):
    # Do not launch tests is there is no proper Internet connection.
    try:
        requests.get("http://www.google.com", timeout=1)
    except requests.exceptions.RequestException:
        pytest.fail("No internet connection")
    try:
        requests.get(config.KRCG_STATIC_SERVER, timeout=1)
    except requests.exceptions.RequestException:
        pytest.fail("KRCG website not available")


@pytest.fixture(scope="session")
def client():
    app = api.create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
