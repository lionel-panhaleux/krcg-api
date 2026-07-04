def test(client):
    response = client.get("/complete/NotACard")
    assert response.status_code == 200
    assert response.json() == []
    # must match every word, if one word matches nothing, no match
    assert client.get("/complete/NotACard%20Pentex").json() == []
    # completion returns unique card names
    assert client.get("/complete/unn").json() == ["The unnamed", "Unnatural Disaster"]
    assert client.get("/complete/pentex").json() == [
        "Pentex™ Subversion",
        "Pentex™ Loves You!",
        "Enzo Giovanni, Pentex Board of Directors",
        "Enzo Giovanni, Pentex Board of Directors (ADV)",
        "Harold Zettler, Pentex Director",
    ]
    # for multiple words, all must match
    assert client.get("/complete/the%20ru").json() == [
        "The Rumor Mill, Tabloid Newspaper",
        "Darvag, The Butcher of Rus",
        "Loyiso, The Ruthless",
    ]
    # match names with special chars, and utf8/url-encoded queries
    expected = ["Rötschreck", "Rotting Behemoth", "Ulrike Rothbart"]
    assert client.get("/complete/rot").json() == expected
    assert client.get("/complete/röt").json() == expected
    assert client.get("/complete/r%C3%B6t").json() == expected
    # match omitted slashes
    assert client.get("/complete/Kpist%20m%204").json() == ["Kpist m/45"]
    # without an Accept-Language header, only the English name is completed
    assert client.get("/complete/Aide%20des").json() == ["Aid from Bats"]


def test_i18n(client):
    # with an Accept-Language header, the localized name is returned
    response = client.get("/complete/Aide%20des", headers={"Accept-Language": "fr"})
    assert response.json() == ["Aide des chauves-souris"]
    response = client.get("/complete/Ankara", headers={"Accept-Language": "fr"})
    assert response.json() == ["La citadelle d'Ankara, Turquie"]
    response = client.get("/complete/Ankara", headers={"Accept-Language": "es"})
    assert response.json() == ["La Ciudadela de Ankara, Turquía"]
