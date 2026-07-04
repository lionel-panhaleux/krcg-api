def test_card_by_name(client):
    assert client.get("/card/NotACard").status_code == 404
    response = client.get("/card/Alastor")
    assert response.status_code == 200
    card = response.json()
    # krcg v5 card shape
    assert card["id"] == 100038
    assert card["kind"] == "Library"
    assert card["printed_name"] == "Alastor"
    assert card["types"] == ["Political Action"]
    assert card["url"].startswith("https://static.krcg.org/")
    assert card["text"]
    assert any(p["set"]["code"] == "Gehenna" for p in card["prints"])
    assert card["rulings"]
    # library cards do not carry crypt-only fields
    assert "capacity" not in card
    assert "clan" not in card


def test_card_by_id(client):
    assert client.get("/card/Alastor").json() == client.get("/card/100038").json()


def test_crypt_card(client):
    # Gilbert Duane, a group 1 Malkavian
    card = client.get("/card/200517").json()
    assert card["kind"] == "Crypt"
    assert card["clan"] == "Malkavian"
    assert card["capacity"] == 7
    assert card["group"] == "G1"
    assert card["disciplines"] == ["AUS", "DOM", "OBF"]
    assert card["types"] == ["Vampire"]


def test_translated_name(client):
    # a card can be looked up by a translated name
    card = client.get("/card/La citadelle d'Ankara, Turquie").json()
    assert card["printed_name"] == "The Ankara Citadel, Turkey"
    assert card["i18n"]["fr"]["name"] == "La citadelle d'Ankara, Turquie"
