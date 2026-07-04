from krcg import analyzer


def test_candidates(client):
    response = client.post("/candidates", json={"cards": ["Cybele", "Nana Buruku"]})
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 10
    for entry in result:
        assert isinstance(entry["card"], str)
        assert 0 <= entry["score"] <= 1
        assert entry["average"] >= 0
        assert entry["deviation"] >= 0
    # the obvious staple shows up
    assert "Villein" in {entry["card"] for entry in result}


def test_candidates_full_mode(client):
    response = client.post(
        "/candidates", json={"cards": ["Cybele", "Nana Buruku"], "mode": "full"}
    )
    assert response.status_code == 200
    result = response.json()
    assert all(isinstance(entry["card"], dict) for entry in result)
    assert all("printed_name" in entry["card"] for entry in result)


def test_candidates_no_card(client):
    # with no card, returns the most played cards
    response = client.post("/candidates", json={})
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 10
    assert all(isinstance(entry["card"], str) for entry in result)


def test_candidates_invalid_card(client):
    response = client.post("/candidates", json={"cards": ["NotACard"]})
    assert response.status_code == 400


def test_candidates_too_few_examples(client, cards, TWDA):
    # a card played by fewer than 4 decks cannot produce enough examples
    played = analyzer.played(TWDA.values(), cards)
    rare = min(played, key=lambda card: played[card])
    assert played[rare] < 4
    response = client.post("/candidates", json={"cards": [rare.id]})
    assert response.status_code == 404


def test_candidates_no_body(client):
    # posting without a body at all behaves like an empty filter
    response = client.post("/candidates")
    assert response.status_code == 200
    assert len(response.json()) == 10
