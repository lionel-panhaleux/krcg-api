def test(client):
    response = client.get("/card/NotACard")
    assert response.status_code == 404
    response = client.get("/card/Alastor")
    assert response.status_code == 200
    assert response.json == {
        "id": 100038,
        "_name": "Alastor",
        "_set": "Gehenna:R, KMW:PAl, KoT:R",
        "name": "Alastor",
        "printed_name": "Alastor",
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
        "ordered_sets": ["Gehenna", "Kindred Most Wanted", "Keepers of Tradition"],
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
                "[LSJ 20040518-2]": (
                    "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                    "c/4emymfUPwAM/m/JF_o7OOoCbkJ"
                ),
            },
            "text": [
                (
                    "If the weapon retrieved costs blood, that cost is paid "
                    "by the vampire chosen by the vote. [LSJ 20040518]"
                ),
                (
                    "Requirements do not apply. If a discipline is required "
                    "(eg. {Inscription}) and the Alastor vampire does not have it, the "
                    "inferior version is used. [ANK 20200901] [LSJ 20040518-2]"
                ),
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
        "artists": ["Melissa Benson", "Eric Lofgren"],
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
        "printed_name": "Aid from Bats",
        "_name": "Aid from Bats",
        "_set": "Jyhad:C, VTES:C, CE:C/PN3, Anarchs:PG2, Third:C, KoT:C, FB:PN6",
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
        "ordered_sets": [
            "Jyhad",
            "Vampire: The Eternal Struggle",
            "Camarilla Edition",
            "Anarchs",
            "Third Edition",
            "Keepers of Tradition",
            "First Blood",
        ],
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
            "You can lock this location to reduce the cost of an action card a vampire "
            "you control plays by 1 blood (this location is not locked if that "
            "card is canceled as it is played). Vampires can steal this "
            "location as a Ⓓ action."
        ),
        "id": 101110,
        "url": "https://static.krcg.org/card/linethe.jpg",
        "name": "The Line",
        "printed_name": "The Line",
        "name_variants": ["Line, The"],
        "_name": "Line, The",
        "_set": "Anthology:LARP1, SoB:1",
        "rulings": {
            "text": [
                (
                    "Can be locked to reduce the cost at any point before resolution, "
                    "from when the action is announced to just before the cost is "
                    "paid. [ANK 20170605] [ANK 20230620]"
                ),
                (
                    "Can reduce the cost in blood (not in pool) of any action (ally, "
                    "retainer, equipment, political). [ANK 20181007]"
                ),
                (
                    "Can reduce the cost of an action card even if it is not played as "
                    "an action (ie. a retainer played with {Pack Alpha}). "
                    "[RTR 20070707] [ANK 20230824]"
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
                "[ANK 20230620]": (
                    "https://www.vekn.net/forum/rules-questions/"
                    "80612-when-to-use-shard-the-line-when-action-becoems-"
                    "to-expensive-after-announcement#108409"
                ),
                "[ANK 20230824]": (
                    "https://www.vekn.net/forum/news-and-announcements/"
                    "80782-the-line-pack-alpha?start=6#109157"
                ),
                "[RTR 20070707]": (
                    "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/"
                    "vSOt2c1uRzQ/MsRAv47Cd4YJ"
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
            ],
            "Shadows of Berlin": [
                {
                    "copies": 1,
                    "release_date": "2023-06-30",
                },
            ],
        },
        "ordered_sets": ["Anthology", "Shadows of Berlin"],
        "scans": {
            "Anthology": "https://static.krcg.org/card/set/anthology/linethe.jpg",
            "Shadows of Berlin": (
                "https://static.krcg.org/card/set/shadows-of-berlin/linethe.jpg"
            ),
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
            "-1 blood. He inflicts +1 damage or steals 1 additional "
            "blood or life with ranged strikes (even at close range). Flight "
            "[FLIGHT]. +1 bleed. +2 strength."
        ),
        "clans": ["Tzimisce"],
        "disciplines": ["ANI", "AUS", "POT", "THA", "VIC"],
        "group": "5",
        "id": 200385,
        "url": "https://static.krcg.org/card/dracontheg5.jpg",
        "name": "The Dracon (G5)",
        "printed_name": "The Dracon",
        "name_variants": [
            "Dracon, The (G5)",
            "The Dracon",
            "Dracon, The",
        ],
        "_name": "Dracon, The",
        "_set": "Promo-20150216, Promo-20181004:HB2, Promo-20190408, POD:DTC",
        "sets": {
            "2015 Storyline Rewards": [{"copies": 1, "release_date": "2015-02-16"}],
            "2018 Humble Bundle": [
                {"copies": 2, "precon": "Humble Bundle", "release_date": "2018-10-04"}
            ],
            "2019 Promo Pack 1": [{"copies": 1, "release_date": "2019-04-08"}],
            "Print on Demand": [{"copies": 1, "precon": "DriveThruCards"}],
        },
        "ordered_sets": [
            "2015 Storyline Rewards",
            "2018 Humble Bundle",
            "2019 Promo Pack 1",
        ],
        "scans": {
            "2015 Storyline Rewards": (
                "https://static.krcg.org/card/set/promo/dracontheg5.jpg"
            ),
            "2018 Humble Bundle": (
                "https://static.krcg.org/card/set/humble-bundle/dracontheg5.jpg"
            ),
            "2019 Promo Pack 1": (
                "https://static.krcg.org/card/set/promo-pack-1/dracontheg5.jpg"
            ),
            "Print on Demand": (
                "https://static.krcg.org/card/set/print-on-demand/dracontheg5.jpg"
            ),
        },
        "text_change": True,
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
            "declined. Cancel an action modifier card as it is played, and its cost is "
            "not paid."
        ),
        "disciplines": ["pre", "ser"],
        "combo": True,
        "id": 101325,
        "url": "https://static.krcg.org/card/ophidiangaze.jpg",
        "name": "Ophidian Gaze",
        "printed_name": "Ophidian Gaze",
        "_name": "Ophidian Gaze",
        "_set": "TU:C/B4",
        "rulings": {
            "text": [
                (
                    "[SER][PRE] Can be used to cancel an action modifier player "
                    '"after the action/referendum is successful" (eg. {Voter '
                    "Captivation} or {Freak Drive}). [ANK 20180909]"
                ),
                (
                    '[SER][PRE] Cards are not replaced during the "as '
                    'played" window. [LSJ 20061013]'
                ),
                (
                    '[SER][PRE] If the canceled card had a "Do Not Replace '
                    'Until" clause on it, that clause is canceled as well '
                    "and the card is replaced normally. [LSJ 20011023]"
                ),
            ],
            "links": {
                "[ANK 20180909]": (
                    "http://www.vekn.net/forum/rules-questions/"
                    "76987-ophidian-gaze-and-post-referendum-action-modifiers#90501"
                ),
                "[LSJ 20011023]": (
                    "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/"
                    "2GOLIrXAF8M/P4T3Dj6UNL0J"
                ),
                "[LSJ 20061013]": (
                    "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                    "c/6w8K3yDtBH0/m/M_SZH9Id8n8J"
                ),
            },
        },
        "sets": {
            "The Unaligned": [
                {"rarity": "Common", "release_date": "2014-10-04"},
                {"copies": 4, "precon": "Bundle 2", "release_date": "2021-07-09"},
            ]
        },
        "ordered_sets": ["The Unaligned"],
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
        "url": "https://static.krcg.org/card/tylerg3.jpg",
        "name": "Tyler (G3)",
        "printed_name": "Tyler",
        "name_variants": ["Tyler"],
        "_name": "Tyler",
        "_set": "CE:V, BSC:X",
        "sets": {
            "Blood Shadowed Court": [{"release_date": "2008-04-14"}],
            "Camarilla Edition": [{"rarity": "Vampire", "release_date": "2002-08-19"}],
        },
        "ordered_sets": ["Camarilla Edition", "Blood Shadowed Court"],
        "scans": {
            "Blood Shadowed Court": (
                "https://static.krcg.org/card/set/blood-shadowed-court/tylerg3.jpg"
            ),
            "Camarilla Edition": (
                "https://static.krcg.org/card/set/camarilla-edition/tylerg3.jpg"
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
            "Sandra Chang-Adair",
            "Ginés Quiñonero-Santiago",
        ],
        "card_text": (
            "Only one Ashur Tablets can be played each turn.\n"
            "Put this card in play. If you control three copies of this card, "
            "remove all copies in play (even controlled by other Methuselahs) from the "
            "game to gain 3 pool and choose up to thirteen library cards "
            "from your ash heap; move one of the chosen cards to your hand "
            "and shuffle the others into your library."
        ),
        "id": 100106,
        "url": "https://static.krcg.org/card/ashurtablets.jpg",
        "name": "Ashur Tablets",
        "printed_name": "Ashur Tablets",
        "_name": "Ashur Tablets",
        "_set": "KoT:C, Anthology:3",
        "rulings": {
            "text": [
                "Can be played with no card in the ash heap. [PIB 20130119]",
                "Is played without announcing targets: they are only chosen once "
                "the third copy get into play. [LSJ 20091030]",
                "You must show which one goes in hand. [LSJ 20081129]",
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
                "[LSJ 20081129]": (
                    "https://groups.google.com/g/rec.games.trading-cards.jyhad"
                    "/c/7fMPCYIPrag/m/_gGD-1da2N8J"
                ),
            },
        },
        "sets": {
            "Anthology": [{"copies": 3, "release_date": "2017-05-11"}],
            "Keepers of Tradition": [
                {"rarity": "Common", "release_date": "2008-11-19"}
            ],
        },
        "ordered_sets": ["Keepers of Tradition", "Anthology"],
        "scans": {
            "Anthology": "https://static.krcg.org/card/set/anthology/ashurtablets.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/ashurtablets.jpg"
            ),
        },
        "types": ["Master"],
    }
