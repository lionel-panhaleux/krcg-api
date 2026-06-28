import pytest


def _fetch(client, path, url):
    response = client.post(path, json={"url": url})
    if response.status_code != 200:
        pytest.skip(f"{path} provider unavailable ({response.status_code})")
    return response.json()


def test_amaranth(client):
    deck = _fetch(
        client,
        "/amaranth",
        "https://amaranth.vtes.co.nz/#deck/4d3aa426-70da-44b7-8cb7-92377a1a0dbd",
    )
    assert deck["id"] == "4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
    assert deck["author"] == "BCP"
    assert deck["name"] == "First Blood: Tremere"
    entries = {(card["id"], card["count"]) for card in deck["cards"]}
    # a sample of the known First Blood: Tremere contents (krcg v5 flat shape)
    assert {(201020, 2), (100845, 12), (100199, 4)} <= entries


def test_amaranth_form_encoded(client):
    response = client.post(
        "/amaranth",
        data={
            "url": (
                "https://amaranth.vtes.co.nz/#deck/4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
            )
        },
    )
    if response.status_code != 200:
        pytest.skip(f"amaranth provider unavailable ({response.status_code})")
    assert response.json()["author"] == "BCP"


def test_missing_url(client):
    assert client.post("/amaranth", json={}).status_code == 400
