def test_dimensions(client):
    response = client.get("/card_search")
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
            "Brian Graupner",
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
            "Christian Byrne",
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
            "Esther Sanz",
            "Felipe Gaona",
            "Francesc Grimalt",
            "Francisco Tébar",
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
            "Helena García Huang",
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
            "Jer Carolina",
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
            "Kamilla Khaminskaya",
            "Kari Christensen",
            "Karl Waller",
            "Katie McCaskill",
            "Kelly Howlett",
            "Ken Meyer, Jr.",
            "Kent Williams",
            "Kevin McCann",
            "Kieran Yanner",
            "Kim Aldau",
            "Krasen Maximov",
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
            "Marta Ruiz Anguera",
            "Martín de Diego",
            "María Lorén",
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
            "Peter Scholtz",
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
            "Algiers",
            "Amsterdam",
            "Aragon",
            "Athens",
            "Atlanta",
            "Barcelona",
            "Belo Horizonte",
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
            "Johannesburg",
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
            "Mombasa",
            "Monaco",
            "Montreal",
            "Moscow",
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
            "Tampa",
            "Thessaloniki",
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
            "Banu Haqim",
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
            "Ministry",
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
            "viz",
        ],
        "group": [1, 2, 3, 4, 5, 6, 7],
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
            "Fifth Edition (Anarch): Banu Haqim",
            "Fifth Edition (Anarch): Brujah",
            "Fifth Edition (Anarch): Gangrel",
            "Fifth Edition (Anarch): Ministry",
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
            "The Unaligned: Bundle 1",
            "The Unaligned: Bundle 2",
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
            "2021 Kickstarter Promo",
            "2021 Mind’s Eye Theatre Promo",
            "2021 Promo Pack 3",
            "2021 Resellers Promo",
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
            "Fifth Edition (Anarch)",
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


def test(client):
    response = client.post("/card_search")
    assert response.status_code == 200
    assert len(response.json) >= 3788
    # invalid dimension raise a 422
    response = client.post("/card_search", json={"foo": ["bar"]})
    assert response.status_code == 400
    assert response.json is None
    assert response.data == (
        b"Invalid search dimension: foo. Valid dimensions are: name, card_text"
        b", flavor_text, type, sect, clan, title, city, trait, group,"
        b" capacity, discipline, artist, set, rarity, precon, bonus, "
        b"text"
    )
    # non-existing values do not crash
    response = client.post("/card_search", json={"bonus": ["foo"]})
    assert response.status_code == 200
    assert response.json == []
    response = client.post("/card_search", json={"trait": ["foo"]})
    assert response.status_code == 200
    assert response.json == []


def test_card_text(client):
    response = client.post(
        "/card_search", json={"text": "this equipment card represents a location"}
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


def test_traits(client):
    # discipline, title
    response = client.post(
        "/card_search", json={"title": ["primogen"], "discipline": ["ser"]}
    )
    assert response.json == ["Amenophobis"]
    # city title
    response = client.post("/card_search", json={"city": ["chicago"]})
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
    response = client.post("/card_search", json={"bonus": ["stealth", "votes"]})
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
        "/card_search",
        json={"bonus": ["votes"], "clan": ["Assamite"], "type": ["Master"]},
    )
    assert response.json == ["Alamut", "The Black Throne"]
    # votes provided by titles
    response = client.post(
        "/card_search",
        json={"bonus": ["votes"], "clan": ["Assamite"], "group": [3]},
    )
    assert response.json == ["Enam", "Rebekah"]
    # title when MERGED
    response = client.post(
        "/card_search", json={"clan": ["Assamite"], "title": ["justicar"]}
    )
    assert response.json == ["Kasim Bayar", "Tegyrius, Vizier (ADV)"]
    # traits: black hand
    response = client.post(
        "/card_search",
        json={"clan": ["Nagaraja"], "trait": ["black hand"]},
    )
    assert response.json == ["Sennadurek"]
    # traits: red list
    response = client.post(
        "/card_search", json={"clan": ["Assamite"], "trait": ["red list"]}
    )
    assert response.json == ["Jamal", "Tariq, The Silent (ADV)"]
    # sect
    response = client.post(
        "/card_search",
        json={"clan": ["assamite"], "sect": ["camarilla"], "group": [2]},
    )
    assert response.json == [
        "Al-Ashrad, Amr of Alamut (ADV)",
        "Tegyrius, Vizier (ADV)",
        "Tegyrius, Vizier",
    ]
    # traits on library cards
    response = client.post(
        "/card_search",
        json={"type": ["action modifier"], "trait": ["black hand"]},
    )
    assert response.json == [
        "Circumspect Revelation",
        "Seraph's Second",
        "The Art of Memory",
    ]


def test_full(client):
    # return full card info
    response = client.post(
        "/card_search",
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
            "url": "https://static.krcg.org/card/sennadurekg4.jpg",
            "_name": "Sennadurek",
            "name": "Sennadurek (G4)",
            "name_variants": ["Sennadurek"],
            "printed_name": "Sennadurek",
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
                    {"rarity": "Uncommon", "release_date": "2005-11-14"}
                ]
            },
            "scans": {
                "Legacies of Blood": (
                    "https://static.krcg.org/card/set/legacies-of-blood/"
                    "sennadurekg4.jpg"
                ),
            },
            "types": ["Vampire"],
        }
    ]


def test_requirements(client):
    # required title
    response = client.post(
        "/card_search", json={"type": ["reaction"], "title": ["justicar"]}
    )
    assert response.json == ["Legacy of Power", "Second Tradition: Domain"]
    # "Requires titled Sabbat/Camarilla" maps to all possible titles
    response = client.post(
        "/card_search",
        json={"bonus": ["intercept"], "title": ["archbishop"]},
    )
    assert response.json == [
        "Matteus, Flesh Sculptor",
        "National Guard Support",
        "Persona Non Grata",
        "Under Siege",
    ]


def test_stealth_intercept(client):
    # Reducing intercept is stealth
    response = client.post(
        "/card_search",
        json={"bonus": ["stealth"], "discipline": ["chi"], "type": ["library"]},
    )
    assert response.json == [
        "Fata Morgana",
        "Heart's Desire",
        "Mirror's Visage",
        "Smoke and Mirrors",
        "Will-o'-the-Wisp",
    ]
    # Reducing stealth is intercept
    response = client.post(
        "/card_search",
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


def test_discipline(client):
    # no discipline (crypt)
    response = client.post(
        "/card_search", json={"discipline": ["none"], "type": ["crypt"]}
    )
    assert response.json == [
        "Anarch Convert",
        "Sandra White",
        "Smudge the Ignored",
    ]
    response = client.post(
        "/card_search",
        json={"discipline": ["none"], "bonus": ["intercept"], "sect": ["sabbat"]},
    )
    # no discipline, sect (or independent) required
    assert response.json == ["Abbot", "Harzomatuili", "Under Siege"]
    response = client.post(
        "/card_search",
        json={"type": ["political action"], "sect": ["independent"]},
    )
    assert response.json == ["Free States Rant", "Reckless Agitation"]
    response = client.post(
        "/card_search",
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
        "/card_search",
        json={"discipline": ["multi", "ani"], "bonus": ["intercept"]},
    )
    assert response.json == [
        "Deep Ecology",
        "Detect Authority",
        "Falcon's Eye",
        "Read the Winds",
        "Speak with Spirits",
        "The Mole",
    ]
    # superior disciplines (vampires only)
    response = client.post("/card_search", json={"discipline": ["OBE"], "group": [2]})
    assert response.json == ["Blanche Hill", "Matthias"]
    # Gwen Brand special case, disciplines abbreviations
    response = client.post(
        "/card_search",
        json={
            "clan": ["ravnos"],
            "group": [5],
            "discipline": ["AUS", "CHI", "FOR", "ANI"],
        },
    )
    assert response.json == ["Gwen Brand"]


def test_i18n(client):
    # i18n - still always perform text search in english
    response = client.post(
        "/card_search",
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
        "/card_search",
        json={"text": "Ankara"},
    )
    assert response.json == ["The Ankara Citadel, Turkey"]
    # i18n - but match the given language in addition to it
    response = client.post(
        "/card_search",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - should work with regions too, whatever their case
    response = client.post(
        "/card_search",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr-fr"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - should work with regions too, whatever their case
    response = client.post(
        "/card_search",
        json={"text": "cette carte d'équipement représente un lieu", "lang": "fr_FR"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]
    # i18n - do not match unrelated translations
    response = client.post(
        "/card_search",
        json={"text": "esta carta de equipo representa un lugar", "lang": "fr"},
    )
    assert response.json == []
    response = client.post(
        "/card_search",
        json={"text": "esta carta de equipo representa un lugar", "lang": "es"},
    )
    assert response.json == ["Living Manse", "The Ankara Citadel, Turkey"]


def test_artist(client):
    response = client.post("/card_search", json={"artist": ["E.M. Gist"]})
    assert response.json == [
        "Flames of Insurrection",
        "Harmony",
        "Marcus Vitel",
        "Public Enemy",
        "Rutor",
    ]
