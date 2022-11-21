def test(client):
    first_blood_tremere = {
        "id": "b798e734fff7404085f7b01ad2ccb479",
        "date": "2021-01-11",
        "author": "BCP",
        "name": "First Blood Tremere",
        "comments": (
            "https://blackchantry.com/"
            "How%20to%20play%20the%20First%20Blood%20Tremere%20deck.pdf"
        ),
        "crypt": {
            "cards": [
                {"count": 2, "id": 200025, "name": "Aidan Lyle"},
                {"count": 2, "id": 200280, "name": "Claus Wegener"},
                {"count": 2, "id": 201020, "name": "Muhsin Samir"},
                {"count": 2, "id": 201213, "name": "Rutor"},
                {"count": 2, "id": 201388, "name": "Troius"},
                {"count": 2, "id": 201501, "name": "Zane"},
            ],
            "count": 12,
        },
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
        "/vdb",
        data={"url": "https://vdb.im/decks?id=b798e734fff7404085f7b01ad2ccb479"},
    )
    assert response.status_code == 200
    assert response.json == first_blood_tremere
    response = client.post(
        "/vdb",
        json={"url": "https://vdb.im/decks/b798e734fff7404085f7b01ad2ccb479"},
    )
    assert response.status_code == 200
    assert response.json == first_blood_tremere
