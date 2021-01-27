def test(client):
    response = client.post("/twda")
    assert response.status_code == 200
    assert len(response.json) >= 3125
    # since Anthelios is banned, this number should stay stable
    response = client.post("/twda", json={"cards": ["Anthelios, The Red Star"]})
    assert response.status_code == 200
    assert len(response.json) == 320
    response = client.post("/twda", json={"cards": ["Not a Card"]})
    assert response.status_code == 400
    response = client.post("/twda", json={"cards": ["Madness of the Bard"]})
    assert response.status_code == 404
    response = client.post("/twda", json={"cards": [""]})
    # test deck parsing and serialization - it has both general and cards comments
    response = client.get("/twda/2020bf3hf")
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


def test_search(client):
    response = client.post(
        "/twda",
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
        "/twda",
        json={
            "date_from": "2015-01-01",
            "date_to": "2020-01-01",
            "cards": ["Al-Ashrad, Amr of Alamut (ADV)"],
        },
    )
    assert len(response.json) == 1
    response = client.post(
        "/twda",
        json={
            "date_from": "2015-01-01",
            "date_to": "2020-01-01",
            "players_count": 22,
            "cards": ["Al-Ashrad, Amr of Alamut (ADV)"],
        },
    )
    assert len(response.json) == 1
    response = client.post(
        "/twda",
        json={
            "date_from": "2015-01-01",
            "date_to": "2020-01-01",
            "players_count": 23,
            "cards": ["Al-Ashrad, Amr of Alamut (ADV)"],
        },
    )
    assert response.status_code == 404
