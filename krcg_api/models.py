"""Pydantic models for request validation and OpenAPI documentation.

Responses are served in the krcg v5 JSON format (see the `krcg` package
``models`` module); only request bodies are modelled here.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DeckSearchRequest(BaseModel):
    """Filters for searching TWDA decks."""

    player: str | None = Field(
        default=None, description="Player name (case insensitive)"
    )
    players_count: int | None = Field(
        default=None,
        description=("Only consider tournaments with at least this number of players."),
    )
    date_from: str | None = Field(
        default=None, description="Only consider decks from this date on."
    )
    date_to: str | None = Field(
        default=None, description="Only consider decks until this date."
    )
    cards: list[str | int] | None = Field(
        default=None,
        description="Return decks containing those cards (card names or IDs).",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cards": ["François Villon"],
                    "date_from": "1994-01-01",
                    "players_count": 25,
                }
            ]
        }
    }


class CandidatesRequest(BaseModel):
    """Request body for the /candidates endpoint."""

    mode: str | None = Field(
        default=None,
        description='Response format: "name" returns card names, "full" returns '
        "full card JSON.",
    )
    players_count: int | None = Field(
        default=None,
        description=(
            "If set, only consider tournament winning decks from tournaments "
            "with at least that many players participating."
        ),
    )
    date_from: str | None = Field(
        default=None,
        description="If set, only consider tournament winning decks from that date on.",
    )
    date_to: str | None = Field(
        default=None,
        description="If set, only consider tournament winning decks up to that date.",
    )
    cards: list[str | int] | None = Field(
        default=None, description="List of card names or IDs."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cards": ["Cybele", "Nana Buruku"],
                    "date_from": "2015",
                    "date_to": "2020",
                }
            ]
        }
    }


class CardSearchRequest(BaseModel):
    """Request body for the POST /card_search endpoint.

    Accepts dynamic keyword arguments for search dimensions.
    """

    mode: str | None = Field(
        default=None,
        description='Response format: "name" returns card names, "full" returns '
        "full card JSON.",
    )
    lang: str | None = Field(
        default=None,
        description="Additional language to search in (for text search only).",
    )
    type: list[str] | None = Field(default=None, description="Type of the card.")
    clan: list[str] | None = Field(
        default=None, description="Clan/Creed or required clan/creed (or none)."
    )
    group: list[int] | None = Field(
        default=None, description="Group (crypt cards only)."
    )
    trait: list[str] | None = Field(default=None, description="Trait.")
    discipline: list[str] | None = Field(
        default=None,
        description=(
            "Discipline trigram. Case matters. Special values: "
            "none, mono, multi, combo, choice, flight, striga, maleficia."
        ),
    )
    sect: list[str] | None = Field(
        default=None,
        description="Vampiric sect. Also matches cards requiring a sect.",
    )
    title: list[str] | None = Field(
        default=None, description="Title. Also matches cards requiring a title."
    )
    set: list[str] | None = Field(
        default=None, description="Set the card was edited in."
    )
    rarity: list[str] | None = Field(
        default=None, description="Rarity of the card in boosters."
    )
    precon: list[str] | None = Field(default=None, description="Precon starter.")
    artist: list[str] | None = Field(
        default=None, description="Artist for the card picture."
    )
    city: list[str] | None = Field(
        default=None, description="Matches cards related to a city title."
    )
    bonus: list[str] | None = Field(default=None, description="Special bonus provided.")
    capacity: list[str] | None = Field(default=None, description="Capacity.")
    text: str | None = Field(
        default=None,
        description="Text to search for - matches card names, card text and flavor.",
    )
    card_text: str | None = Field(
        default=None,
        description="Card text to search for, excluding card names and flavor text.",
    )
    name: str | None = Field(default=None, description="Card name to search for.")
    flavor_text: str | None = Field(
        default=None, description="Flavor text to search for."
    )

    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [{"type": ["political action"], "sect": ["anarch"]}]
        },
    }


class UrlRequest(BaseModel):
    """Request body for /amaranth, /vdb, /vtesdecks endpoints."""

    url: str = Field(description="Share URL for the deck.")
