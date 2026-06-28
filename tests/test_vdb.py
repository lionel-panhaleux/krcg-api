import pytest


def _fetch(client, url):
    response = client.post("/vdb", json={"url": url})
    if response.status_code != 200:
        pytest.skip(f"VDB provider unavailable ({response.status_code})")
    return response.json()


def test_vdb(client):
    deck = _fetch(client, "https://vdb.im/decks/b798e734f")
    assert deck["id"] == "b798e734f"
    assert deck["author"] == "BCP"
    entries = {(card["id"], card["count"]) for card in deck["cards"]}
    assert {(200025, 2), (100845, 12), (100199, 4)} <= entries


def test_vdb_query_url(client):
    deck = _fetch(client, "https://vdb.im/decks?id=b798e734f")
    assert deck["id"] == "b798e734f"
