import requests


def test_swagger(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json is None
    assert (
        response.data[:95]
        == b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>KRCG API</title>
"""
    )


def test_complete(client):
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
    # do not complete translations without accept-language header
    response = client.get("/complete/Aide%20des")
    assert response.status_code == 200
    assert response.json == []


def test_complete_i18n(client):
    response = client.get("/complete/Aide%20des", headers=[("accept-language", "fr")])
    assert response.status_code == 200
    assert response.json == ["Aide des chauves-souris"]
    response = client.get("/complete/Ankara", headers=[("accept-language", "fr")])
    assert response.status_code == 200
    assert response.json == ["La citadelle d'Ankara, Turquie"]
    response = client.get("/complete/Ankara", headers=[("accept-language", "es")])
    assert response.status_code == 200
    assert response.json == ["La Ciudadela de Ankara, Turquía"]


def test_card(client):
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
            "Gehenna": [{"Rarity": "Rare", "Release Date": "2004-05-17"}],
            "Keepers of Tradition": [{"Rarity": "Rare", "Release Date": "2008-11-19"}],
            "Kindred Most Wanted": [
                {"Copies": 1, "Precon": "Alastors", "Release Date": "2005-02-21"}
            ],
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
    # slash in names cannot be used
    response = client.get("/card/Kpist%20m45")
    assert response.status_code == 200
    # translated card
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
                {"Copies": 2, "Precon": "Gangrel", "Release Date": "2003-05-19"}
            ],
            "Camarilla Edition": [
                {"Rarity": "Common", "Release Date": "2002-08-19"},
                {"Copies": 3, "Precon": "Nosferatu", "Release Date": "2002-08-19"},
            ],
            "First Blood": [
                {"Copies": 6, "Precon": "Nosferatu", "Release Date": "2019-10-01"}
            ],
            "Jyhad": [{"Rarity": "Common", "Release Date": "1994-08-16"}],
            "Keepers of Tradition": [
                {"Rarity": "Common", "Release Date": "2008-11-19"}
            ],
            "Third Edition": [{"Rarity": "Common", "Release Date": "2006-09-04"}],
            "Vampire: The Eternal Struggle": [
                {"Rarity": "Common", "Release Date": "1995-09-15"}
            ],
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
    # fetching by translated name does not work out of the box
    response = client.get("/card/Aide%20des%20chauves-souris")
    assert response.status_code == 404
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
                    "Copies": 1,
                    "Precon": "EC Berlin Edition",
                    "Release Date": "2017-05-11",
                }
            ]
        },
        "types": ["Master"],
    }
    # sets serialization (promo, POD, PDF sets, ...)
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
            "2015 Storyline Rewards": [{"Copies": 1, "Release Date": "2015-02-16"}],
            "2018 Humble Bundle": [
                {"Copies": 2, "Precon": "Humble Bundle", "Release Date": "2018-10-04"}
            ],
            "2019 Promo Pack 1": [{"Copies": 1, "Release Date": "2019-04-08"}],
        },
        "types": ["Vampire"],
    }
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
        "sets": {"The Unaligned": [{"Rarity": "Common", "Release Date": "2014-10-04"}]},
        "types": ["Reaction"],
    }
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
            "Blood Shadowed Court": [{"Release Date": "2008-04-14"}],
            "Camarilla Edition": [{"Rarity": "Vampire", "Release Date": "2002-08-19"}],
        },
        "title": "Primogen",
        "types": ["Vampire"],
    }
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
            "Anthology": [{"Copies": 3, "Release Date": "2017-05-11"}],
            "Keepers of Tradition": [
                {"Rarity": "Common", "Release Date": "2008-11-19"}
            ],
        },
        "types": ["Master"],
    }


def test_deck(client):
    response = client.post("/deck")
    assert response.status_code == 200
    assert len(response.json) >= 3125
    # since Anthelios is banned, this number should stay stable
    response = client.post("/deck", json={"cards": ["Anthelios, The Red Star"]})
    assert response.status_code == 200
    assert len(response.json) == 320
    response = client.post("/deck", json={"cards": ["Not a Card"]})
    assert response.status_code == 400
    response = client.post("/deck", json={"cards": ["Madness of the Bard"]})
    assert response.status_code == 404
    response = client.post("/deck", json={"cards": [""]})
    # test deck parsing and serialization - it has both general and cards comments
    response = client.get("/deck/2020bf3hf")
    assert response.json == {
        "id": "2020bf3hf",
        "event": "Black Forest Base 3",
        "place": "Hyvinkää, Finland",
        "date": "2020-09-05",
        "name": "My stick is better than bacon",
        "tournament_format": "2R+F",
        "players_count": 14,
        "player": "Niko Vanhatalo",
        "score": "1gw5 + 3vp in the final",
        "comments": """Here is a quick report by the Winner of the event Niko Vanhatalo.

Just your average Ventrue grinder/stickmen with my own personal preferences

Finals were pretty brutal because every deck was a bleeder in some way or the
other and there was no clear winner even when it was down to 2 players.
Players from 1 to 5 were Petri with Anarch stealth bleeder, Jyrkkä with
Lasombra/Kiasyd stealth bleeder, Pauli with Ventrue grinder, me with my own
Ventrue grinder and Lasse with Legion and Legionnaire bleeder.  My biggest
concern was my predator who played pretty much the same deck with like 90% of
the crypt being the same cards, but we were able to avoid unnecesary contesting
thanks to table talk. He still contested my Lodin later in the game but was
ousted pretty fast after that before any real damage to me was done.
""",
        "crypt": {
            "cards": [
                {"count": 3, "id": 200848, "name": "Lodin (Olaf Holte)"},
                {"count": 2, "id": 200533, "name": "Graham Gottesman"},
                {"count": 2, "id": 201438, "name": "Victor Donaldson"},
                {"count": 1, "id": 201026, "name": "Mustafa, The Heir"},
                {"count": 1, "id": 200280, "name": "Claus Wegener"},
                {"count": 1, "id": 200421, "name": "Emily Carson"},
                {"count": 1, "id": 200691, "name": "Jephta Hester"},
                {"count": 1, "id": 201403, "name": "Ulrike Rothbart"},
            ],
            "count": 12,
        },
        "library": {
            "cards": [
                {
                    "cards": [
                        {"count": 1, "id": 100058, "name": "Anarch Troublemaker"},
                        {"count": 1, "id": 100545, "name": "Direct Intervention"},
                        {"count": 1, "id": 100588, "name": "Dreams of the Sphinx"},
                        {"count": 1, "id": 100824, "name": "Giant's Blood"},
                        {
                            "comments": (
                                "Neat card, but never played. "
                                "Should propably switch for another Dreams or Wash"
                            ),
                            "count": 1,
                            "id": 100842,
                            "name": "Golconda: Inner Peace",
                        },
                        {"count": 1, "id": 101225, "name": "Misdirection"},
                        {"count": 1, "id": 101350, "name": "Papillon"},
                        {"count": 2, "id": 101384, "name": "Pentex™ Subversion"},
                        {"count": 2, "id": 101388, "name": "Perfectionist"},
                        {"count": 2, "id": 102113, "name": "Vessel"},
                        {"count": 2, "id": 102121, "name": "Villein"},
                        {"count": 1, "id": 102151, "name": "Wash"},
                    ],
                    "count": 16,
                    "type": "Master",
                },
                {
                    "cards": [
                        {"count": 1, "id": 100573, "name": "Dominate Kine"},
                        {"count": 2, "id": 100652, "name": "Entrancement"},
                        {"count": 11, "id": 100845, "name": "Govern the Unaligned"},
                    ],
                    "count": 14,
                    "type": "Action",
                },
                {
                    "cards": [{"count": 2, "id": 100903, "name": "Heart of Nizchetus"}],
                    "count": 2,
                    "type": "Equipment",
                },
                {
                    "cards": [{"count": 4, "id": 101353, "name": "Parity Shift"}],
                    "count": 4,
                    "type": "Political Action",
                },
                {
                    "cards": [
                        {"count": 2, "id": 100236, "name": "Bonding"},
                        {"count": 3, "id": 100401, "name": "Conditioning"},
                        {"count": 3, "id": 100492, "name": "Daring the Dawn"},
                        {"count": 4, "id": 100788, "name": "Freak Drive"},
                        {"count": 5, "id": 101712, "name": "Seduction"},
                        {"count": 2, "id": 101978, "name": "Threats"},
                    ],
                    "count": 19,
                    "type": "Action Modifier",
                },
                {
                    "cards": [
                        {"count": 8, "id": 100518, "name": "Deflection"},
                        {"count": 3, "id": 101321, "name": "On the Qui Vive"},
                        {
                            "count": 4,
                            "id": 101706,
                            "name": "Second Tradition: Domain",
                        },
                        {
                            "comments": (
                                "This should be another On the Qui Vive "
                                "but I was too lazy to find 1 from my collection"
                            ),
                            "count": 1,
                            "id": 102137,
                            "name": "Wake with Evening's Freshness",
                        },
                    ],
                    "count": 16,
                    "type": "Reaction",
                },
                {
                    "cards": [
                        {"count": 5, "id": 100918, "name": "Hidden Strength"},
                        {"count": 6, "id": 100973, "name": "Indomitability"},
                        {
                            "count": 2,
                            "id": 101649,
                            "name": "Rolling with the Punches",
                        },
                        {"count": 4, "id": 102169, "name": "Weighted Walking Stick"},
                    ],
                    "count": 17,
                    "type": "Combat",
                },
            ],
            "count": 88,
        },
    }


def test_convert(client):
    response = client.post("/convert")
    assert response.status_code == 400
    assert response.data == b"Missing key: text or json"
    deck_json = {
        "crypt": {
            "cards": [
                {"count": 1, "id": 200517, "name": "Gilbert Duane"},
                {"count": 1, "id": 200929, "name": "Mariel, Lady Thunder"},
                {"count": 1, "id": 200161, "name": "Badr al-Budur"},
                {"count": 1, "id": 200295, "name": "Count Ormonde"},
                {"count": 1, "id": 200343, "name": "Didi Meyers"},
                {"count": 1, "id": 201503, "name": "Zebulon"},
                {"count": 1, "id": 200346, "name": "Dimple"},
                {"count": 1, "id": 201027, "name": "Mustafa Rahman"},
                {"count": 1, "id": 201065, "name": "Normal"},
                {"count": 1, "id": 201073, "name": "Ohanna"},
                {"count": 1, "id": 201231, "name": "Samson"},
                {"count": 1, "id": 200173, "name": "Basil"},
            ],
            "count": 12,
        },
        "library": {
            "cards": [
                {
                    "cards": [
                        {"count": 1, "id": 100327, "name": "Channel 10"},
                        {"count": 2, "id": 100332, "name": "Charisma"},
                        {"count": 1, "id": 100444, "name": "Creepshow Casino"},
                        {"count": 1, "id": 101067, "name": "KRCG News Radio"},
                        {"count": 2, "id": 101388, "name": "Perfectionist"},
                        {"count": 6, "id": 101877, "name": "Storage Annex"},
                        {"count": 3, "id": 101896, "name": "Sudden Reversal"},
                        {"count": 3, "id": 102113, "name": "Vessel"},
                    ],
                    "count": 19,
                    "type": "Master",
                },
                {
                    "cards": [
                        {"count": 1, "id": 100298, "name": "Carlton Van Wyk"},
                        {"count": 1, "id": 100855, "name": "Gregory Winter"},
                        {"count": 1, "id": 100966, "name": "Impundulu"},
                        {
                            "count": 1,
                            "id": 101250,
                            "name": "Muddled Vampire Hunter",
                        },
                        {"count": 1, "id": 101333, "name": "Ossian"},
                        {"count": 6, "id": 101491, "name": "Procurer"},
                        {"count": 1, "id": 102202, "name": "Young Bloods"},
                    ],
                    "count": 12,
                    "type": "Ally",
                },
                {
                    "cards": [
                        {"count": 1, "id": 100516, "name": "Deer Rifle"},
                        {"count": 8, "id": 100745, "name": "Flash Grenade"},
                    ],
                    "count": 9,
                    "type": "Equipment",
                },
                {
                    "cards": [
                        {"count": 6, "id": 100362, "name": "Cloak the Gathering"},
                        {"count": 7, "id": 100401, "name": "Conditioning"},
                        {"count": 2, "id": 101125, "name": "Lost in Crowds"},
                        {"count": 4, "id": 102097, "name": "Veil the Legions"},
                    ],
                    "count": 19,
                    "type": "Action Modifier",
                },
                {
                    "cards": [
                        {"count": 7, "id": 100518, "name": "Deflection"},
                        {"count": 2, "id": 100519, "name": "Delaying Tactics"},
                        {"count": 7, "id": 101321, "name": "On the Qui Vive"},
                    ],
                    "count": 16,
                    "type": "Reaction",
                },
                {
                    "cards": [{"count": 8, "id": 100392, "name": "Concealed Weapon"}],
                    "count": 8,
                    "type": "Combat",
                },
                {
                    "cards": [
                        {
                            "count": 1,
                            "id": 100709,
                            "name": "FBI Special Affairs " "Division",
                        },
                        {"count": 1, "id": 100944, "name": "Hunger Moon"},
                        {"count": 1, "id": 101614, "name": "Restricted Vitae"},
                        {"count": 1, "id": 102079, "name": "The Unmasking"},
                    ],
                    "count": 4,
                    "type": "Event",
                },
            ],
            "count": 87,
        },
    }
    deck_text = """Crypt (12 cards, min=7, max=24, avg=3.75)
-----------------------------------------
1x Gilbert Duane          7 AUS DOM OBF      prince  Malkavian:1
1x Mariel, Lady Thunder   7 DOM OBF aus tha          Malkavian:1
1x Badr al-Budur          5 OBF cel dom qui          Assamite:2
1x Count Ormonde          5 OBF dom pre ser          Follower of Set:2
1x Didi Meyers            5 DOM aus cel obf          Malkavian:1
1x Zebulon                5 OBF aus dom pro          Malkavian:1
1x Dimple                 2 obf                      Nosferatu:1
1x Mustafa Rahman         2 dom                      Tremere:2
1x Normal                 2 obf                      Malkavian:1
1x Ohanna                 2 dom                      Malkavian:2
1x Samson                 2 dom                      Ventrue antitribu:2
1x Basil                  1 obf                      Pander:2

Library (87 cards)
Master (19; 3 trifle)
1x Channel 10
2x Charisma
1x Creepshow Casino
1x KRCG News Radio
2x Perfectionist
6x Storage Annex
3x Sudden Reversal
3x Vessel

Ally (12)
1x Carlton Van Wyk
1x Gregory Winter
1x Impundulu
1x Muddled Vampire Hunter
1x Ossian
6x Procurer
1x Young Bloods

Equipment (9)
1x Deer Rifle
8x Flash Grenade

Action Modifier (19)
6x Cloak the Gathering
7x Conditioning
2x Lost in Crowds
4x Veil the Legions

Reaction (16)
7x Deflection
2x Delaying Tactics
7x On the Qui Vive

Combat (8)
8x Concealed Weapon

Event (4)
1x FBI Special Affairs Division
1x Hunger Moon
1x Restricted Vitae
1x Unmasking, The"""
    response = client.post("/convert", json={"format": "lackey", "text": deck_text})
    assert response.status_code == 200
    assert response.json == {
        "result": (
            "1\tChannel 10\n"
            "2\tCharisma\n"
            "1\tCreepshow Casino\n"
            "1\tKRCG News Radio\n"
            "2\tPerfectionist\n"
            "6\tStorage Annex\n"
            "3\tSudden Reversal\n"
            "3\tVessel\n"
            "1\tCarlton Van Wyk\n"
            "1\tGregory Winter\n"
            "1\tImpundulu\n"
            "1\tMuddled Vampire Hunter\n"
            "1\tOssian\n"
            "6\tProcurer\n"
            "1\tYoung Bloods\n"
            "1\tDeer Rifle\n"
            "8\tFlash Grenade\n"
            "6\tCloak the Gathering\n"
            "7\tConditioning\n"
            "2\tLost in Crowds\n"
            "4\tVeil the Legions\n"
            "7\tDeflection\n"
            "2\tDelaying Tactics\n"
            "7\tOn the Qui Vive\n"
            "8\tConcealed Weapon\n"
            "1\tFBI Special Affairs Division\n"
            "1\tHunger Moon\n"
            "1\tRestricted Vitae\n"
            "1\tUnmasking, The\n"
            "Crypt:\n"
            "1\tGilbert Duane\n"
            "1\tMariel, Lady Thunder\n"
            "1\tBadr al-Budur\n"
            "1\tCount Ormonde\n"
            "1\tDidi Meyers\n"
            "1\tZebulon\n"
            "1\tDimple\n"
            "1\tMustafa Rahman\n"
            "1\tNormal\n"
            "1\tOhanna\n"
            "1\tSamson\n"
            "1\tBasil"
        ),
    }
    response = client.post("/convert", json={"format": "jol", "text": deck_text})
    assert response.status_code == 200
    assert response.json == {
        "result": (
            "1x Gilbert Duane\n"
            "1x Mariel, Lady Thunder\n"
            "1x Badr al-Budur\n"
            "1x Count Ormonde\n"
            "1x Didi Meyers\n"
            "1x Zebulon\n"
            "1x Dimple\n"
            "1x Mustafa Rahman\n"
            "1x Normal\n"
            "1x Ohanna\n"
            "1x Samson\n"
            "1x Basil\n"
            "\n"
            "1x Channel 10\n"
            "2x Charisma\n"
            "1x Creepshow Casino\n"
            "1x KRCG News Radio\n"
            "2x Perfectionist\n"
            "6x Storage Annex\n"
            "3x Sudden Reversal\n"
            "3x Vessel\n"
            "1x Carlton Van Wyk\n"
            "1x Gregory Winter\n"
            "1x Impundulu\n"
            "1x Muddled Vampire Hunter\n"
            "1x Ossian\n"
            "6x Procurer\n"
            "1x Young Bloods\n"
            "1x Deer Rifle\n"
            "8x Flash Grenade\n"
            "6x Cloak the Gathering\n"
            "7x Conditioning\n"
            "2x Lost in Crowds\n"
            "4x Veil the Legions\n"
            "7x Deflection\n"
            "2x Delaying Tactics\n"
            "7x On the Qui Vive\n"
            "8x Concealed Weapon\n"
            "1x FBI Special Affairs Division\n"
            "1x Hunger Moon\n"
            "1x Restricted Vitae\n"
            "1x Unmasking, The"
        ),
    }
    response = client.post("/convert", json={"format": "twd", "text": deck_text})
    assert response.status_code == 200
    assert response.json == {"result": deck_text}
    response = client.post("/convert", json={"format": "json", "text": deck_text})
    assert response.status_code == 200
    assert response.json == {"result": deck_json}
    response = client.post("/convert", json={"json": deck_json})
    assert response.status_code == 200
    assert response.json == {"result": deck_text}


def test_amaranth(client):
    first_blood_tremere = {
        "author": "BCP",
        "crypt": {
            "cards": [
                {"count": 2, "id": 201020, "name": "Muhsin Samir"},
                {"count": 2, "id": 201213, "name": "Rutor"},
                {"count": 2, "id": 201388, "name": "Troius"},
                {"count": 2, "id": 201501, "name": "Zane"},
                {"count": 2, "id": 200025, "name": "Aidan Lyle"},
                {"count": 2, "id": 200280, "name": "Claus Wegener"},
            ],
            "count": 12,
        },
        "date": "2020-12-13",
        "id": "4d3aa426-70da-44b7-8cb7-92377a1a0dbd",
        "library": {
            "cards": [
                {
                    "cards": [
                        {"count": 1, "id": 100015, "name": "Academic Hunting Ground"},
                        {"count": 1, "id": 100081, "name": "Arcane Library"},
                        {"count": 4, "id": 100199, "name": "Blood Doll"},
                        {"count": 1, "id": 100329, "name": "Chantry"},
                        {"count": 2, "id": 102092, "name": "Vast Wealth"},
                    ],
                    "count": 9,
                    "type": "Master",
                },
                {
                    "cards": [
                        {"count": 12, "id": 100845, "name": "Govern the Unaligned"}
                    ],
                    "count": 12,
                    "type": "Action",
                },
                {
                    "cards": [{"count": 1, "id": 101963, "name": "Thadius Zho"}],
                    "count": 1,
                    "type": "Ally",
                },
                {
                    "cards": [
                        {"count": 4, "id": 100001, "name": ".44 Magnum"},
                        {"count": 1, "id": 101014, "name": "Ivory Bow"},
                        {"count": 2, "id": 101856, "name": "Sport Bike"},
                    ],
                    "count": 7,
                    "type": "Equipment",
                },
                {
                    "cards": [{"count": 1, "id": 100335, "name": "Charnas the Imp"}],
                    "count": 1,
                    "type": "Retainer",
                },
                {
                    "cards": [{"count": 6, "id": 100236, "name": "Bonding"}],
                    "count": 6,
                    "type": "Action Modifier",
                },
                {
                    "cards": [
                        {"count": 4, "id": 100644, "name": "Enhanced Senses"},
                        {"count": 5, "id": 100760, "name": "Forced Awakening"},
                        {"count": 5, "id": 101321, "name": "On the Qui Vive"},
                        {"count": 4, "id": 101475, "name": "Precognition"},
                        {"count": 4, "id": 101850, "name": "Spirit's Touch"},
                        {"count": 8, "id": 101949, "name": "Telepathic Misdirection"},
                    ],
                    "count": 30,
                    "type": "Reaction",
                },
                {
                    "cards": [
                        {"count": 8, "id": 100077, "name": "Apportation"},
                        {"count": 10, "id": 101966, "name": "Theft of Vitae"},
                        {"count": 2, "id": 102139, "name": "Walk of Flame"},
                    ],
                    "count": 20,
                    "type": "Combat",
                },
            ],
            "count": 86,
        },
    }
    response = client.post(
        "/amaranth",
        data={
            "url": (
                "https://amaranth.vtes.co.nz/#deck/"
                "4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
            )
        },
    )
    assert response.status_code == 200
    assert response.json == first_blood_tremere
    response = client.post(
        "/amaranth",
        json={
            "url": (
                "https://amaranth.vtes.co.nz/#deck/"
                "4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
            )
        },
    )
    assert response.status_code == 200
    assert response.json == first_blood_tremere


def test_card_search_dimensions(client):
    response = client.get("/card")
    assert response.status_code == 200
    assert response.json == {
        "artist": [
            "Aaron Acevedo",
            "Aaron Voss",
            "Abrar Ajmal",
            "Alan Rabinowitz",
            "Albrecht",
            "Alejandro Colucci",
            "Alejandro F. Giraldo",
            "Alexander Dunnigan",
            "Amy Weber",
            "Amy Wilkins",
            "Andre Gates",
            "Andrew Bates",
            "Andrew Hepworth",
            "Andrew Robinson",
            "Andrew Trabbold",
            "André Freitas",
            "Anna Christenson",
            "Anna Evertsdotter",
            "Anson Maddocks",
            "Ari Targownik",
            "Arkady Roytman",
            "Arthur Roberg",
            "Ash Arnett",
            "Atilio Gambedotti",
            "Attila Adorjany",
            "August Bøgedal Hansen",
            "Avery Butterworth",
            "Becky Cloonan",
            "Becky Jollensten",
            "Ben Mirabelli",
            "Beth Trott",
            "Bob Stevlic",
            "Brad Williams",
            "Brian Ashmore",
            "Brian Horton",
            "Brian LeBlanc",
            "Brian Miskelley",
            "Brian Snoddy",
            "Britt Martin",
            "Bryon Wackwitz",
            "Caleb Cleaveland",
            "Carmen Cornet",
            "Chad Michael Ward",
            "Chet Masters",
            "Chris McLoughlin",
            "Chris Richards",
            "Chris Stevens",
            "Christel Espenkrona",
            "Christopher Rush",
            "Christopher Shy",
            "Cliff Nielson",
            "Clint Langley",
            "Corey Macourek",
            "Cos Koniotis",
            "Craig Grant",
            "Craig Maher",
            "D. Fryendall",
            "Dan Frazier",
            "Dan Smith",
            "Daniel Gelon",
            "Darryl Elliott",
            "Dave Leri",
            "Dave Roach",
            "Dave Seeley",
            "David Day",
            "David Fooden",
            "David Ho",
            "David Kimmel",
            "Dennis Calero",
            "Diana Vick",
            "Doug Alexander",
            "Doug Gregory",
            "Doug Stambaugh",
            "Douglas Shuler",
            "Drew Tucker",
            "Durwin Talon",
            "E.M. Gist",
            "Ed Tadem",
            "Edward Beard, Jr.",
            "Efrem Palacios",
            "Elli Adams",
            "Eric Deschamps",
            "Eric Kim",
            "Eric LaCombe",
            "Eric Lofgren",
            "Erica Danell",
            "Felipe Gaona",
            "Francesc Grimalt",
            "Franz Vohwinkel",
            "Fred Harper",
            "Fred Hooper",
            "Gary Chatterton",
            "Gary Leach",
            "Ginés Quiñonero-Santiago",
            "Glen Osterberger",
            "Grant Garvin",
            "Grant Goleash",
            "Greg Boychuk",
            "Greg Loudon",
            "Greg Simanson",
            "Grzegorz Bobrowski",
            "Gábor Németh",
            "Hannibal King",
            "Harold Arthur McNeill",
            "Heather Hudson",
            "Heather J. McKinney",
            "Heather V. Kreiter",
            "Ian Hernaiz",
            "Imaginary Friends Studios",
            "J Frederick Y",
            "Jake Smidt",
            "James Allen Higgins",
            "James Richardson",
            "James Stowe",
            "Jami Waggoner",
            "Jared Smith",
            "Jarkko Suvela",
            "Jason Alexander Behnke",
            "Jason Brubaker",
            "Javier Santos",
            'Jeff "el jefe" Holt',
            "Jeff Klimek",
            "Jeff Laubenstein",
            "Jeff Menges",
            "Jeff Miracola",
            "Jeff Rebner",
            "Jenny Frison",
            "Jeremy C. Bills",
            "Jeremy McHugh",
            "Jesús Ybarzábal",
            "Jim Di Bartolo",
            "Jim Nelson",
            "Jim Pavelec",
            "Joe Slucher",
            "Joe Ziolkowski",
            "Joel Biske",
            "John Bolton",
            "John Bridges",
            "John Kent",
            "John Matson",
            "John McCrea",
            "John Scotello",
            "John Van Fleet",
            "Josh Timbrook",
            "Juan Antonio Serrano Garcia",
            "Juan Calle",
            "Julian Jackson",
            "Julie Collins",
            "Justin Norman",
            "Kaja Foglio",
            "Kari Christensen",
            "Karl Waller",
            "Katie McCaskill",
            "Kelly Howlett",
            "Ken Meyer, Jr.",
            "Kent Williams",
            "Kevin McCann",
            "Kieran Yanner",
            "Kyri Koniotis",
            "L. A. Williams",
            "Laia López Tubau",
            "Larry MacDougall",
            "Lawrence Snelly",
            "Lee Carter",
            "Lee Dotson",
            "Lee Fields",
            "Leif Jones",
            "Liz Danforth",
            "Marco Marzoni",
            "Marco Nelor",
            "Margaret Organ-Kean",
            "Marian Churchland",
            "Mark Kelly",
            "Mark Nelson",
            "Mark Poole",
            "Mark Tedin",
            "Martín de Diego Sábada",
            "Mathias Kollros",
            "Matias Tapia",
            "Matt Cavotta",
            "Matt Dixon",
            "Matt Smith",
            "Matt Wilson",
            "Matthew Mitchell",
            "Max Shade Fellwalker",
            "Melissa Benson",
            "Melissa Uran",
            "Michael Astrachan",
            "Michael Dixon",
            "Michael Gaydos",
            "Michael Weaver",
            "Mick Bertilorenzi",
            "Mike Chaney",
            "Mike Danza",
            "Mike Dringenberg",
            "Mike Huddleston",
            "Mike Raabe",
            "Mirko Falloni",
            "Mitch Mueller",
            "Monte Moore",
            "Newel Anderson",
            "Nicola Leonard",
            'Nicolas "Dimple" Bigot',
            "Nicole Cardiff",
            "Nigel Sade",
            "Nilson",
            "Noah Hirka",
            "Noora Hirvonen",
            "Né Né Thomas",
            "Oliver Meinerding",
            "Oscar Salcedo",
            "Pat Loboyko",
            "Pat Morrissey",
            "Patrick Kochakji",
            "Patrick Lambert",
            "Patrick McEvoy",
            "Paul Ballard",
            "Paul Tobin",
            "Pete Burges",
            "Pete Venters",
            "Peter Bergting",
            "Peter Kim",
            "Peter Morbacher",
            "Phil Wohr",
            "Phillip Hilliker",
            "Phillip Tan",
            "Quinton Hoover",
            "Randy Asplund",
            "Randy Gallegos",
            "Rebecca Guay",
            "Riccardo Fabiani",
            "Richard Kane Ferguson",
            "Richard Thomas",
            "Rick Berry",
            "Rick O'Brien",
            "Rik Martin",
            "Rob Alexander",
            "Robert McNeill",
            "Robin Chyo",
            "Roel Wielinga",
            "Roger Raupp",
            "Ron Lemon",
            "Ron Spencer",
            "Ron Van Halen",
            "Rubén Bravo",
            "Samuel Araya",
            "Sandra Chang-Adair",
            "Sandra Everingham",
            "Satyr",
            "Scott Fischer",
            "Scott Kirschner",
            "Scott M. Bakal",
            "Shane Coppage",
            "Steve Casper",
            "Steve Eidson",
            "Steve Ellis",
            "Steve Prescott",
            "Stuart Beel",
            "Stuart Sayger",
            "Sue Ann Harkey",
            "Susan Van Camp",
            "Talon Dunning",
            "Ted Naifeh",
            "Terese Nielsen",
            "Thea Maia",
            "Theodore Black",
            "Thomas Baxa",
            "Thomas Denmark",
            "Thomas Manning",
            "Thomas Nairb",
            "Tim Bradstreet",
            "Tom Biondillo",
            "Tom Duncan",
            "Tom Gianni",
            "Tom Wänerstrand",
            'Tomáš "zelgaris" Zahradníček',
            "Tony Harris",
            "Tony Shasteen",
            "Torstein Nordstrand",
            "Travis Ingram",
            "Trevor Claxton",
            "UDON",
            "Vatche Mavlian",
            "Veronica Jones",
            "Vince Locke",
            "Warren Mahy",
            "Will Simpson",
            "William O'Connor",
            "Zina Saunders",
            "matrix von z",
            "rk post",
        ],
        "bonus": ["Bleed", "Capacity", "Intercept", "Stealth", "Trifle", "Votes"],
        "capacity": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "city": [
            "Addis Ababa",
            "Amsterdam",
            "Aragon",
            "Athens",
            "Atlanta",
            "Barcelona",
            "Berlin",
            "Birmingham",
            "Boston",
            "Brussels",
            "Budapest",
            "Buenos Aires",
            "Cairo",
            "Canberra",
            "Cape Town",
            "Chicago",
            "Cleveland",
            "Columbus",
            "Copenhagen",
            "Cordoba",
            "Corte",
            "Dallas",
            "Detroit",
            "Dublin",
            "Fortaleza",
            "Frankfurt",
            "Geneva",
            "Glasgow",
            "Guadalajara",
            "Guatemala City",
            "Houston",
            "Istanbul",
            "Lisbon",
            "London",
            "Los Angeles",
            "Manila",
            "Mannheim",
            "Melbourne",
            "Mexico City",
            "Miami",
            "Milan",
            "Milwaukee",
            "Monaco",
            "Montreal",
            "Nairobi",
            "New York",
            "Paris",
            "Perth",
            "Philadelphia",
            "Pittsburgh",
            "Port-au-Prince",
            "Prague",
            "Rio de Janeiro",
            "Rome",
            "Rotterdam",
            "San Diego",
            "Seattle",
            "Stockholm",
            "Strasbourg",
            "Sydney",
            "Taipei",
            "Toronto",
            "Venice",
            "Versailles",
            "Washington, D.C.",
        ],
        "clan": [
            "Abomination",
            "Ahrimane",
            "Akunanse",
            "Assamite",
            "Avenger",
            "Baali",
            "Blood Brother",
            "Brujah",
            "Brujah antitribu",
            "Caitiff",
            "Daughter of Cacophony",
            "Defender",
            "Follower of Set",
            "Gangrel",
            "Gangrel antitribu",
            "Gargoyle",
            "Giovanni",
            "Guruhi",
            "Harbinger of Skulls",
            "Innocent",
            "Ishtarri",
            "Judge",
            "Kiasyd",
            "Lasombra",
            "Malkavian",
            "Malkavian antitribu",
            "Martyr",
            "Nagaraja",
            "Nosferatu",
            "Nosferatu antitribu",
            "Osebo",
            "Pander",
            "Ravnos",
            "Redeemer",
            "Salubri",
            "Salubri antitribu",
            "Samedi",
            "Toreador",
            "Toreador antitribu",
            "Tremere",
            "Tremere antitribu",
            "True Brujah",
            "Tzimisce",
            "Ventrue",
            "Ventrue antitribu",
            "Visionary",
            "none",
        ],
        "discipline": [
            "ABO",
            "ANI",
            "AUS",
            "CEL",
            "CHI",
            "DAI",
            "DEM",
            "DOM",
            "FOR",
            "MEL",
            "MYT",
            "NEC",
            "OBE",
            "OBF",
            "OBT",
            "POT",
            "PRE",
            "PRO",
            "QUI",
            "SAN",
            "SER",
            "SPI",
            "TEM",
            "THA",
            "THN",
            "VAL",
            "VIC",
            "VIS",
            "abo",
            "ani",
            "aus",
            "cel",
            "chi",
            "choice",
            "combo",
            "dai",
            "def",
            "dem",
            "dom",
            "flight",
            "for",
            "inn",
            "jud",
            "maleficia",
            "mar",
            "mel",
            "mono",
            "multi",
            "myt",
            "nec",
            "none",
            "obe",
            "obf",
            "obt",
            "pot",
            "pre",
            "pro",
            "qui",
            "red",
            "san",
            "ser",
            "spi",
            "striga",
            "tem",
            "tha",
            "thn",
            "val",
            "ven",
            "vic",
            "vin",
            "vis",
        ],
        "group": [1, 2, 3, 4, 5, 6],
        "precon": [
            "2018 Humble Bundle: Humble Bundle",
            "Anarchs: Anarch Barons",
            "Anarchs: Anarch Gang",
            "Anarchs: Gangrel",
            "Anthology: EC Berlin Edition",
            "Black Hand: Malkavian antitribu",
            "Black Hand: Nosferatu antitribu",
            "Black Hand: Toreador antitribu",
            "Black Hand: Tremere antitribu",
            "Camarilla Edition: Brujah",
            "Camarilla Edition: Malkavian",
            "Camarilla Edition: Nosferatu",
            "Camarilla Edition: Toreador",
            "Camarilla Edition: Tremere",
            "Camarilla Edition: Ventrue",
            "Fifth Edition: Malkavian",
            "Fifth Edition: Nosferatu",
            "Fifth Edition: Toreador",
            "Fifth Edition: Tremere",
            "Fifth Edition: Ventrue",
            "Final Nights: Assamite",
            "Final Nights: Followers of Set",
            "Final Nights: Giovanni",
            "Final Nights: Ravnos",
            "First Blood: Malkavian",
            "First Blood: Nosferatu",
            "First Blood: Toreador",
            "First Blood: Tremere",
            "First Blood: Ventrue",
            "Heirs to the Blood: Gargoyles",
            "Heirs to the Blood: Kiasyd",
            "Heirs to the Blood: Reprint Bundle 1",
            "Heirs to the Blood: Reprint Bundle 2",
            "Heirs to the Blood: Salubri antitribu",
            "Heirs to the Blood: Samedi",
            "Keepers of Tradition: Brujah",
            "Keepers of Tradition: Malkavian",
            "Keepers of Tradition: Reprint Bundle 1",
            "Keepers of Tradition: Reprint Bundle 2",
            "Keepers of Tradition: Toreador",
            "Keepers of Tradition: Ventrue",
            "Kindred Most Wanted: Alastors",
            "Kindred Most Wanted: Anathema",
            "Kindred Most Wanted: Baali",
            "Kindred Most Wanted: Gangrel antitribu",
            "Legacies of Blood: Akunanse",
            "Legacies of Blood: Guruhi",
            "Legacies of Blood: Ishtarri",
            "Legacies of Blood: Osebo",
            "Lords of the Night: Assamite",
            "Lords of the Night: Followers of Set",
            "Lords of the Night: Giovanni",
            "Lords of the Night: Ravnos",
            "Print on Demand: DriveThruCards",
            "Sabbat Preconstructed: Den of Fiends",
            "Sabbat Preconstructed: Libertine Ball",
            "Sabbat Preconstructed: Pact with Nephandi",
            "Sabbat Preconstructed: Parliament of Shadows",
            "Sabbat War: Brujah antitribu",
            "Sabbat War: Lasombra",
            "Sabbat War: Tzimisce",
            "Sabbat War: Ventrue antitribu",
            "Tenth Anniversary: Tin A",
            "Tenth Anniversary: Tin B",
            "Third Edition: Brujah antitribu",
            "Third Edition: Malkavian antitribu",
            "Third Edition: Tremere antitribu",
            "Third Edition: Tzimisce",
        ],
        "rarity": ["Common", "Rare", "Uncommon", "Vampire"],
        "sect": ["Anarch", "Camarilla", "Independent", "Laibon", "Sabbat"],
        "set": [
            "1996 Promo",
            "2003 Tournament promo",
            "2004 promo",
            "2005 Storyline promo",
            "2005 Tournament promo",
            "2006 Championship promo",
            "2006 EC Tournament promo",
            "2006 Storyline promo",
            "2006 Tournament promo",
            "2007 Promo",
            "2008 Storyline promo",
            "2008 Tournament promo",
            "2009 Tournament / Storyline promo",
            "2010 Storyline promo",
            "2015 Storyline Rewards",
            "2018 Humble Bundle",
            "2019 AC Promo",
            "2019 ACC Promo",
            "2019 DriveThruCards Promo",
            "2019 EC Promo",
            "2019 Grand Prix Promo",
            "2019 NAC Promo",
            "2019 Promo",
            "2019 Promo Pack 1",
            "2019 SAC Promo",
            "2020 GP Promo",
            "2020 Promo Pack 2",
            "Anarch Unbound",
            "Anarchs",
            "Anarchs promo",
            "Ancient Hearts",
            "Anthology",
            "Black Hand",
            "Black Hand promo",
            "Blood Shadowed Court",
            "Bloodlines",
            "Bloodlines promo",
            "Camarilla Edition",
            "Camarilla Edition promo",
            "Danse Macabre",
            "Dark Sovereigns",
            "Ebony Kingdom",
            "Fall 2002 Storyline promo",
            "Fall 2004 Storyline promo",
            "Fifth Edition",
            "Final Nights",
            "Final Nights promo",
            "First Blood",
            "Gehenna",
            "Gehenna promo",
            "Heirs to the Blood",
            "Jyhad",
            "Keepers of Tradition",
            "Kindred Most Wanted",
            "Kindred Most Wanted promo",
            "Legacies of Blood",
            "Legacies of Blood promo",
            "Lords of the Night",
            "Lost Kindred",
            "Nights of Reckoning",
            "Print on Demand",
            "Prophecies league promo",
            "Sabbat",
            "Sabbat Preconstructed",
            "Sabbat War",
            "Sabbat War promo",
            "Summer 2003 Storyline promo",
            "Sword of Caine",
            "Sword of Caine promo",
            "Tenth Anniversary",
            "The Unaligned",
            "Third Edition",
            "Third Edition promo",
            "Twenty-Fifth Anniversary",
            "Twilight Rebellion",
            "V5 Polish Edition promo",
            "Vampire: The Eternal Struggle",
            "Winter 2002 Storyline promo",
        ],
        "title": [
            "1 vote",
            "2 votes",
            "Archbishop",
            "Baron",
            "Bishop",
            "Cardinal",
            "Imperator",
            "Inner Circle",
            "Justicar",
            "Kholo",
            "Magaji",
            "Primogen",
            "Prince",
            "Priscus",
            "Regent",
        ],
        "trait": [
            "Black Hand",
            "Infernal",
            "Red List",
            "Scarce",
            "Seraph",
            "Slave",
            "Sterile",
        ],
        "type": [
            "Action",
            "Action Modifier",
            "Ally",
            "Combat",
            "Conviction",
            "Crypt",
            "Equipment",
            "Event",
            "Imbued",
            "Library",
            "Master",
            "Political Action",
            "Power",
            "Reaction",
            "Retainer",
            "Vampire",
        ],
    }


def test_candidates(client):
    response = client.post("/candidates")
    assert response.status_code == 200
    assert len(response.json) == 10
    response = client.post("/candidates", json={"date_from": "2019", "date_to": "2020"})
    assert response.status_code == 200
    assert response.json == [
        {
            "average": 2,
            "card": "Dreams of the Sphinx",
            "deviation": 0.86,
            "score": 0.6939,
        },
        {
            "average": 1,
            "card": "Pentex™ Subversion",
            "deviation": 0.44,
            "score": 0.6531,
        },
        {"average": 3, "card": "On the Qui Vive", "deviation": 1.49, "score": 0.5918},
        {"average": 4, "card": "Villein", "deviation": 1.92, "score": 0.5646},
        {"average": 1, "card": "Giant's Blood", "deviation": 0.0, "score": 0.5102},
        {"average": 1, "card": "Wider View", "deviation": 0.55, "score": 0.4082},
        {
            "average": 2,
            "card": "Information Highway",
            "deviation": 0.87,
            "score": 0.4014,
        },
        {"average": 3, "card": "Vessel", "deviation": 1.25, "score": 0.3605},
        {"average": 5, "card": "Deflection", "deviation": 2.12, "score": 0.3401},
        {
            "average": 5,
            "card": "Telepathic Misdirection",
            "deviation": 1.56,
            "score": 0.3333,
        },
    ]
    response = client.post(
        "/candidates",
        json={
            "cards": ["Cybele", "Nana Buruku"],
            "date_from": "2015",
            "date_to": "2020",
        },
    )
    assert response.status_code == 200
    assert response.json == [
        {"average": 14, "card": "Ashur Tablets", "deviation": 6.25, "score": 1.0},
        {"average": 1, "card": "Giant's Blood", "deviation": 0.0, "score": 1.0},
        {"average": 2, "card": "The Parthenon", "deviation": 0.81, "score": 1.0},
        {"average": 1, "card": "Archon Investigation", "deviation": 0.0, "score": 0.9},
        {"average": 5, "card": "Villein", "deviation": 1.7, "score": 0.9},
        {"average": 1, "card": "Wider View", "deviation": 0.42, "score": 0.9},
        {"average": 3, "card": "Aksinya Daclau", "deviation": 0.43, "score": 0.8},
        {"average": 2, "card": "Dreams of the Sphinx", "deviation": 0.6, "score": 0.8},
        {"average": 8, "card": "Liquidation", "deviation": 2.42, "score": 0.8},
        {"average": 1, "card": "Pentex™ Subversion", "deviation": 0.48, "score": 0.8},
    ]


def test_card_search(client):
    response = client.post("/card")
    assert response.status_code == 200
    assert len(response.json) >= 3788
    # non-existing filters have no impact
    response = client.post("/card", json={"foo": ["bar"]})
    assert response.status_code == 422
    assert response.json is None
    assert response.data == (
        b"Invalid search dimension {'foo'}. Valid dimensions are: ['name', 'card_text"
        b"', 'flavor_text', 'type', 'sect', 'clan', 'title', 'city', 'trait', 'group',"
        b" 'capacity', 'discipline', 'artist', 'set', 'rarity', 'precon', 'bonus', "
        b"'text']"
    )
    # non-existing values do not crash
    response = client.post("/card", json={"bonus": ["foo"]})
    assert response.status_code == 200
    assert response.json == []
    response = client.post("/card", json={"trait": ["foo"]})
    assert response.status_code == 200
    assert response.json == []
    # card text
    response = client.post(
        "/card", json={"text": "this equipment card represents a location"}
    )
    assert response.json == [
        "Catacombs",
        "Dartmoor, England",
        "Inveraray, Scotland",
        "Living Manse",
        "Local 1111",
        "Lyndhurst Estate, New York",
        "Palatial Estate",
        "Pier 13, Port of Baltimore",
        "Ruins of Ceoris",
        "Ruins of Villers Abbey, Belgium",
        "Sacré-Cœur Cathedral, France",
        "San Lorenzo de El Escorial, Spain",
        "San Nicolás de los Servitas",
        "The Ankara Citadel, Turkey",
        "Winchester Mansion",
        "Zaire River Ferry",
    ]
    # discipline, title
    response = client.post("/card", json={"title": ["primogen"], "discipline": ["ser"]})
    assert response.json == ["Amenophobis"]
    # city title
    response = client.post("/card", json={"city": ["chicago"]})
    assert response.json == [
        "Antón de Concepción",
        "Crusade: Chicago",
        "Horatio Ballard",
        "Lachlan, Noddist",
        "Lodin (Olaf Holte)",
        "Maldavis (ADV)",
        "Maxwell",
        "Praxis Seizure: Chicago",
        "Sir Walter Nash",
    ]
    # stealth, votes
    response = client.post("/card", json={"bonus": ["stealth", "votes"]})
    assert response.json == [
        "Antonio Veradas",
        "Bulscu (ADV)",
        "Dark Selina",
        "Jessica (ADV)",
        "Joseph Cambridge",
        "Karen Suadela",
        "Loki's Gift",
        "Maxwell",
        "Natasha Volfchek",
        "Perfect Paragon",
        "Sela (ADV)",
        "Suhailah",
        "Zayyat, The Sandstorm",
    ]

    # votes provided by master cards
    response = client.post(
        "/card",
        json={"bonus": ["votes"], "clan": ["Assamite"], "type": ["Master"]},
    )
    assert response.json == ["Alamut", "The Black Throne"]
    # votes provided by titles
    response = client.post(
        "/card",
        json={"bonus": ["votes"], "clan": ["Assamite"], "group": [3]},
    )
    assert response.json == ["Enam", "Rebekah"]
    # title when MERGED
    response = client.post("/card", json={"clan": ["Assamite"], "title": ["justicar"]})
    assert response.json == ["Tegyrius, Vizier (ADV)"]
    # traits: black hand, red list ...
    response = client.post(
        "/card",
        json={"clan": ["Nagaraja"], "trait": ["black hand"]},
    )
    assert response.json == ["Sennadurek"]
    # return full card info
    response = client.post(
        "/card",
        json={"clan": ["Nagaraja"], "trait": ["black hand"], "mode": "full"},
    )
    assert response.json == [
        {
            "artists": ["Andrew Trabbold"],
            "capacity": 6,
            "card_text": (
                "Sabbat. Black Hand: Whenever a Methuselah loses the Edge when "
                "it is not your turn, Sennadurek unlocks, and you may look at "
                "that Methuselah's hand. Scarce."
            ),
            "clans": ["Nagaraja"],
            "disciplines": ["dom", "AUS", "NEC"],
            "group": "4",
            "id": 201263,
            "url": "https://static.krcg.org/card/sennadurek.jpg",
            "_name": "Sennadurek",
            "name": "Sennadurek",
            "rulings": {
                "text": [
                    "Black Hand is not a title, it is a trait unrelated to any sect. "
                    "The trait is not lost if the vampire changes sect. [LSJ "
                    "20070322] [ANK 20180807]"
                ],
                "links": {
                    "[LSJ 20070322]": (
                        "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/"
                        "Ww-4rYJxi4w/P3QchWVq2o4J"
                    ),
                    "[ANK 20180807]": (
                        "http://www.vekn.net/forum/rules-questions/"
                        "76905-going-anarch-as-black-hand#89735"
                    ),
                },
            },
            "sets": {
                "Legacies of Blood": [
                    {"Rarity": "Uncommon", "Release Date": "2005-11-14"}
                ]
            },
            "types": ["Vampire"],
        }
    ]
    response = client.post("/card", json={"clan": ["Assamite"], "trait": ["red list"]})
    assert response.json == ["Jamal", "Tariq, The Silent (ADV)"]
    # sect
    response = client.post(
        "/card",
        json={"clan": ["assamite"], "sect": ["camarilla"], "group": [2]},
    )
    assert response.json == [
        "Al-Ashrad, Amr of Alamut (ADV)",
        "Tegyrius, Vizier",
        "Tegyrius, Vizier (ADV)",
    ]
    # traits on library cards
    response = client.post(
        "/card",
        json={"type": ["action modifier"], "trait": ["black hand"]},
    )
    assert response.json == [
        "Circumspect Revelation",
        "Seraph's Second",
        "The Art of Memory",
    ]
    # required title
    response = client.post("/card", json={"type": ["reaction"], "title": ["justicar"]})
    assert response.json == ["Legacy of Power", "Second Tradition: Domain"]
    # "Requires titled Sabbat/Camarilla" maps to all possible titles
    response = client.post(
        "/card",
        json={"bonus": ["intercept"], "title": ["archbishop"]},
    )
    assert response.json == [
        "Matteus, Flesh Sculptor",
        "National Guard Support",
        "Persona Non Grata",
        "Under Siege",
    ]
    # Reducing intercept is stealth
    response = client.post(
        "/card",
        json={"bonus": ["stealth"], "discipline": ["chi"], "type": ["library"]},
    )
    assert response.json == [
        "Fata Morgana",
        "Mirror's Visage",
        "Smoke and Mirrors",
        "Will-o'-the-Wisp",
    ]
    # Reducing stealth is intercept
    response = client.post(
        "/card",
        json={
            "bonus": ["intercept"],
            "discipline": ["chi"],
            "type": ["library"],
        },
    )
    assert response.json == [
        "Draba",
        "Ignis Fatuus",
        # multi-disc are tricky: it has chi, it has intercept.
        # chi doesn't provide intercept, but it matches - fair enough
        "Netwar",
        "Veiled Sight",
    ]
    # no discipline (crypt)
    response = client.post("/card", json={"discipline": ["none"], "type": ["crypt"]})
    assert response.json == ["Anarch Convert", "Sandra White", "Smudge the Ignored"]
    response = client.post(
        "/card",
        json={"discipline": ["none"], "bonus": ["intercept"], "sect": ["sabbat"]},
    )
    # no discipline, sect (or independent) required
    assert response.json == ["Abbot", "Harzomatuili", "Under Siege"]
    response = client.post(
        "/card",
        json={"type": ["political action"], "sect": ["independent"]},
    )
    assert response.json == ["Free States Rant", "Reckless Agitation"]
    response = client.post(
        "/card",
        json={"type": ["political action"], "sect": ["anarch"]},
    )
    assert response.json == [
        "Anarch Salon",
        "Eat the Rich",
        "Firebrand",
        "Free States Rant",
        "Patsy",
        "Reckless Agitation",
        "Revolutionary Council",
        "Sweeper",
    ]
    # multi-disciplines
    response = client.post(
        "/card",
        json={"discipline": ["multi", "ani"], "bonus": ["intercept"]},
    )
    assert response.json == [
        "Detect Authority",
        "Falcon's Eye",
        "Read the Winds",
        "Speak with Spirits",
        "The Mole",
    ]
    # superior disciplines (vampires only)
    response = client.post("/card", json={"discipline": ["OBE"], "group": [2]})
    assert response.json == ["Blanche Hill", "Matthias"]
    # Gwen Brand special case, disciplines abbreviations
    response = client.post(
        "/card",
        json={
            "clan": ["ravnos"],
            "group": [5],
            "discipline": ["AUS", "CHI", "FOR", "ANI"],
        },
    )
    assert response.json == ["Gwen Brand"]
    # i18n - still always perform text search in english
    response = client.post(
        "/card",
        json={"text": "this equipment card represents a location", "lang": "fr"},
    )
    assert response.json == [
        "Catacombs",
        "Dartmoor, England",
        "Inveraray, Scotland",
        "Living Manse",
        "Local 1111",
        "Lyndhurst Estate, New York",
        "Palatial Estate",
        "Pier 13, Port of Baltimore",
        "Ruins of Ceoris",
        "Ruins of Villers Abbey, Belgium",
        "Sacré-Cœur Cathedral, France",
        "San Lorenzo de El Escorial, Spain",
        "San Nicolás de los Servitas",
        "The Ankara Citadel, Turkey",
        "Winchester Mansion",
        "Zaire River Ferry",
    ]
    # text also matches card name
    response = client.post(
        "/card",
        json={"text": "Ankara"},
    )
    assert response.json == ["The Ankara Citadel, Turkey"]
    # i18n - but match the given language in addition to it
    response = client.post(
        "/card",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - should work with regions too, whatever their case
    response = client.post(
        "/card",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr-fr"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - should work with regions too, whatever their case
    response = client.post(
        "/card",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr_FR"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - do not match unrelated translations
    response = client.post(
        "/card", json={"text": "esta carta de equipo representa un lugar", "lang": "fr"}
    )
    assert response.json == []
    response = client.post(
        "/card", json={"text": "esta carta de equipo representa un lugar", "lang": "es"}
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # artist
    response = client.post("/card", json={"artist": ["E.M. Gist"]})
    assert response.json == [
        "Flames of Insurrection",
        "Harmony",
        "Marcus Vitel",
        "Public Enemy",
        "Rutor",
    ]


def test_deck_search(client):
    response = client.post(
        "/deck",
        json={
            "date_from": "2015-01-01",
            "date_to": "2020-01-01",
            "player": "Serge Cirri",
            "cards": ["Al-Ashrad, Amr of Alamut (ADV)"],
        },
    )
    assert response.json == [
        {
            "author": "Orpheus",
            "comments": (
                "Description: They make the best Kebab In Town !\n\n"
                "Yes, the Assamites belong in the Camarilla and they can vote "
                "better than most ! ^^\n"
                "I made many versions of this deck. It used to be Assamites only "
                "with Tegyrius merged also, but his absence of Obf is too "
                "dangerous in the current meta. So I mixed with some Malks and "
                "pumped up on the stealth.\n"
                "I should probably get back to 4 Al-Ashrad advanced in 13 vamps, "
                "or maybe in 12 if I really want Maris too.\n"
                "The reste of the deck worked liked a charm, maybe I could add a "
                "Telepathic Misdirection and / or an Eye of Argus, they can be "
                "cycled easily enough with Rebekah. I used to play Telepathic "
                "Vote Counting but with the locs I usually can pass or deal my votes.\n"
            ),
            "crypt": {
                "cards": [
                    {
                        "count": 3,
                        "id": 200036,
                        "name": "Al-Ashrad, Amr of Alamut (ADV)",
                    },
                    {"count": 1, "id": 200035, "name": "Al-Ashrad, Amr of Alamut"},
                    {"count": 2, "id": 200935, "name": "Maris Streck"},
                    {"count": 2, "id": 201170, "name": "Rebekah"},
                    {"count": 2, "id": 200422, "name": "Enam"},
                    {"count": 1, "id": 200538, "name": "Greger Anderssen"},
                    {"count": 1, "id": 201141, "name": "Quentin King III"},
                ],
                "count": 12,
            },
            "date": "2018-04-22",
            "event": "NCQ Villevaudé",
            "id": "2018ncqvvf",
            "library": {
                "cards": [
                    {
                        "cards": [
                            {"count": 1, "id": 100037, "name": "Alamut"},
                            {"count": 1, "id": 100172, "name": "The Black Throne"},
                            {"count": 2, "id": 100588, "name": "Dreams of the Sphinx"},
                            {
                                "count": 1,
                                "id": 100632,
                                "name": "Elysium: The Palace of " "Versailles",
                            },
                            {"count": 2, "id": 100984, "name": "Information Highway"},
                            {"count": 1, "id": 101238, "name": "Monastery of Shadows"},
                            {"count": 1, "id": 101384, "name": "Pentex™ Subversion"},
                            {"count": 6, "id": 102121, "name": "Villein"},
                            {"count": 2, "id": 102180, "name": "Wider View"},
                            {"count": 2, "id": 102207, "name": "Zillah's Valley"},
                        ],
                        "count": 19,
                        "type": "Master",
                    },
                    {
                        "cards": [{"count": 8, "id": 101085, "name": "Legacy"}],
                        "count": 8,
                        "type": "Action",
                    },
                    {
                        "cards": [
                            {"count": 1, "id": 100059, "name": "Anarchist Uprising"},
                            {"count": 1, "id": 100065, "name": "Ancilla Empowerment"},
                            {"count": 1, "id": 100570, "name": "Domain Challenge"},
                            {
                                "count": 6,
                                "id": 101056,
                                "name": "Kine Resources Contested",
                            },
                            {"count": 7, "id": 101353, "name": "Parity Shift"},
                        ],
                        "count": 16,
                        "type": "Political Action",
                    },
                    {
                        "cards": [
                            {"count": 2, "id": 100362, "name": "Cloak the Gathering"},
                            {"count": 2, "id": 100617, "name": "Elder Impersonation"},
                            {"count": 2, "id": 100687, "name": "Faceless Night"},
                            {"count": 2, "id": 100769, "name": "Forgotten Labyrinth"},
                            {"count": 5, "id": 101125, "name": "Lost in Crowds"},
                            {"count": 1, "id": 101318, "name": "Old Friends"},
                            {"count": 1, "id": 101857, "name": "Spying Mission"},
                        ],
                        "count": 15,
                        "type": "Action Modifier",
                    },
                    {
                        "cards": [
                            {"count": 2, "id": 101913, "name": "Swallowed by the Night"}
                        ],
                        "count": 2,
                        "type": "Action Modifier/Combat",
                    },
                    {
                        "cards": [
                            {"count": 4, "id": 100680, "name": "Eyes of Argus"},
                            {
                                "count": 6,
                                "id": 101949,
                                "name": "Telepathic Misdirection",
                            },
                        ],
                        "count": 10,
                        "type": "Reaction",
                    },
                    {
                        "cards": [{"count": 5, "id": 101292, "name": "No Trace"}],
                        "count": 5,
                        "type": "Combat",
                    },
                ],
                "count": 75,
            },
            "name": "Royal Kebab (sauce blanche)",
            "place": "Villevaudé, France",
            "player": "Serge Cirri",
            "players_count": 22,
            "score": "2gw9 + 1.5vp in the final",
            "tournament_format": "3R+F",
        },
    ]
    response = client.post(
        "/deck",
        json={
            "date_from": "2015-01-01",
            "date_to": "2020-01-01",
            "cards": ["Al-Ashrad, Amr of Alamut (ADV)"],
        },
    )
    assert len(response.json) == 1


def test_submit_ruling(client, monkeypatch):
    class SessionMock:
        called = False

        @classmethod
        def post(cls, *args, **kwargs):
            cls.called = True
            cls.args = args
            cls.kwargs = kwargs
            cls.ok = True
            cls.status_code = 201
            return cls

        @classmethod
        def json(cls):
            return {"response": "ok"}

    monkeypatch.setattr(requests, "session", lambda: SessionMock)
    response = client.post(
        "/submit-ruling/Arson", json={"text": "foo", "link": "http://example.com"}
    )
    assert response.status_code == 400
    response = client.post(
        "/submit-ruling/Arson", json={"text": "foo", "link": "http://www.vekn.net"}
    )
    assert response.status_code == 201
    assert response.json == {"response": "ok"}
    assert SessionMock.called
    assert SessionMock.auth == (None, None)
    assert SessionMock.args == (
        "https://api.github.com/repos/lionel-panhaleux/krcg/issues",
        '{"title": "Arson", "body": "- **text:** foo\\n- **link:** '
        'http://www.vekn.net"}',
    )
    assert SessionMock.kwargs == {}
    assert SessionMock.ok
