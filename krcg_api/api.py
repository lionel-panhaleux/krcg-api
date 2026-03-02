from collections.abc import Iterable

import arrow
import babel
import io
import math
import random
import urllib.parse

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse, RedirectResponse

from krcg import analyzer
from krcg import deck
from krcg import twda
from krcg import utils as krcg_utils
from krcg import vtes

from . import config
from .models import (
    CandidateFullResponse,
    CandidateNameResponse,
    CandidatesRequest,
    CardResponse,
    CardSearchDimensionsResponse,
    CardSearchRequest,
    DeckListResponse,
    DeckResponse,
    DeckSearchRequest,
)

router = APIRouter()


@router.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get(
    "/card/{text}",
    tags=["Card"],
    summary="Get card information",
    description=(
        "Return the matching card information. "
        "Also works with **translated** card names."
    ),
    response_model=CardResponse,
    response_model_exclude_none=True,
)
def card(text: str) -> dict:
    card_id: int | str = text
    try:
        card_id = int(text)
    except ValueError:
        card_id = urllib.parse.unquote(text)
    try:
        return vtes.VTES[card_id].to_json()
    except KeyError:
        raise HTTPException(status_code=404, detail="Card not found")


@router.post(
    "/twda",
    tags=["Deck"],
    summary="Get TWDA decks matching given filters",
    response_model=list[DeckResponse],
    response_model_exclude_none=True,
)
def deck_search(data: DeckSearchRequest | None = None) -> list[dict]:
    if data is None:
        data = DeckSearchRequest()
    if data.player:
        decks = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data.player)]
        ]
    else:
        decks = list(twda.TWDA.values())
    if data.players_count:
        decks = [d for d in decks if (d.players_count or 0) >= int(data.players_count)]
    if data.date_from:
        decks = [d for d in decks if d.date >= arrow.get(data.date_from).date()]
    if data.date_to:
        decks = [d for d in decks if d.date < arrow.get(data.date_to).date()]
    if data.cards:
        try:
            cards = set(vtes.VTES[c] for c in data.cards)
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid card name: {e.args}")
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return [d.to_json() for d in decks]


@router.post(
    "/twda/list",
    tags=["Deck"],
    summary="Get list of TWDA decks matching given filters",
    response_model=DeckListResponse,
    response_model_exclude_none=True,
)
def deck_list(data: DeckSearchRequest | None = None) -> dict:
    if data is None:
        data = DeckSearchRequest()
    if data.player:
        decks: list[deck.Deck] = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data.player)]
        ]
    else:
        decks = list(twda.TWDA.values())
    if data.players_count:
        decks = [d for d in decks if (d.players_count or 0) >= int(data.players_count)]
    if data.date_from:
        decks = [
            d for d in decks if d.date and d.date >= arrow.get(data.date_from).date()
        ]
    if data.date_to:
        decks = [d for d in decks if d.date and d.date < arrow.get(data.date_to).date()]
    if data.cards:
        try:
            cards = set(vtes.VTES[c] for c in data.cards)
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid card name: {e.args}")
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return {
        "count": len(decks),
        "decks": [
            {"name": d.name, "id": d.id, "date": d.date, "author": d.author}
            for d in decks
        ],
    }


@router.get(
    "/twda/{twda_id}",
    tags=["Deck"],
    summary="Get a deck by its TWDA ID",
    description="Returns the deck with the given ID in the TWDA.",
    response_model=DeckResponse,
    response_model_exclude_none=True,
)
def deck_by_id(twda_id: str) -> dict:
    if not twda_id:
        raise HTTPException(status_code=400, detail="Bad Request")
    if twda_id not in twda.TWDA:
        raise HTTPException(status_code=404, detail="Not Found")
    return twda.TWDA[twda_id].to_json()


@router.post(
    "/twda/random",
    tags=["Deck"],
    summary="Get a random TWDA deck matching given filters",
    response_model=DeckResponse,
    response_model_exclude_none=True,
)
def random_deck(data: DeckSearchRequest | None = None) -> dict:
    if data is None:
        data = DeckSearchRequest()
    if data.player:
        decks = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data.player)]
        ]
    else:
        decks = list(twda.TWDA.values())
    if data.players_count:
        decks = [d for d in decks if (d.players_count or 0) >= int(data.players_count)]
    if data.date_from:
        decks = [d for d in decks if d.date >= arrow.get(data.date_from).date()]
    if data.date_to:
        decks = [d for d in decks if d.date < arrow.get(data.date_to).date()]
    if data.cards:
        try:
            cards = set(vtes.VTES[c] for c in data.cards)
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid card name: {e.args}")
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return random.choice(decks).to_json()


@router.post(
    "/convert/{format}",
    tags=["Deck"],
    summary="Convert a deck list format",
    description=(
        "Provide a text/plain or application/json deck list, "
        "returns the decklist in the requested format (defaults to json)."
    ),
    response_model=None,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/DeckResponse"},
                    "example": {
                        "crypt": {
                            "count": 12,
                            "cards": [
                                {
                                    "count": 1,
                                    "id": 200517,
                                    "name": "Gilbert Duane",
                                },
                                {
                                    "count": 1,
                                    "id": 200929,
                                    "name": "Mariel, Lady Thunder",
                                },
                            ],
                        },
                        "library": {
                            "count": 19,
                            "cards": [
                                {
                                    "type": "Master",
                                    "count": 3,
                                    "cards": [
                                        {
                                            "count": 3,
                                            "id": 102113,
                                            "name": "Vessel",
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                },
                "text/plain": {
                    "schema": {"type": "string"},
                    "example": (
                        "Crypt (12 cards)\n"
                        "1x Gilbert Duane\n"
                        "1x Mariel, Lady Thunder\n\n"
                        "Library (19 cards)\n"
                        "Master (3)\n"
                        "3x Vessel"
                    ),
                },
            },
        }
    },
    responses={
        200: {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/DeckResponse"},
                    "example": {
                        "crypt": {
                            "count": 12,
                            "cards": [
                                {
                                    "count": 3,
                                    "id": 200848,
                                    "name": "Lodin (Olaf Holte)",
                                }
                            ],
                        },
                        "library": {
                            "count": 88,
                            "cards": [
                                {
                                    "type": "Master",
                                    "count": 16,
                                    "cards": [
                                        {
                                            "count": 2,
                                            "id": 102121,
                                            "name": "Villein",
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                },
                "text/plain": {
                    "example": (
                        "3x Lodin (Olaf Holte)\n"
                        "2x Graham Gottesman\n\n"
                        "2x Villein\n"
                        "11x Govern the Unaligned"
                    )
                },
            }
        }
    },
)
@router.post("/convert", tags=["Deck"], include_in_schema=False, response_model=None)
async def convert(request: Request, format: str = "json") -> dict | PlainTextResponse:
    raw_data = await request.body()
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        d = deck.Deck()
        d.from_json(await request.json())
    else:
        try:
            text = io.StringIO(raw_data.decode("utf-8"))
            d = deck.Deck.from_txt(text)
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Failed to decode text/plain data in utf-8",
            )
    if format in ["twd", "lackey", "jol"]:
        return PlainTextResponse(d.to_txt(format), status_code=200)
    else:
        return d.to_json()


def _url_request_body(example_url: str) -> dict:
    """OpenAPI extra for endpoints that accept a URL via raw Request."""
    return {
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["url"],
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "Share URL for the deck.",
                            }
                        },
                    },
                    "example": {"url": example_url},
                }
            },
        }
    }


@router.post(
    "/amaranth",
    tags=["Deck"],
    summary="Retrieve a deck from Amaranth",
    description=(
        "Retrieve a deck from [Amaranth](https://amaranth.vtes.co.nz/) "
        "using a share URL."
    ),
    response_model=DeckResponse,
    response_model_exclude_none=True,
    openapi_extra=_url_request_body(
        "https://amaranth.vtes.co.nz/#deck/4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
    ),
)
async def amaranth(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        data = await request.json()
    else:
        form = await request.form()
        data = dict(form)
    if "url" not in data:
        raise HTTPException(status_code=400, detail="Missing required parameter: url")
    return deck.Deck.from_url(str(data["url"])).to_json()


@router.post(
    "/vdb",
    tags=["Deck"],
    summary="Retrieve a deck from VDB",
    description=("Retrieve a deck from [VDB](https://vdb.im) using a share URL."),
    response_model=DeckResponse,
    response_model_exclude_none=True,
    openapi_extra=_url_request_body("https://vdb.im/decks/b798e734f"),
)
async def vdb(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        data = await request.json()
    else:
        form = await request.form()
        data = dict(form)
    if "url" not in data:
        raise HTTPException(status_code=400, detail="Missing required parameter: url")
    return deck.Deck.from_url(str(data["url"])).to_json()


@router.post(
    "/vtesdecks",
    tags=["Deck"],
    summary="Retrieve a deck from VTES Decks",
    description=(
        "Retrieve a deck from [VTES Decks](https://vtesdecks.com) using a share URL."
    ),
    response_model=DeckResponse,
    response_model_exclude_none=True,
    openapi_extra=_url_request_body("https://vtesdecks.com/deck/example-deck-id"),
)
async def vtesdecks(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        data = await request.json()
    else:
        form = await request.form()
        data = dict(form)
    if "url" not in data:
        raise HTTPException(status_code=400, detail="Missing required parameter: url")
    return deck.Deck.from_url(str(data["url"])).to_json()


@router.post(
    "/candidates",
    tags=["Card"],
    summary="Given a list of cards, returns likely additional candidates for a deck",
    description=(
        "Only 10 candidates are returned. If there are less than 4 decks in the TWDA "
        "that resemble the cards list provided, 404 is returned. "
        "If no card is provided, it will simply output the list of most played cards."
    ),
    response_model=list[CandidateNameResponse] | list[CandidateFullResponse],
    response_model_exclude_none=True,
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "name_mode": {
                            "summary": "Name mode (default)",
                            "value": [
                                {
                                    "card": "Ashur Tablets",
                                    "score": 1.0,
                                    "average": 14,
                                    "deviation": 6.25,
                                },
                                {
                                    "card": "Giant's Blood",
                                    "score": 1.0,
                                    "average": 1,
                                    "deviation": 0.0,
                                },
                            ],
                        },
                        "full_mode": {
                            "summary": "Full mode (mode=full)",
                            "value": [
                                {
                                    "card": {
                                        "id": 100106,
                                        "name": "Ashur Tablets",
                                        "printed_name": "Ashur Tablets",
                                        "url": "https://static.krcg.org/card/ashurtablets.jpg",
                                        "types": ["Master"],
                                        "card_text": "Only one Ashur Tablets can be played each turn...",
                                        "sets": {},
                                        "scans": {},
                                        "artists": ["Sandra Chang-Adair"],
                                        "ordered_sets": ["Keepers of Tradition"],
                                        "legality": "2008-11-19",
                                    },
                                    "score": 1.0,
                                    "average": 14,
                                    "deviation": 6.25,
                                }
                            ],
                        },
                    }
                }
            },
            "description": (
                "List of candidate cards. Shape depends on **mode**: "
                "default returns card names as strings, "
                "**full** returns complete card objects."
            ),
        }
    },
)
def candidates(data: CandidatesRequest | None = None) -> list[dict]:
    if data is None:
        data = CandidatesRequest()
    full = data.mode == "full"
    decks: list[deck.Deck] = list(twda.TWDA.values())
    if data.players_count:
        decks = [d for d in decks if (d.players_count or 0) >= int(data.players_count)]
    if data.date_from:
        decks = [
            d for d in decks if d.date and d.date >= arrow.get(data.date_from).date()
        ]
    if data.date_to:
        decks = [d for d in decks if d.date and d.date < arrow.get(data.date_to).date()]
    try:
        cards_list = [vtes.VTES[c] for c in (data.cards or [])]
        A = analyzer.Analyzer(decks)
        A.refresh(*cards_list)
        if len(A.examples) < 4:
            raise HTTPException(status_code=404, detail="Too few examples in TWDA")
        if cards_list:
            ret = A.candidates(*cards_list, spoiler_multiplier=1)[:10]
        else:
            ret = A.played.most_common()[:10]
        if full:
            return [
                {
                    "card": c.to_json(),
                    "score": round(
                        s / (len(cards_list) if cards_list else len(decks)), 4
                    ),
                    "average": round(A.average[c]),
                    "deviation": round(math.sqrt(A.variance[c]), 2),
                }
                for c, s in ret
            ]
        else:
            return [
                {
                    "card": c.usual_name,
                    "score": round(
                        s / (len(cards_list) if cards_list else len(decks)), 4
                    ),
                    "average": round(A.average[c]),
                    "deviation": round(math.sqrt(A.variance[c]), 2),
                }
                for c, s in ret
            ]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid card name: {e.args}")


@router.get(
    "/complete/{text}",
    tags=["Card"],
    summary="Complete a card name",
    description=(
        "Return all candidates matching the partial name. "
        "If Accept-Language is set, will also return available names in that language, "
        "in addition to the english completions."
    ),
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        "Pentex\u2122 Subversion",
                        "Pentagon, The",
                    ]
                }
            }
        }
    },
)
def complete(
    text: str,
    accept_language: str | None = Header(None, alias="Accept-Language"),
) -> list[str]:
    lang = _negotiate_locale(_parse_accept_language(accept_language))
    return vtes.VTES.complete(urllib.parse.unquote(text), lang)


@router.post(
    "/card_search",
    tags=["Card"],
    summary="Get cards matching given filters",
    description=(
        "If multiple filters are specified, only get cards matching **all filters**. "
        "If no filter is specified, get all cards. "
        "Only the *discipline* field is case sensitive.\n\n"
        "Filtering on the text fields *text*, *card_text*, *flavor_text* and *name* "
        "is done using a case insensitive prefix search in full text. "
        "It will match two separated words, but only match words from start, "
        "not parts of them. It will not match any other enum field (eg. *type*).\n\n"
        "When multiple values are provided for a given filter, it matches any value, "
        'except for the "trait", "bonus" and "discipline" dimensions, where it must '
        "match all values.\n\n"
        "Note that:\n\n"
        "- Crypt & Library are included in *type*.\n"
        "- Independent titles are registered as *1 vote* and *2 votes*.\n"
        "- City titles are also registered in the *city* dimension.\n"
        '- Crypt cards in the "any" group are registered in all groups.\n'
        "- Disciplines are case-sensitive: "
        "UPPERCASE trigram (eg. *AUS*) to denote the **superior** version "
        "and lowercase trigram (eg. *aus*) to denote the **inferior** version.\n"
        "- Virtues are listed as disciplines. "
        "*vin* is used as trigram for the Vision virtue, so as to not mix it with "
        "*vis* Visceratika.\n"
        "- Only crypt cards register superior disciplines.\n"
        "- *flight*, *striga* and *maleficia* are registered as disciplines.\n"
        "- Multi-disciplines cards are registered in the *multi* discipline, "
        "then in the *combo* or *choice* discipline, depending on the case. "
        "In contrast, mono discipline cards are registered in the *mono* discipline. "
        "Cards requiring no discipline are registered in the *none* discipline. "
        "This allows for search like *discipline: [mono, ani]*."
    ),
    response_model=None,
    responses={
        200: {
            "content": {
                "application/json": {
                    "schema": {
                        "anyOf": [
                            {
                                "type": "array",
                                "title": "Name mode (default)",
                                "items": {"type": "string"},
                            },
                            {
                                "type": "array",
                                "title": "Full mode (mode=full)",
                                "items": {"$ref": "#/components/schemas/CardResponse"},
                            },
                        ]
                    },
                    "examples": {
                        "name_mode": {
                            "summary": "Name mode (default)",
                            "value": [
                                "Eat the Rich",
                                "Firebrand",
                                "Free States Rant",
                                "Reckless Agitation",
                            ],
                        },
                        "full_mode": {
                            "summary": "Full mode (mode=full)",
                            "value": [
                                {
                                    "id": 100038,
                                    "name": "Alastor",
                                    "printed_name": "Alastor",
                                    "url": "https://static.krcg.org/card/alastor.jpg",
                                    "types": ["Political Action"],
                                    "card_text": "Requires a justicar or Inner Circle member...",
                                    "sets": {},
                                    "scans": {},
                                    "artists": ["Monte Moore"],
                                    "ordered_sets": ["Gehenna"],
                                    "legality": "2004-05-17",
                                }
                            ],
                        },
                    },
                }
            },
            "description": (
                "List of matching cards. Shape depends on **mode**: "
                "default returns card names as strings, "
                "**full** returns complete card objects."
            ),
        }
    },
)
def card_search(data: CardSearchRequest | None = None) -> list:
    if data is None:
        data = CardSearchRequest()
    search_data = data.model_dump(exclude_none=True)
    full = search_data.pop("mode", "") == "full"
    if search_data.get("lang"):
        search_data["lang"] = _negotiate_locale([search_data["lang"]])
    try:
        result = sorted(vtes.VTES.search(**search_data), key=lambda c: c.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if full:
        return [c.to_json() for c in result]
    return [c.usual_name for c in result]


@router.get(
    "/card_search",
    tags=["Card"],
    summary="Get available search dimensions",
    description=(
        "Returns a JSON dictionary of search dimensions. "
        "Note that the text dimensions *text*, *name*, *card_text* and *flavor_text* "
        "are not included in the response."
    ),
    response_model=CardSearchDimensionsResponse,
    response_model_exclude_none=True,
)
def card_search_dimensions() -> dict:
    return vtes.VTES.search_dimensions


def _parse_accept_language(header: str | None) -> list[str]:
    """Parse an Accept-Language header into a list of locale strings."""
    if not header:
        return []
    locales = []
    for part in header.split(","):
        part = part.strip()
        if not part:
            continue
        # strip quality factor (e.g. ";q=0.9")
        lang = part.split(";")[0].strip()
        if lang:
            locales.append(lang)
    return locales


def _negotiate_locale(preferred: Iterable[str]) -> str:
    res = babel.negotiate_locale(
        [x.replace("_", "-") for x in preferred],
        ["en"] + list(config.SUPPORTED_LANGUAGES),
        sep="-",
    )
    # negotiation is case-insensitive but the result uses the case of the first argument
    if res:
        res = res[:2]
    return res or "en"
