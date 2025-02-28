def test(client):
    response = client.get("/card/NotACard")
    assert response.status_code == 404
    response = client.get("/card/Alastor")
    assert response.status_code == 200
    assert response.json == {
        "id": 100038,
        "_name": "Alastor",
        "_set": "Gehenna:R, KMW:PAl, KoT:R, 30th:1",
        "legality": "2004-05-17",
        "name": "Alastor",
        "printed_name": "Alastor",
        "url": "https://static.krcg.org/card/alastor.jpg",
        "types": ["Political Action"],
        "card_text": (
            "Requires a justicar or Inner Circle member.\n"
            "Choose a ready Camarilla vampire. Successful referendum means you "
            "search your library for an equipment card and put this card "
            "and the equipment on the chosen vampire (ignore requirements; "
            "shuffle afterward); pay half the cost rounded down of the equipment. "
            "The attached vampire can enter combat with a vampire "
            "as a +1 stealth Ⓓ action. "
            "The attached vampire cannot commit diablerie. A vampire can have only one Alastor."
        ),
        "sets": {
            "Gehenna": [{"rarity": "Rare", "release_date": "2004-05-17"}],
            "Keepers of Tradition": [{"rarity": "Rare", "release_date": "2008-11-19"}],
            "Kindred Most Wanted": [
                {"copies": 1, "precon": "Alastors", "release_date": "2005-02-21"}
            ],
            "Thirtieth Anniversary": [{"copies": 1, "release_date": "2024-07-20"}],
        },
        "ordered_sets": [
            "Gehenna",
            "Kindred Most Wanted",
            "Keepers of Tradition",
            "Thirtieth Anniversary",
        ],
        "scans": {
            "Gehenna": "https://static.krcg.org/card/set/gehenna/alastor.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/alastor.jpg"
            ),
            "Kindred Most Wanted": (
                "https://static.krcg.org/card/set/kindred-most-wanted/alastor.jpg"
            ),
            "Thirtieth Anniversary": (
                "https://static.krcg.org/card/set/thirtieth-anniversary/alastor.jpg"
            ),
        },
        "artists": ["Monte Moore"],
        "rulings": [
            {
                "references": [
                    {
                        "label": "LSJ 20040518",
                        "text": "[LSJ 20040518]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/4emymfUPwAM/m/B2SCC7L6kuMJ"
                        ),
                    },
                ],
                "text": "If the weapon retrieved costs blood, that cost is paid by the "
                "vampire chosen by the terms. [LSJ 20040518]",
            },
            {
                "cards": [
                    {
                        "id": 100989,
                        "name": "Inscription",
                        "text": "{Inscription}",
                        "usual_name": "Inscription",
                        "vekn_name": "Inscription",
                    },
                ],
                "references": [
                    {
                        "label": "ANK 20200901",
                        "text": "[ANK 20200901]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "78830-alastor-and-ankara-citadel#100653"
                        ),
                    },
                    {
                        "label": "LSJ 20040518-2",
                        "text": "[LSJ 20040518-2]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/4emymfUPwAM/m/JF_o7OOoCbkJ"
                        ),
                    },
                ],
                "text": "Requirements do not apply. If a discipline is required (eg. "
                "{Inscription}) and the Alastor vampire does not have it, the "
                "inferior version is used. [ANK 20200901] [LSJ 20040518-2]",
            },
            {
                "references": [
                    {
                        "label": "LSJ 20050331-2",
                        "text": "[LSJ 20050331-2]",
                        "url": "https://groups.google.com/g/rec.games.trading-cards.jyhad/c/NLFFYNok1Ns/m/n7mHhZ_oTRQJ",
                    },
                ],
                "text": "Finding equipment is optional. When no equipment is found, "
                "alastor is still attached. [LSJ 20050331-2]",
            },
        ],
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
        "legality": "1994-08-16",
        "name": "Aid from Bats",
        "printed_name": "Aid from Bats",
        "_name": "Aid from Bats",
        "_set": "Jyhad:C, VTES:C, CE:C/PN3, Anarchs:PG2, Third:C, KoT:C, FB:PN6",
        "rulings": [
            {
                "group": "Optional press",
                "references": [
                    {
                        "label": "TOM 19960521",
                        "text": "[TOM 19960521]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/poYD3n0TKGo/m/xvU5HW7lBxMJ"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "I",
                        "text": "[ANI]",
                    },
                ],
                "text": (
                    "[ANI]The optional press can only be used during the current "
                    "round. [TOM 19960521]"
                ),
            },
        ],
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
        "legality": "2017-05-11",
        "name": "The Line",
        "printed_name": "The Line",
        "name_variants": ["Line, The"],
        "_name": "Line, The",
        "_set": "Anthology:LARP1, SoB:1",
        "rulings": [
            {
                "references": [
                    {
                        "label": "ANK 20170605",
                        "text": "[ANK 20170605]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "75862-timing-of-the-line#82113"
                        ),
                    },
                    {
                        "label": "ANK 20230620",
                        "text": "[ANK 20230620]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "80612-when-to-use-shard-the-line-when-action-becoems-to"
                            "-expensive-after-announcement#108409"
                        ),
                    },
                ],
                "text": (
                    "Can be locked to reduce the cost at any point before resolution, "
                    "from when the action is announced to just before the cost is "
                    "paid. [ANK 20170605] [ANK 20230620]"
                ),
            },
            {
                "references": [
                    {
                        "label": "ANK 20181007",
                        "text": "[ANK 20181007]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "77057-quick-question-on-the-line#91020"
                        ),
                    },
                ],
                "text": (
                    "Can reduce the cost in blood (not in pool) of any action (ally, "
                    "retainer, equipment, political). [ANK 20181007]"
                ),
            },
            {
                "cards": [
                    {
                        "id": 101342,
                        "name": "Pack Alpha",
                        "text": "{Pack Alpha}",
                        "usual_name": "Pack Alpha",
                        "vekn_name": "Pack Alpha",
                    },
                ],
                "references": [
                    {
                        "label": "RTR 20070707",
                        "text": "[RTR 20070707]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/vSOt2c1uRzQ/m/MsRAv47Cd4YJ"
                        ),
                    },
                    {
                        "label": "ANK 20230824",
                        "text": "[ANK 20230824]",
                        "url": (
                            "https://www.vekn.net/forum/news-and-announcements/"
                            "80782-the-line-pack-alpha?start=6#109157"
                        ),
                    },
                ],
                "text": (
                    "Can reduce the cost of an action card even if it is not played as "
                    "an action (ie. a retainer played with {Pack Alpha}). [RTR "
                    "20070707] [ANK 20230824]"
                ),
            },
            {
                "references": [
                    {
                        "label": "ANK 20200605",
                        "text": "[ANK 20200605]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "78671-can-an-ally-with-play-as-a-vampire-use-the-line-"
                            "to-reduce-action-costs#100015"
                        ),
                    },
                ],
                "text": (
                    'Cannot be used by an ally acting "as a vampire". [ANK 20200605]'
                ),
            },
        ],
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
        "legality": "2015-02-16",
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
        "legality": "2014-10-04",
        "name": "Ophidian Gaze",
        "printed_name": "Ophidian Gaze",
        "_name": "Ophidian Gaze",
        "_set": "TU:C/B4",
        "rulings": [
            {
                "cards": [
                    {
                        "id": 102131,
                        "name": "Voter Captivation",
                        "text": "{Voter Captivation}",
                        "usual_name": "Voter Captivation",
                        "vekn_name": "Voter Captivation",
                    },
                    {
                        "id": 100788,
                        "name": "Freak Drive",
                        "text": "{Freak Drive}",
                        "usual_name": "Freak Drive",
                        "vekn_name": "Freak Drive",
                    },
                ],
                "references": [
                    {
                        "label": "ANK 20180909",
                        "text": "[ANK 20180909]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "76987-ophidian-gaze-and-post-referendum-action-"
                            "modifiers#90501"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                ],
                "text": (
                    '[SER][PRE] Can be used to cancel an action modifier player "after '
                    'the action/referendum is successful" (eg. {Voter Captivation} or '
                    "{Freak Drive}). [ANK 20180909]"
                ),
            },
            {
                "cards": [
                    {
                        "id": 100135,
                        "name": "The Barrens",
                        "text": "{The Barrens}",
                        "usual_name": "The Barrens",
                        "vekn_name": "Barrens, The",
                    },
                    {
                        "id": 100588,
                        "name": "Dreams of the Sphinx",
                        "text": "{Dreams of the Sphinx}",
                        "usual_name": "Dreams of the Sphinx",
                        "vekn_name": "Dreams of the Sphinx",
                    },
                ],
                "group": "Cancel",
                "references": [
                    {
                        "label": "LSJ 20061207",
                        "text": "[LSJ 20061207]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/nqcrJlhg4Ng/m/qQu7p-LLhfAJ"
                        ),
                    },
                    {
                        "label": "RBK playing-a-card",
                        "text": "[RBK playing-a-card]",
                        "url": "https://www.vekn.net/rulebook#playing-a-card",
                    },
                    {
                        "label": "LSJ 20061013",
                        "text": "[LSJ 20061013]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/6w8K3yDtBH0/m/M_SZH9Id8n8J"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                ],
                "text": (
                    '[PRE][SER]Cards are not replaced during the "as played" window. '
                    "The cancelation must be played immediately: no other effects can "
                    "be used, except for wakes (eg. neither\xa0{The Barrens}\xa0nor "
                    "{Dreams of the Sphinx}\xa0can be used). [LSJ 20061207] [RBK "
                    "playing-a-card] [LSJ 20061013]"
                ),
            },
            {
                "cards": [
                    {
                        "id": 101869,
                        "name": "Steely Tenacity",
                        "text": "{Steely Tenacity}",
                        "usual_name": "Steely Tenacity",
                        "vekn_name": "Steely Tenacity",
                    },
                ],
                "group": "Cancel",
                "references": [
                    {
                        "label": "LSJ 20080630",
                        "text": "[LSJ 20080630]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/nvuXBpEaKAA/m/ymiC3yAQVOwJ"
                        ),
                    },
                    {
                        "label": "LSJ 20011023",
                        "text": "[LSJ 20011023]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/2GOLIrXAF8M/m/P4T3Dj6UNL0J"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                ],
                "text": '[PRE][SER]If the canceled card had a "do not replace until" '
                "clause (or alternate replacement like {Steely Tenacity}), that "
                "clause is canceled as well and the card is replaced normally. "
                "[LSJ 20080630] [LSJ 20011023]",
            },
            {
                "group": "Cancel",
                "references": [
                    {
                        "label": "ANK 20190104",
                        "text": "[ANK 20190104]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "77254-canceling-cards-and-bold-text?start=6#92640"
                        ),
                    },
                    {
                        "label": "RBK cancel-a-card",
                        "text": "[RBK cancel-a-card]",
                        "url": "https://www.vekn.net/rulebook#cancel-a-card",
                    },
                    {
                        "label": "LSJ 19980212",
                        "text": "[LSJ 19980212]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/fLFLlXZXHqA/m/ggjw8aGjdRoJ"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                ],
                "text": (
                    "[PRE][SER]The canceled card has still been played. The same "
                    "reaction or modifier cannot be played again by the same minion. "
                    "Any card which text prohibits to play more than once cannot be "
                    "played again. [ANK 20190104] [RBK cancel-a-card] [LSJ 19980212]"
                ),
            },
            {
                "group": "Cancel",
                "references": [
                    {
                        "label": "LSJ 20030224",
                        "text": "[LSJ 20030224]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/67261v339Ds/m/um8V7VVp2Y4J"
                        ),
                    },
                ],
                "symbols": [
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                ],
                "text": "[PRE][SER]If a limited effect is canceled (bleed, additional "
                "strike), then the limit is not triggered and another limited "
                "effect can be used. [LSJ 20030224]",
            },
            {
                "group": "Cancel as a reaction",
                "references": [
                    {
                        "label": "LSJ 20021011",
                        "text": "[LSJ 20021011]",
                        "url": "https://groups.google.com/g/rec.games.trading-cards.jyhad/c/9WWIzxek9Nc/m/PlIwI11sNpkJ",
                    },
                ],
                "symbols": [
                    {
                        "symbol": "R",
                        "text": "[PRE]",
                    },
                    {
                        "symbol": "S",
                        "text": "[SER]",
                    },
                ],
                "text": "[PRE][SER]Cancelation must be immediate: a wake can be used in "
                'the "as played" window, but a reaction to "unlock and attempt to '
                'block" cannot. [LSJ 20021011]',
            },
        ],
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
        "legality": "2002-08-19",
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
        "legality": "2008-11-19",
        "name": "Ashur Tablets",
        "printed_name": "Ashur Tablets",
        "_name": "Ashur Tablets",
        "_set": "KoT:C, Anthology:3, Promo:202401011",
        "rulings": [
            {
                "references": [
                    {
                        "label": "PIB 20130119",
                        "text": "[PIB 20130119]",
                        "url": (
                            "https://www.vekn.net/forum/rules-questions/"
                            "44197-ashur-tablets-for-zero#44229"
                        ),
                    },
                ],
                "text": "Can be played with no card in the ash heap. [PIB 20130119]",
            },
            {
                "references": [
                    {
                        "label": "LSJ 20091030",
                        "text": "[LSJ 20091030]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/ZKuCyTayYbc/m/5nMjLpX4DuMJ"
                        ),
                    },
                ],
                "text": (
                    "Is played without announcing targets: they are only chosen once "
                    "the third copy get into play. [LSJ 20091030]"
                ),
            },
            {
                "references": [
                    {
                        "label": "LSJ 20081129",
                        "text": "[LSJ 20081129]",
                        "url": (
                            "https://groups.google.com/g/rec.games.trading-cards.jyhad/"
                            "c/7fMPCYIPrag/m/_gGD-1da2N8J"
                        ),
                    },
                ],
                "text": "You must show which one goes in hand. [LSJ 20081129]",
            },
        ],
        "sets": {
            "Anthology": [{"copies": 3, "release_date": "2017-05-11"}],
            "Keepers of Tradition": [
                {"rarity": "Common", "release_date": "2008-11-19"}
            ],
            "Promo": [{"copies": 1, "release_date": "2024-01-01"}],
        },
        "ordered_sets": ["Keepers of Tradition", "Anthology"],
        "scans": {
            "Anthology": "https://static.krcg.org/card/set/anthology/ashurtablets.jpg",
            "Keepers of Tradition": (
                "https://static.krcg.org/card/set/keepers-of-tradition/ashurtablets.jpg"
            ),
            "Promo": "https://static.krcg.org/card/set/promo/ashurtablets.jpg",
        },
        "types": ["Master"],
    }
