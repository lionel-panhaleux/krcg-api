def test_deck_by_id(client, TWDA):
    twda_id = next(iter(TWDA))
    response = client.get(f"/twda/{twda_id}")
    assert response.status_code == 200
    deck = response.json()
    assert deck["id"] == twda_id
    # krcg v5 deck shape: a flat list of card entries
    assert isinstance(deck["cards"], list)
    assert all(
        {"id", "count", "kind", "types"} <= card.keys() for card in deck["cards"]
    )


def test_deck_by_id_not_found(client):
    assert client.get("/twda/NotADeck").status_code == 404


def test_deck_search_by_cards(client, cards):
    response = client.post("/twda", json={"cards": ["Cybele", "Nana Buruku"]})
    assert response.status_code == 200
    decks = response.json()
    wanted = {cards["Cybele"].id, cards["Nana Buruku"].id}
    for deck in decks:
        assert wanted <= {card["id"] for card in deck["cards"]}


def test_deck_list_by_cards(client):
    response = client.post("/twda/list", json={"cards": ["Cybele", "Nana Buruku"]})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == len(body["decks"])
    assert body["count"] > 0
    assert all({"id", "name", "date", "author"} <= d.keys() for d in body["decks"])


def test_deck_search_no_result(client):
    # no tournament happened after this date
    response = client.post("/twda", json={"date_from": "3000-01-01"})
    assert response.status_code == 404


def test_deck_search_by_player(client, TWDA):
    author = next(d.author for d in TWDA.values() if d.author)
    response = client.post("/twda", json={"player": author})
    assert response.status_code == 200
    assert response.json()


def test_random_deck(client):
    response = client.post("/twda/random", json={"cards": ["Cybele", "Nana Buruku"]})
    assert response.status_code == 200
    assert "cards" in response.json()


def test_deck_list_no_result(client):
    response = client.post("/twda/list", json={"date_from": "3000-01-01"})
    assert response.status_code == 404


def test_random_deck_no_result(client):
    response = client.post("/twda/random", json={"date_from": "3000-01-01"})
    assert response.status_code == 404
