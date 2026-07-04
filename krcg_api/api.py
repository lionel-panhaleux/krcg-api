from collections.abc import Iterable
from typing import Annotated, Any

import io
import math
import random
import urllib.parse

import aiohttp
import arrow
import babel
import msgspec
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import PlainTextResponse, RedirectResponse

from krcg import analyzer
from krcg import collections as krcg_collections
from krcg import models
from krcg import parser
from krcg import providers
from krcg import twda as krcg_twda
from krcg import utils as krcg_utils

from . import config
from .models import (
    CandidatesRequest,
    CardSearchRequest,
    DeckSearchRequest,
)

router = APIRouter()

#: search keys understood by krcg (everything else in a request is ignored)
SEARCH_DIMENSIONS = {dimension.value for dimension in models.SearchDimension}
#: trie dimensions a free-text "text" query is unioned over
TEXT_DIMENSIONS = ["name", "card_text", "flavor_text"]
#: dimensions matched case-sensitively (everything else is case-insensitive)
CASE_SENSITIVE_DIMENSIONS = {"discipline", *TEXT_DIMENSIONS}


def get_cards(request: Request) -> krcg_collections.CardDict:
    """Dependency: the loaded cards library."""
    return request.app.state.cards


def get_twda(request: Request) -> krcg_twda.DecksArchive:
    """Dependency: the loaded TWDA."""
    return request.app.state.twda


def get_http(request: Request) -> aiohttp.ClientSession:
    """Dependency: the shared aiohttp session (deck providers)."""
    return request.app.state.http


Cards = Annotated[krcg_collections.CardDict, Depends(get_cards)]
Twda = Annotated[krcg_twda.DecksArchive, Depends(get_twda)]
Http = Annotated[aiohttp.ClientSession, Depends(get_http)]


def _card_json(card: models.Card) -> dict[str, Any]:
    """Serialize a card to the krcg v5 JSON shape."""
    return msgspec.to_builtins(card, str_keys=True)


def _deck_json(deck: models.Deck) -> dict[str, Any]:
    """Serialize a deck to the krcg v5 JSON shape."""
    return msgspec.to_builtins(deck, str_keys=True)


def _resolve_card_ids(
    cards: krcg_collections.CardDict, names: Iterable[str | int]
) -> set[int]:
    """Resolve card names or ids to their integer ids (400 on an unknown name)."""
    try:
        return {cards[name].id for name in names}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Invalid card name: {e.args}")


def _filter_decks(
    decks: Iterable[models.Deck],
    cards: krcg_collections.CardDict,
    data: DeckSearchRequest | CandidatesRequest,
) -> list[models.Deck]:
    """Filter a deck collection by the request's common filters."""
    result = list(decks)
    player = getattr(data, "player", None)
    if player:
        norm = krcg_utils.normalize(player)
        result = [d for d in result if norm in krcg_utils.normalize(d.author or "")]
    if data.players_count:
        count = int(data.players_count)
        result = [d for d in result if d.event and d.event.players_count >= count]
    if data.date_from:
        date_from = arrow.get(data.date_from).date()
        result = [
            d for d in result if d.event and d.event.date and d.event.date >= date_from
        ]
    if data.date_to:
        date_to = arrow.get(data.date_to).date()
        result = [
            d for d in result if d.event and d.event.date and d.event.date < date_to
        ]
    if data.cards:
        ids = _resolve_card_ids(cards, data.cards)
        result = [d for d in result if ids <= {entry.id for entry in d.cards}]
    return result


def _canonicalize_criteria(
    cards: krcg_collections.CardDict, criteria: dict[str, Any]
) -> dict[str, Any]:
    """Make set-dimension values case-insensitive (krcg matches case-sensitively).

    Each value is expanded to the dimension choices it matches case-insensitively
    (an OR), so ``sect=["anarch"]`` finds the ``Anarch`` cards. The case-sensitive
    dimensions (``discipline`` and the text tries) pass through untouched.
    """
    dimensions: dict[str, Any] | None = None
    result: dict[str, Any] = {}
    for key, value in criteria.items():
        if key in CASE_SENSITIVE_DIMENSIONS or not isinstance(value, list):
            result[key] = value
            continue
        if dimensions is None:
            dimensions = cards.search_dimensions
        folded: dict[str, list[str]] = {}
        for choice in dimensions.get(key, []):
            if isinstance(choice, str):
                folded.setdefault(choice.lower(), []).append(choice)
        expanded: list[str] = []
        for item in value:
            expanded.extend(folded.get(item.lower(), [item]))
        result[key] = expanded
    return result


@router.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/scalar")


@router.get(
    "/card/{text}",
    tags=["Card"],
    summary="Get card information",
    description=(
        "Return the matching card in the krcg v5 JSON format. "
        "Accepts a card **id** or a card **name** (also **translated** names)."
    ),
    response_model=None,
)
def card(text: str, cards: Cards) -> dict[str, Any]:
    card_id: int | str
    try:
        card_id = int(text)
    except ValueError:
        card_id = urllib.parse.unquote(text)
    try:
        return _card_json(cards[card_id])
    except KeyError:
        raise HTTPException(status_code=404, detail="Card not found")


@router.post(
    "/twda",
    tags=["Deck"],
    summary="Get TWDA decks matching given filters",
    response_model=None,
)
def deck_search(
    cards: Cards, twda: Twda, data: DeckSearchRequest | None = None
) -> list[Any]:
    decks = _filter_decks(twda.values(), cards, data or DeckSearchRequest())
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return [_deck_json(d) for d in decks]


@router.post(
    "/twda/list",
    tags=["Deck"],
    summary="Get list of TWDA decks matching given filters",
    response_model=None,
)
def deck_list(
    cards: Cards, twda: Twda, data: DeckSearchRequest | None = None
) -> dict[str, Any]:
    decks = _filter_decks(twda.values(), cards, data or DeckSearchRequest())
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return {
        "count": len(decks),
        "decks": [
            {
                "name": d.name,
                "id": d.id,
                "date": d.event.date if d.event else None,
                "author": d.author,
            }
            for d in decks
        ],
    }


@router.get(
    "/twda/{twda_id}",
    tags=["Deck"],
    summary="Get a deck by its TWDA ID",
    description="Returns the deck with the given ID in the TWDA.",
    response_model=None,
)
def deck_by_id(twda_id: str, twda: Twda) -> dict[str, Any]:
    if not twda_id:
        raise HTTPException(status_code=400, detail="Bad Request")
    if twda_id not in twda:
        raise HTTPException(status_code=404, detail="Not Found")
    return _deck_json(twda[twda_id])


@router.post(
    "/twda/random",
    tags=["Deck"],
    summary="Get a random TWDA deck matching given filters",
    response_model=None,
)
def random_deck(
    cards: Cards, twda: Twda, data: DeckSearchRequest | None = None
) -> dict[str, Any]:
    decks = _filter_decks(twda.values(), cards, data or DeckSearchRequest())
    if not decks:
        raise HTTPException(status_code=404, detail="No result in TWDA")
    return _deck_json(random.choice(decks))


@router.post(
    "/convert/{format}",
    tags=["Deck"],
    summary="Convert a deck list format",
    description=(
        "Provide a text/plain or application/json (krcg v5 deck) deck list, "
        "returns the decklist in the requested format (defaults to json). "
        "Plain-text formats: twd, txt, lackey, jol, vdb."
    ),
    response_model=None,
)
@router.post("/convert", tags=["Deck"], include_in_schema=False, response_model=None)
async def convert(
    request: Request, cards: Cards, format: str = "json"
) -> dict[str, Any] | PlainTextResponse:
    raw_data = await request.body()
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            deck = msgspec.convert(await request.json(), models.Deck)
        except (msgspec.ValidationError, msgspec.DecodeError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid deck: {e}")
    else:
        try:
            text = io.StringIO(raw_data.decode("utf-8"))
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Failed to decode text/plain data in utf-8",
            )
        deck = parser.deck_from_txt(text, cards)
    match format:
        case "twd":
            return PlainTextResponse(providers.serialize_twd(deck, cards))
        case "txt":
            return PlainTextResponse(providers.serialize_txt(deck))
        case "lackey":
            return PlainTextResponse(providers.serialize_lackey(deck))
        case "jol":
            return PlainTextResponse(providers.serialize_jol(deck))
        case "vdb":
            return PlainTextResponse(providers.serialize_vdb(deck))
        case _:
            return _deck_json(deck)


def _url_request_body(example_url: str) -> dict[str, Any]:
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


async def _fetch_deck(request: Request, cards: Cards, session: Http) -> dict[str, Any]:
    """Read a `url` from the request body and fetch the matching deck."""
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        data = await request.json()
    else:
        form = await request.form()
        data = dict(form)
    if "url" not in data:
        raise HTTPException(status_code=400, detail="Missing required parameter: url")
    try:
        deck = await providers.fetch(session, str(data["url"]), cards)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch the deck: {e}")
    return _deck_json(deck)


@router.post(
    "/amaranth",
    tags=["Deck"],
    summary="Retrieve a deck from Amaranth",
    description=(
        "Retrieve a deck from [Amaranth](https://amaranth.vtes.co.nz/) "
        "using a share URL."
    ),
    response_model=None,
    openapi_extra=_url_request_body(
        "https://amaranth.vtes.co.nz/#deck/4d3aa426-70da-44b7-8cb7-92377a1a0dbd"
    ),
)
async def amaranth(request: Request, cards: Cards, session: Http) -> dict[str, Any]:
    return await _fetch_deck(request, cards, session)


@router.post(
    "/vdb",
    tags=["Deck"],
    summary="Retrieve a deck from VDB",
    description="Retrieve a deck from [VDB](https://vdb.im) using a share URL.",
    response_model=None,
    openapi_extra=_url_request_body("https://vdb.im/decks/b798e734f"),
)
async def vdb(request: Request, cards: Cards, session: Http) -> dict[str, Any]:
    return await _fetch_deck(request, cards, session)


@router.post(
    "/vtesdecks",
    tags=["Deck"],
    summary="Retrieve a deck from VTES Decks",
    description=(
        "Retrieve a deck from [VTES Decks](https://vtesdecks.com) using a share URL."
    ),
    response_model=None,
    openapi_extra=_url_request_body("https://vtesdecks.com/deck/example-deck-id"),
)
async def vtesdecks(request: Request, cards: Cards, session: Http) -> dict[str, Any]:
    return await _fetch_deck(request, cards, session)


@router.post(
    "/candidates",
    tags=["Card"],
    summary="Given a list of cards, returns likely additional candidates for a deck",
    description=(
        "Only 10 candidates are returned. If there are less than 4 decks in the TWDA "
        "that play all the cards provided, 404 is returned. "
        "If no card is provided, it will simply output the list of most played cards."
    ),
    response_model=None,
)
def candidates(
    cards: Cards, twda: Twda, data: CandidatesRequest | None = None
) -> list[Any]:
    if data is None:
        data = CandidatesRequest()
    full = data.mode == "full"
    decks = _filter_decks(twda.values(), cards, data)
    reference = _resolve_cards(cards, data.cards or [])
    ref_ids = {c.id for c in reference}
    examples = [d for d in decks if ref_ids <= {entry.id for entry in d.cards}]
    if len(examples) < 4:
        raise HTTPException(status_code=404, detail="Too few examples in TWDA")
    stats = analyzer.stats(decks, cards)
    if reference:
        ranked = analyzer.affinity(decks, cards, *reference)[:10]
        scale = len(reference)
        scored = [(c, score / scale) for c, score in ranked]
    else:
        played = analyzer.played(decks, cards)
        scale = len(decks)
        scored = [(c, count / scale) for c, count in played.most_common(10)]
    return [
        {
            "card": _card_json(c) if full else c.unique_name,
            "score": round(score, 4),
            "average": round(stats[c][0]) if c in stats else 0,
            "deviation": round(math.sqrt(stats[c][1]), 2) if c in stats else 0.0,
        }
        for c, score in scored
    ]


def _resolve_cards(
    cards: krcg_collections.CardDict, names: Iterable[str | int]
) -> list[models.Card]:
    """Resolve card names or ids to cards (400 on an unknown name)."""
    try:
        return [cards[name] for name in names]
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
                "application/json": {"example": ["Pentex™ Subversion", "Pentagon, The"]}
            }
        }
    },
)
def complete(
    text: str,
    cards: Cards,
    accept_language: str | None = Header(None, alias="Accept-Language"),
) -> list[str]:
    lang = _negotiate_locale(_parse_accept_language(accept_language))
    matches = cards.complete(urllib.parse.unquote(text), lang)
    return [_display_name(c, lang) for c in matches]


def _display_name(card: models.Card, lang: str) -> str:
    """The card name in the requested language, falling back to English."""
    if lang != models.Lang.EN:
        translation = card.i18n.get(models.Lang(lang))
        if translation:
            return translation.name
    return card.unique_name


@router.post(
    "/card_search",
    tags=["Card"],
    summary="Get cards matching given filters",
    description=(
        "If multiple filters are specified, only get cards matching **all filters**. "
        "If no filter is specified, get all cards. "
        "Only the *discipline* field is case sensitive.\n\n"
        "The *text* filter matches card names, card text and flavor text "
        "(case insensitive prefix search). When multiple values are provided for a "
        "given filter, it matches any value, except for the *trait*, *bonus* and "
        "*discipline* dimensions, where it must match all values.\n\n"
        "Use `mode=full` to get full card objects (krcg v5 JSON) instead of names."
    ),
    response_model=None,
)
def card_search(cards: Cards, data: CardSearchRequest | None = None) -> list[Any]:
    if data is None:
        data = CardSearchRequest()
    search_data = data.model_dump(exclude_none=True)
    full = search_data.pop("mode", "") == "full"
    lang_req = search_data.pop("lang", None)
    text_val = search_data.pop("text", None)
    lang = _negotiate_locale([lang_req]) if lang_req else "en"
    search_lang = models.Lang(lang)
    criteria: dict[str, Any] = {}
    for key, value in search_data.items():
        if key not in SEARCH_DIMENSIONS:
            continue
        if not isinstance(value, list):
            criteria[key] = value
        elif key == "group":
            # krcg groups are "G1".."G7"/"Any"; accept bare numbers too
            criteria[key] = [f"G{v}" if str(v).isdigit() else str(v) for v in value]
        else:
            criteria[key] = [str(v) for v in value]
    criteria = _canonicalize_criteria(cards, criteria)
    try:
        if criteria:
            result = set(cards.search(n=None, lang=search_lang, **criteria))
        elif text_val:
            result = set(cards.cards())
        else:
            result = set(cards.cards())
        if text_val:
            matches: set[models.Card] = set()
            for dimension in TEXT_DIMENSIONS:
                matches |= set(
                    cards.search(n=None, lang=search_lang, **{dimension: text_val})
                )
            result &= matches
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    ordered = sorted(result, key=lambda c: c.unique_name)
    if full:
        return [_card_json(c) for c in ordered]
    return [c.unique_name for c in ordered]


@router.get(
    "/card_search",
    tags=["Card"],
    summary="Get available search dimensions",
    description=(
        "Returns a JSON dictionary of search dimensions. "
        "Note that the text dimensions *name*, *card_text* and *flavor_text* "
        "are not included in the response."
    ),
    response_model=None,
)
def card_search_dimensions(cards: Cards) -> dict[str, Any]:
    return cards.search_dimensions


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
