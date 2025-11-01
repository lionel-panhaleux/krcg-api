def test(client):
    deck_json = {
        "date": "2020-01-01",
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
                            "name": "FBI Special Affairs Division",
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
    deck_text = """January 1st 2020

Crypt (12 cards, min=7, max=24, avg=3.75)
-----------------------------------------
1x Gilbert Duane          7 AUS DOM OBF      prince  Malkavian:1
1x Mariel, Lady Thunder   7 DOM OBF aus tha          Malkavian:1
1x Badr al-Budur          5 OBF cel dom qui          Banu Haqim:2
1x Count Ormonde          5 OBF dom pre ser          Ministry:2
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
    response = client.post("/convert/lackey", data=deck_text, content_type="text/plain")
    assert response.status_code == 200
    assert response.data == (
        b"1\tChannel 10\n"
        b"2\tCharisma\n"
        b"1\tCreepshow Casino\n"
        b"1\tKRCG News Radio\n"
        b"2\tPerfectionist\n"
        b"6\tStorage Annex\n"
        b"3\tSudden Reversal\n"
        b"3\tVessel\n"
        b"1\tCarlton Van Wyk\n"
        b"1\tGregory Winter\n"
        b"1\tImpundulu\n"
        b"1\tMuddled Vampire Hunter\n"
        b"1\tOssian\n"
        b"6\tProcurer\n"
        b"1\tYoung Bloods\n"
        b"1\tDeer Rifle\n"
        b"8\tFlash Grenade\n"
        b"6\tCloak the Gathering\n"
        b"7\tConditioning\n"
        b"2\tLost in Crowds\n"
        b"4\tVeil the Legions\n"
        b"7\tDeflection\n"
        b"2\tDelaying Tactics\n"
        b"7\tOn the Qui Vive\n"
        b"8\tConcealed Weapon\n"
        b"1\tFBI Special Affairs Division\n"
        b"1\tHunger Moon\n"
        b"1\tRestricted Vitae\n"
        b"1\tUnmasking, The\n"
        b"Crypt:\n"
        b"1\tGilbert Duane\n"
        b"1\tMariel, Lady Thunder\n"
        b"1\tBadr al-Budur\n"
        b"1\tCount Ormonde\n"
        b"1\tDidi Meyers\n"
        b"1\tZebulon\n"
        b"1\tDimple\n"
        b"1\tMustafa Rahman\n"
        b"1\tNormal\n"
        b"1\tOhanna\n"
        b"1\tSamson\n"
        b"1\tBasil"
    )
    response = client.post("/convert/jol", data=deck_text, content_type="text/plain")
    assert response.status_code == 200
    assert response.data == (
        b"1x Gilbert Duane\n"
        b"1x Mariel, Lady Thunder\n"
        b"1x Badr al-Budur\n"
        b"1x Count Ormonde\n"
        b"1x Didi Meyers\n"
        b"1x Zebulon\n"
        b"1x Dimple\n"
        b"1x Mustafa Rahman\n"
        b"1x Normal\n"
        b"1x Ohanna\n"
        b"1x Samson\n"
        b"1x Basil\n"
        b"\n"
        b"1x Channel 10\n"
        b"2x Charisma\n"
        b"1x Creepshow Casino\n"
        b"1x KRCG News Radio\n"
        b"2x Perfectionist\n"
        b"6x Storage Annex\n"
        b"3x Sudden Reversal\n"
        b"3x Vessel\n"
        b"1x Carlton Van Wyk\n"
        b"1x Gregory Winter\n"
        b"1x Impundulu\n"
        b"1x Muddled Vampire Hunter\n"
        b"1x Ossian\n"
        b"6x Procurer\n"
        b"1x Young Bloods\n"
        b"1x Deer Rifle\n"
        b"8x Flash Grenade\n"
        b"6x Cloak the Gathering\n"
        b"7x Conditioning\n"
        b"2x Lost in Crowds\n"
        b"4x Veil the Legions\n"
        b"7x Deflection\n"
        b"2x Delaying Tactics\n"
        b"7x On the Qui Vive\n"
        b"8x Concealed Weapon\n"
        b"1x FBI Special Affairs Division\n"
        b"1x Hunger Moon\n"
        b"1x Restricted Vitae\n"
        b"1x Unmasking, The"
    )
    response = client.post("/convert/twd", data=deck_text, content_type="text/plain")
    assert response.status_code == 200
    assert response.data == deck_text.encode("utf-8")
    response = client.post("/convert/json", data=deck_text, content_type="text/plain")
    assert response.status_code == 200
    assert response.json == deck_json
    response = client.post("/convert", data=deck_text, content_type="text/plain")
    assert response.status_code == 200
    assert response.json == deck_json
    response = client.post("/convert/twd", json=deck_json)
    assert response.status_code == 200
    assert response.data == deck_text.encode("utf-8")
