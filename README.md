# KRCG API

[![PyPI version](https://badge.fury.io/py/krcg-api.svg)](https://badge.fury.io/py/krcg-api)
[![Validation](https://github.com/lionel-panhaleux/krcg-api/workflows/Validation/badge.svg)](https://github.com/lionel-panhaleux/krcg-api/actions)
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
    },
    "scans": {
        "Gehenna": "https://static.krcg.org/card/set/gehenna/alastor.jpg",
        "Keepers of Tradition": "https://static.krcg.org/card/set/keepers-of-tradition/alastor.jpg",
        "Kindred Most Wanted": "https://static.krcg.org/card/set/kindred-most-wanted/alastor.jpg"
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

Check the [online documentation](https://api.v2.krcg.org/) for more.

### Hosting the web API

To host the web API, you can use pip to install it:

```bash
pip install "krcg-api"
```

No wsgi server is installed by default, you need to install one.
HTTP web servers can then easily be configured to serve WSGI applications,
check the documentation of your web server.

The API can be served with [uWSGI](https://uwsgi-docs.readthedocs.io):

```bash
uwsgi --module krcg_api.wsgi:application
```

or [Gunicorn](https://gunicorn.org):

```bash
gunicorn krcg_api.wsgi:application
```

Two environment variables are expected: `GITHUB_USERNAME` and `GITHUB_TOKEN`,
to allow the API to connect to Github as a user in order to post new rulings
as issues on the repository (`/submit-ruling` endpoint).

See the [Github help](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
on how to generate a personal token for the account you want KRCG to use.

#### Development

The development version of KRCG installs uWSGI to serve the API,
this is the preferred WSGI server for now.

```bash
$ pip install -e ".[dev]"
$ make serve
...
uwsgi socket 0 bound to TCP address 127.0.0.1:8000
```

You can check the API is running by using your browser
on the provided address [http://127.0.0.1:8000](http://127.0.0.1:8000).

The environment variables `GITHUB_USERNAME` and `GITHUB_TOKEN` can be provided
by a personal `.env` file at the root of the krcg folder (ignored by git):

```bash
export GITHUB_USERNAME="dedicated_github_username_for_the_api"
export GITHUB_TOKEN="the_matching_github_token"
```
