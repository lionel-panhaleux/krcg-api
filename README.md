# KRCG API

[![PyPI version](https://badge.fury.io/py/krcg-api.svg)](https://badge.fury.io/py/krcg-api)
[![Validation](https://github.com/lionel-panhaleux/krcg-api/actions/workflows/validation.yml/badge.svg)](https://github.com/lionel-panhaleux/krcg-api/actions/workflows/validation.yml)
[![Python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A web API for V:tES based on
the VEKN [official card texts](http://www.vekn.net/card-lists)
and the [Tournament Winning Deck Archive (TWDA)](http://www.vekn.fr/decks/twd.htm).

Portions of the materials are the copyrights and trademarks of Paradox Interactive AB,
and are used with permission. All rights reserved.
For more information please visit [white-wolf.com](http://www.white-wolf.com).

![Dark Pack](dark-pack.png)

## Online API and documentation

KRCG is a free to use (and documented) [online API](https://api.krcg.org/).
Anyone is free to use it, without warranty.

Breaking changes will only be introduced at major version upgrades,
after a proper deprecation period.

## Contribute

**Contributions are welcome !**

This API is an offspring of the [KRCG](https://github.com/lionel-panhaleux/krcg)
python package, so please refer to that repository for issues, discussions
and contributions guidelines.

Cards and decks are served in the
[KRCG v5](https://github.com/lionel-panhaleux/krcg) JSON format.

## Examples

Query a card by name or ID, get text, rulings, prints and image URL
(`prints` and `rulings` truncated here for brevity):

```bash
curl -X GET "http://127.0.0.1:8000/card/Alastor" -H  "accept: application/json"
```

```json
{
  "id": 100038,
  "printed_name": "Alastor",
  "kind": "Library",
  "types": ["Political Action"],
  "url": "https://static.krcg.org/card/alastor.jpg",
  "text": "Requires a justicar or Inner Circle member...",
  "legal": "2004-06-16",
  "artists": ["Monte Moore"],
  "prints": [
    {
      "set": { "id": 300012, "code": "Gehenna" },
      "occurrences": [{ "type": "Rarity", "frequency": "R", "multiplier": 1.0 }],
      "url": "https://static.krcg.org/card/set/gehenna/alastor.jpg"
    }
  ],
  "rulings": [
    {
      "text": "If the weapon retrieved costs blood, that cost is paid by the vampire chosen by the terms. [LSJ 20040518]",
      "reminder": false,
      "references": [
        {
          "text": "[LSJ 20040518]",
          "label": "LSJ 20040518",
          "url": "https://groups.google.com/g/rec.games.trading-cards.jyhad/c/4emymfUPwAM/m/B2SCC7L6kuMJ"
        }
      ]
    }
  ],
  "i18n": {},
  "variants": [],
  "cards": []
}
```

A card whose text names another card marks it in place with `<Card Name>`,
and lists the cards it names in `cards`:

```json
{
  "printed_name": "Villein",
  "text": "Trifle.\nPut this card on a vampire you control who has any amount of blood and move 2 to 5 blood from that vampire to your pool. Cards named <Minion Tap> cost you +1 pool to play. Villein costs +1 pool to play on this vampire.",
  "cards": [
    {
      "id": 101217,
      "printed_name": "Minion Tap",
      "unicity_suffix": "",
      "suffix": ""
    }
  ]
}
```

Every marker left in the text names a card listed in `cards`, so a client can
render them as links; strip the angle brackets to display the plain text.

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

Get candidates for your decklist out of the **TWDA**:

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

-   search decks in the TWDA, by cards, dates, author and number of players
-   deck list format conversion
-   retrieving a decklist from an Amaranth share URL
-   card name completions

Check the [online documentation](https://api.krcg.org/) for more.

### Hosting the web API

To host the web API, you can use uv or pip to install it:

```bash
uv pip install "krcg-api"
# or
pip install "krcg-api"
```

`krcg-api` is an ASGI application served by [uvicorn](https://www.uvicorn.org)
(installed as a dependency). The ASGI entrypoint is `krcg_api:application`:

```bash
uvicorn krcg_api:application --host 127.0.0.1 --port 8000
```

For production you can run several uvicorn workers behind a reverse proxy
(see [Deployment](#deployment) below).

The API loads all card and deck data in memory at startup (no database). It
needs no configuration nor environment variables.

#### Development

The development version uses [uv](https://github.com/astral-sh/uv) for package
management. Requires Python 3.12+.

```bash
$ just install
$ just serve
...
Uvicorn running on http://127.0.0.1:8000
```

You can check the API is running by using your browser
on the provided address [http://127.0.0.1:8000](http://127.0.0.1:8000).

`just test` runs the quality checks (ruff, ty) and the test suite. The tests
load the bundled card/deck snapshot, so they run offline; the deck-provider
tests (Amaranth, VDB, VTES Decks) reach external sites and skip when offline.

### Deployment

The API is deployed to a server with Ansible, reusing the shared roles from
[server-setup](https://github.com/lionel-panhaleux/server-setup). A systemd
service runs uvicorn on a local port and the `nginx_site` role fronts it with
nginx + Let's Encrypt. See [`deploy/README.md`](deploy/README.md) for details.

Deployment runs from GitHub Actions via `workflow_dispatch` and automatically
on every published release. The workflow ships in
[`deploy/ci/deploy.yml`](deploy/ci/deploy.yml) and must be moved under
`.github/workflows/` by a maintainer (see [`deploy/ci/README.md`](deploy/ci/README.md)).
