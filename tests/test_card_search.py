def test_search_combined(client):
    # case-insensitive set dimensions, all filters must match (AND)
    response = client.post(
        "/card_search", json={"type": ["political action"], "sect": ["anarch"]}
    )
    assert response.status_code == 200
    names = response.json()
    assert "Eat the Rich" in names
    assert "Firebrand" in names
    # results are sorted
    assert names == sorted(names)


def test_search_full_mode(client):
    response = client.post(
        "/card_search",
        json={"type": ["political action"], "sect": ["anarch"], "mode": "full"},
    )
    assert response.status_code == 200
    cards = response.json()
    assert all(card["kind"] == "Library" for card in cards)
    assert {"Eat the Rich", "Firebrand"} <= {card["printed_name"] for card in cards}


def test_search_text(client):
    # the "text" filter matches names, card text and flavor text
    response = client.post("/card_search", json={"text": "archon investigation"})
    assert response.status_code == 200
    assert "Archon Investigation" in response.json()


def test_search_discipline_case_sensitive(client):
    superior = client.post("/card_search", json={"discipline": ["AUS"]}).json()
    inferior = client.post("/card_search", json={"discipline": ["aus"]}).json()
    # inferior matches every card with the discipline; superior is a strict subset
    assert set(superior) < set(inferior)


def test_search_group_number(client):
    # group is given as a number and mapped to krcg's "G2" form
    response = client.post("/card_search", json={"clan": ["Brujah"], "group": [2]})
    assert response.status_code == 200
    g2 = response.json()
    assert g2
    full = client.post(
        "/card_search", json={"clan": ["Brujah"], "group": [2], "mode": "full"}
    ).json()
    assert all(card["group"] == "G2" for card in full)


def test_search_empty_returns_all(client, cards):
    response = client.post("/card_search", json={})
    assert response.status_code == 200
    assert len(response.json()) == len(cards)


def test_search_dimensions(client):
    response = client.get("/card_search")
    assert response.status_code == 200
    dimensions = response.json()
    assert "Political Action" in dimensions["type"]
    assert "Anarch" in dimensions["sect"]
    assert dimensions["group"] == [
        None,
        "Any",
        "G1",
        "G2",
        "G3",
        "G4",
        "G5",
        "G6",
        "G7",
    ]


def test_search_no_body(client, cards):
    # posting without a body at all returns all cards, like an empty filter
    response = client.post("/card_search")
    assert response.status_code == 200
    assert len(response.json()) == len(set(cards.cards()))
