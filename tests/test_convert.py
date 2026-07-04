DECK_TXT = (
    "Crypt (4 cards)\n"
    "2x Gilbert Duane\n"
    "2x Mariel, Lady Thunder\n"
    "Library (3 cards)\n"
    "3x Vessel\n"
)


def _entries(deck):
    return {(card["id"], card["count"]) for card in deck["cards"]}


def test_convert_txt_to_json(client):
    response = client.post(
        "/convert/json", content=DECK_TXT, headers={"content-type": "text/plain"}
    )
    assert response.status_code == 200
    deck = response.json()
    # krcg v5 flat card list, with kind/types on each entry
    assert _entries(deck) == {(200517, 2), (200929, 2), (102113, 3)}
    by_id = {card["id"]: card for card in deck["cards"]}
    assert by_id[200517]["kind"] == "Crypt"
    assert by_id[102113]["kind"] == "Library"
    assert by_id[102113]["types"] == ["Master"]


def test_convert_default_is_json(client):
    response = client.post(
        "/convert", content=DECK_TXT, headers={"content-type": "text/plain"}
    )
    assert response.status_code == 200
    assert "cards" in response.json()


def test_convert_json_to_text_formats(client):
    deck = client.post(
        "/convert/json", content=DECK_TXT, headers={"content-type": "text/plain"}
    ).json()
    twd = client.post("/convert/twd", json=deck)
    assert twd.status_code == 200
    assert "Crypt (4 cards" in twd.text
    assert "Gilbert Duane" in twd.text
    assert "Vessel" in twd.text
    for fmt in ("txt", "lackey", "jol", "vdb"):
        response = client.post(f"/convert/{fmt}", json=deck)
        assert response.status_code == 200
        assert response.text


def test_convert_invalid_json(client):
    response = client.post("/convert/json", json={"cards": [{"bogus": 1}]})
    assert response.status_code == 400


def test_convert_invalid_utf8(client):
    response = client.post(
        "/convert/txt",
        content=b"\xff\xfe\xfa",
        headers={"content-type": "text/plain"},
    )
    assert response.status_code == 400
