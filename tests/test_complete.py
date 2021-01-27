def test(client):
    response = client.get("/complete")
    assert response.status_code == 404
    response = client.get("/complete/NotACard")
    assert response.status_code == 200
    assert response.json == []
    # must match every word, if one word matches nothing, no match
    response = client.get("/complete/NotACard%20Pentex")
    assert response.status_code == 200
    assert response.json == []
    # first word is a better match
    response = client.get("/complete/unn")
    assert response.status_code == 200
    assert response.json == ["Unnatural Disaster", "The unnamed"]
    # on same match level, order alphabetically
    response = client.get("/complete/pentex")
    assert response.status_code == 200
    assert response.json == [
        "Pentex™ Loves You!",  # Pentex is first word
        "Pentex™ Subversion",
        "Enzo Giovanni, Pentex Board of Directors",  # then alphabetically
        "Enzo Giovanni, Pentex Board of Directors (ADV)",
        "Harold Zettler, Pentex Director",
    ]
    # for multiple words, all must match
    response = client.get("/complete/the%20ru")
    assert response.status_code == 200
    assert response.json == [
        "The Rumor Mill, Tabloid Newspaper",
        "Darvag, The Butcher of Rus",
    ]
    # match names with special chars
    response = client.get("/complete/rot")
    assert response.status_code == 200
    assert response.json == ["Rötschreck", "Ulrike Rothbart"]
    response = client.get("/complete/r%C3%B6t")
    assert response.status_code == 200
    assert response.json == ["Rötschreck", "Ulrike Rothbart"]
    # match omitted slashes
    response = client.get("/complete/Kpist%20m%204")
    assert response.status_code == 200
    assert response.json == ["Kpist m/45"]
    # do not complete translations without accept-language header
    response = client.get("/complete/Aide%20des")
    assert response.status_code == 200
    assert response.json == []


def test_i18n(client):
    response = client.get("/complete/Aide%20des", headers=[("accept-language", "fr")])
    assert response.status_code == 200
    assert response.json == ["Aide des chauves-souris"]
    response = client.get("/complete/Ankara", headers=[("accept-language", "fr")])
    assert response.status_code == 200
    assert response.json == ["La citadelle d'Ankara, Turquie"]
    response = client.get("/complete/Ankara", headers=[("accept-language", "es")])
    assert response.status_code == 200
    assert response.json == ["La Ciudadela de Ankara, Turquía"]
