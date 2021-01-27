def test(client):
    response = client.get("/card/NotACard")
    assert response.status_code == 404
    response = client.get("/card/Alastor")
    assert response.status_code == 200
    assert response.json == {
        "id": 100038,
        "_name": "Alastor",
        "name": "Alastor",
        "url": "https://static.krcg.org/card/alastor.jpg",
        "types": ["Political Action"],
        "card_text": (
            "Requires a justicar or Inner Circle member.\n"
            "Choose a ready Camarilla vampire. If this referendum is successful, "
            "search your library for an equipment card and place this card "
            "and the equipment on the chosen vampire. "
            "Pay half the cost (round down) of the equipment. "
            "This vampire may enter combat with any vampire "
            "controlled by another Methuselah as a +1 stealth Ⓓ action. "
            "This vampire cannot commit diablerie. A vampire may have only one Alastor."
        ),
        "sets": {
            "Gehenna": [{"rarity": "Rare", "release_date": "2004-05-17"}],
            "Keepers of Tradition": [{"rarity": "Rare", "release_date": "2008-11-19"}],
            "Kindred Most Wanted": [
                {"copies": 1, "precon": "Alastors", "release_date": "2005-02-21"}
            ],
        },
        "scans": {
            "Gehenna": "https://static.krcg.org/card/set/gehenna/alastor.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/alastor.jpg"
            ),
            "Kindred Most Wanted": (
                "https://static.krcg.org/card/set/kindred-most-wanted/alastor.jpg"
            ),
        },
        "artists": ["Monte Moore"],
        "rulings": {
            "links": {
                "[LSJ 20040518]": (
                    "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/"
                    "4emymfUPwAM/B2SCC7L6kuMJ"
                ),
                "[ANK 20200901]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "78830-alastor-and-ankara-citadel#100653"
                ),
            },
            "text": [
                (
                    "If the given weapon costs blood, "
                    "the target Alastor pays the cost. [LSJ 20040518]"
                ),
                "Requirements do not apply. [ANK 20200901]",
            ],
        },
    }
    id_response = client.get("/card/100038")
    assert id_response.status_code == 200
    assert id_response.json == response.json


def test_slashes(client):
    # slash in names must be replaced by spaces
    response = client.get("/card/Kpist%20m%2045")
    assert response.status_code == 200


def test_i18n(client):
    response = client.get("/card/Aid%20from%20Bats")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": ["Eric Lofgren", "Melissa Benson"],
        "card_text": (
            "[ani] Strike: 1R damage, with 1 optional maneuver.\n"
            "[ANI] As above, with 1 optional press."
        ),
        "disciplines": ["ani"],
        "flavor_text": (
            "Hanging upside down like rows of disgusting old rags\n"
            "And grinning in their sleep. Bats!\n"
            'D.H. Lawrence, "Bat"'
        ),
        "id": 100029,
        "url": "https://static.krcg.org/card/aidfrombats.jpg",
        "name": "Aid from Bats",
        "_name": "Aid from Bats",
        "rulings": {
            "text": [
                (
                    "[ANI] The press can only be used during the current round. "
                    "[TOM 19960521]"
                )
            ],
            "links": {
                "[TOM 19960521]": (
                    "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/"
                    "poYD3n0TKGo/xvU5HW7lBxMJ"
                )
            },
        },
        "sets": {
            "Anarchs": [
                {"copies": 2, "precon": "Gangrel", "release_date": "2003-05-19"}
            ],
            "Camarilla Edition": [
                {"rarity": "Common", "release_date": "2002-08-19"},
                {"copies": 3, "precon": "Nosferatu", "release_date": "2002-08-19"},
            ],
            "First Blood": [
                {"copies": 6, "precon": "Nosferatu", "release_date": "2019-10-01"}
            ],
            "Jyhad": [{"rarity": "Common", "release_date": "1994-08-16"}],
            "Keepers of Tradition": [
                {"rarity": "Common", "release_date": "2008-11-19"}
            ],
            "Third Edition": [{"rarity": "Common", "release_date": "2006-09-04"}],
            "Vampire: The Eternal Struggle": [
                {"rarity": "Common", "release_date": "1995-09-15"}
            ],
        },
        "scans": {
            "Anarchs": "https://static.krcg.org/card/set/anarchs/aidfrombats.jpg",
            "Camarilla Edition": (
                "https://static.krcg.org/card/set/camarilla-edition/aidfrombats.jpg"
            ),
            "First Blood": (
                "https://static.krcg.org/card/set/first-blood/aidfrombats.jpg"
            ),
            "Jyhad": "https://static.krcg.org/card/set/jyhad/aidfrombats.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/aidfrombats.jpg"
            ),
            "Third Edition": (
                "https://static.krcg.org/card/set/third-edition/aidfrombats.jpg"
            ),
            "Vampire: The Eternal Struggle": (
                "https://static.krcg.org/card/set/"
                "vampire-the-eternal-struggle/aidfrombats.jpg"
            ),
        },
        "_i18n": {
            "es": {
                "card_text": (
                    "[ani] Ataque: 1 de daño a distancia, con 1 maniobra opcional.\n"
                    "[ANI] Como antes, con 1 acoso opcional."
                ),
                "flavor_text": (
                    "Colgando boca abajo como hileras de trapos viejos y repugnantes\n"
                    "Y sonriendo mientras duermen. ¡Murciélagos!\n"
                    'D.H. Lawrence, "Murciélago"'
                ),
                "name": "Ayuda de murciélagos",
                "sets": {"First Blood": "Primera Sangre"},
                "url": "https://static.krcg.org/card/es/aidfrombats.jpg",
            },
            "fr": {
                "card_text": (
                    "[ani] Frapper à toute portée : 1 point de dégâts, "
                    "avec 1 manœuvre optionnelle.\n"
                    "[ANI] Comme ci-dessus, avec 1 poursuite optionnelle."
                ),
                "flavor_text": (
                    "Pendues tête en bas comme des rangées de guenilles repoussantes\n"
                    "Et souriant de toutes leurs dents dans leur sommeil. "
                    "Des chauves-souris !\n"
                    'D.H. Lawrence, "La Chauve-souris"'
                ),
                "name": "Aide des chauves-souris",
                "sets": {"First Blood": "Premier Sang"},
                "url": "https://static.krcg.org/card/fr/aidfrombats.jpg",
            },
        },
        "types": ["Combat"],
    }
    # fetching by translated name does work if the name is exact
    # (for ease of use when combined with /complete)
    response = client.get("/card/Aide%20des%20chauves-souris")
    assert response.status_code == 200


def test_sets(client):
    # sets serialization (prom, POD, PDF sets, ...)
    response = client.get("/card/The%20Line")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": ["Carmen Cornet"],
        "card_text": (
            "Unique location.\n"
            "Lock to reduce the cost of an action card played by a vampire "
            "you control by 1 blood (this location is not locked if that "
            "card is canceled as it is played). Any vampire can steal this "
            "location as a Ⓓ action."
        ),
        "id": 101110,
        "url": "https://static.krcg.org/card/linethe.jpg",
        "name": "The Line",
        "_name": "Line, The",
        "rulings": {
            "text": [
                (
                    "Can be locked when the action is announced or when the cost is "
                    "paid. [ANK 20170605]"
                ),
                (
                    "Can be used to reduce the cost in blood of a recruit ally (eg. "
                    "{Shambling Hordes}) or employ retainer action. [ANK 20181007]"
                ),
                'Cannot be used by an ally acting "as a vampire". [ANK 20200605]',
            ],
            "links": {
                "[ANK 20170605]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "75862-timing-of-the-line#82113"
                ),
                "[ANK 20181007]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "77057-quick-question-on-the-line#91020"
                ),
                "[ANK 20200605]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "78671-can-an-ally-with-play-as-a-vampire-"
                    "use-the-line-to-reduce-action-costs#100015"
                ),
            },
        },
        "sets": {
            "Anthology": [
                {
                    "copies": 1,
                    "precon": "EC Berlin Edition",
                    "release_date": "2017-05-11",
                }
            ]
        },
        "scans": {
            "Anthology": "https://static.krcg.org/card/set/anthology/linethe.jpg"
        },
        "types": ["Master"],
    }
    # promo card
    response = client.get("/card/The%20Dracon")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": ["Ginés Quiñonero-Santiago"],
        "capacity": 11,
        "card_text": (
            "Independent: Cards requiring Vicissitude [vic] cost The Dracon "
            "1 fewer blood. He inflicts +1 damage or steals 1 additional "
            "blood or life with ranged strikes (even at close range). Flight "
            "[FLIGHT]. +1 bleed. +2 strength."
        ),
        "clans": ["Tzimisce"],
        "disciplines": ["ANI", "AUS", "POT", "THA", "VIC"],
        "group": "5",
        "id": 200385,
        "url": "https://static.krcg.org/card/draconthe.jpg",
        "name": "The Dracon",
        "_name": "Dracon, The",
        "sets": {
            "2015 Storyline Rewards": [{"copies": 1, "release_date": "2015-02-16"}],
            "2018 Humble Bundle": [
                {"copies": 2, "precon": "Humble Bundle", "release_date": "2018-10-04"}
            ],
            "2019 Promo Pack 1": [{"copies": 1, "release_date": "2019-04-08"}],
        },
        "scans": {
            "2015 Storyline Rewards": (
                "https://static.krcg.org/card/set/promo/draconthe.jpg"
            ),
            "2018 Humble Bundle": (
                "https://static.krcg.org/card/set/humble-bundle/draconthe.jpg"
            ),
            "2019 Promo Pack 1": (
                "https://static.krcg.org/card/set/promo-pack-1/draconthe.jpg"
            ),
        },
        "types": ["Vampire"],
    }
    # PDF
    response = client.get("/card/Ophidian%20Gaze")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": ["Ginés Quiñonero-Santiago"],
        "card_text": (
            "[pre][ser] Reduce a bleed against you by 2.\n"
            "[PRE][SER] Only usable during a political action, after blocks are "
            "declined. Cancel an action modifier as it is played, and its cost is not "
            "paid."
        ),
        "disciplines": ["pre", "ser"],
        "combo": True,
        "id": 101325,
        "url": "https://static.krcg.org/card/ophidiangaze.jpg",
        "name": "Ophidian Gaze",
        "_name": "Ophidian Gaze",
        "rulings": {
            "text": [
                "[SER][PRE] Can be used to cancel an action modifier player "
                '"after the action/referendum is successful" (eg. {Voter '
                "Captivatoin} or {Freak Drive}). [ANK 20180909]"
            ],
            "links": {
                "[ANK 20180909]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "76987-ophidian-gaze-and-post-referendum-action-modifiers#90501"
                ),
            },
        },
        "sets": {"The Unaligned": [{"rarity": "Common", "release_date": "2014-10-04"}]},
        "scans": {
            "The Unaligned": (
                "https://static.krcg.org/card/set/the-unaligned/ophidiangaze.jpg"
            ),
        },
        "types": ["Reaction"],
    }


def test_artists(client):
    # corrected wrongly spelled artist name in CSV
    # L. Snelly -> Lawrence Snelly
    response = client.get("/card/Tyler")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": ["Lawrence Snelly"],
        "capacity": 9,
        "card_text": (
            "Camarilla primogen: When Tyler diablerizes a vampire, she "
            "unlocks and gains a blood from the blood bank. Once per turn, "
            "she may burn a blood to get +1 bleed or an additional vote."
        ),
        "clans": ["Brujah"],
        "disciplines": ["dom", "for", "obt", "CEL", "POT", "PRE"],
        "group": "3",
        "id": 201397,
        "url": "https://static.krcg.org/card/tyler.jpg",
        "name": "Tyler",
        "_name": "Tyler",
        "sets": {
            "Blood Shadowed Court": [{"release_date": "2008-04-14"}],
            "Camarilla Edition": [{"rarity": "Vampire", "release_date": "2002-08-19"}],
        },
        "scans": {
            "Blood Shadowed Court": (
                "https://static.krcg.org/card/set/blood-shadowed-court/tyler.jpg"
            ),
            "Camarilla Edition": (
                "https://static.krcg.org/card/set/camarilla-edition/tyler.jpg"
            ),
        },
        "title": "Primogen",
        "types": ["Vampire"],
    }
    # merge alternative artist names in CSV in a single instance
    # Ginés Quiñonero -> Ginés Quiñonero-Santiago
    response = client.get("/card/Ashur%20Tablets")
    assert response.status_code == 200
    assert response.json == {  # noqa: E501
        "artists": [
            "Ginés Quiñonero-Santiago",
            "Sandra Chang-Adair",
        ],
        "card_text": (
            "Put this card in play. If you control three copies, remove all "
            "copies in play (even controlled by other Methuselahs) from the "
            "game to gain 3 pool and choose up to thirteen library cards "
            "from your ash heap; move one of the chosen cards to your hand "
            "and shuffle the others in your library."
        ),
        "id": 100106,
        "url": "https://static.krcg.org/card/ashurtablets.jpg",
        "name": "Ashur Tablets",
        "_name": "Ashur Tablets",
        "rulings": {
            "text": [
                "Can be played with no card in the ash heap. [PIB 20130119]",
                "Is played without announcing targets: they are only chosen once "
                "the third copy get into play. [LSJ 20091030]",
            ],
            "links": {
                "[PIB 20130119]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "44197-ashur-tablets-for-zero#44229"
                ),
                "[LSJ 20091030]": (
                    "https://groups.google.com/g/rec.games.trading-cards.jyhad"
                    "/c/ZKuCyTayYbc/m/5nMjLpX4DuMJ"
                ),
            },
        },
        "sets": {
            "Anthology": [{"copies": 3, "release_date": "2017-05-11"}],
            "Keepers of Tradition": [
                {"rarity": "Common", "release_date": "2008-11-19"}
            ],
        },
        "scans": {
            "Anthology": "https://static.krcg.org/card/set/anthology/ashurtablets.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/ashurtablets.jpg"
            ),
        },
        "types": ["Master"],
    }
