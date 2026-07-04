import pytest


def _fetch(client, url):
    response = client.post("/vtesdecks", json={"url": url})
    if response.status_code != 200:
        pytest.skip(f"VTES Decks provider unavailable ({response.status_code})")
    return response.json()


def test_vtesdecks(client):
    deck = _fetch(
        client,
        "https://vtesdecks.com/deck/user-lionelpx-bf26e06e078348e8b5852d4e86dbdf6c",
    )
    assert deck["id"] == "user-lionelpx-bf26e06e078348e8b5852d4e86dbdf6c"
    assert deck["name"] == "Test"
    assert deck["author"] == "lionelpx"
    assert deck["comment"] == "Here goes my description!"
    entries = {(card["id"], card["count"]) for card in deck["cards"]}
    assert (200001, 7) in entries  # Aabbt Kindred


def test_missing_url(client):
    assert client.post("/vtesdecks", json={}).status_code == 400


def test_invalid_url(client):
    response = client.post(
        "/vtesdecks", json={"url": "https://vtesdecks.com/not-a-deck"}
    )
    assert response.status_code == 400
