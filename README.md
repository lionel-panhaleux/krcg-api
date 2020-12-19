# KRCG API

A web API for V:tES based on
the VEKN [official card texts](http://www.vekn.net/card-lists)
and the [Tournament Winning Deck Archive (TWDA)](http://www.vekn.fr/decks/twd.htm).

Portions of the materials are the copyrights and trademarks of Paradox Interactive AB,
and are used with permission. All rights reserved.
For more information please visit [white-wolf.com](http://www.white-wolf.com).

![Dark Pack](dark-pack.png)

## Online API and documentation

KRCG is a free to use (and documented) [online API](https://api.v2.krcg.org/).
Anyone is free to use it, without warranty.

Breaking changes will only be introduced at major version upgrades,
after a proper deprecation period.

## Contribute

**Contributions are welcome !**

This API is an offspring of the [KRCG](https://github.com/lionel-panhaleux/krcg)
python package, so please refer to that repository for issues, discussions
and contributions guidelines.

## Examples

Query a card by name or ID, get text, rulings and image URL:

```bash
curl -X GET "http://127.0.0.1:8000/card/Alastor" -H  "accept: application/json"
```

```json
{
    "id": 100038,
    "name": "Alastor",
    "_name": "Alastor",
    "types": ["Political Action"],
    "url": "https://static.krcg.org/card/alastor.jpg",
    "card_text": "Requires a justicar or Inner Circle member...",
    "rulings": {
        "links": {
            "[ANK 20200901]": "http://www.vekn.net/forum/rules-questions/78830-alastor-and-ankara-citadel#100653",
            "[LSJ 20040518]": "https://groups.google.com/d/msg/rec.games.trading-cards.jyhad/4emymfUPwAM/B2SCC7L6kuMJ"
        },
        "text": [
            "If the given weapon costs blood, the target Alastor pays the cost. [LSJ 20040518]",
            "Requirements do not apply. [ANK 20200901]"
        ]
    },
    "artists": ["Monte Moore"],
    "sets": {
        "Gehenna": [{ "rarity": "Rare", "release_date": "2004-05-17" }],
        "Keepers of Tradition": [{ "rarity": "Rare", "release_date": "2008-11-19" }],
        "Kindred Most Wanted": [
            {
                "copies": 1,
                "precon": "Alastors",
                "release_date": "2005-02-21"
            }
        ]
    }
}
```

Search for cards by text, type, discipline, title, city, artist, set,
preconstructed starter, group, capacity, trait, sect, bonus values, etc.:

```bash
curl
    -X POST "http://127.0.0.1:8000/card_search"
    -H "Content-Type: application/json"
    -d "{\"type\":[\"political action\"],\"sect\":[\"anarch\"]}"
```

```json
[
    "Anarch Salon",
    "Eat the Rich",
    "Firebrand",
    "Free States Rant",
    "Patsy",
    "Reckless Agitation",
    "Revolutionary Council",
    "Sweeper"
]
```

Browse the **TWDA**: search for decks containing given cards,
get candidates for your decklist out of it:

```bash
curl
    -X POST "http://127.0.0.1:8000/candidates"
    -H  "Content-Type: application/json"
    -d "{\"cards\":[\"Cybele\",\"Nana Buruku\"]}"
```

```json
[
  {
    "average": 14,
    "card": "Ashur Tablets",
    "deviation": 6.25,
    "score": 1
  },
  {
    "average": 1,
    "card": "Giant's Blood",
    "deviation": 0,
    "score": 1
  },
  {
    "average": 2,
    "card": "The Parthenon",
    "deviation": 0.81,
    "score": 1
  },
  {
    "average": 1,
    "card": "Archon Investigation",
    "deviation": 0,
    "score": 0.9
  },
  ...
]
```

And a few other features, including:

-   deck list format conversion
-   retrieving a decklist from an Amaranth share URL
-   card name completions

Check the [online documentation](https://api.v2.krcg.org/) for more.
