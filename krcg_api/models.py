"""Pydantic models for request validation and OpenAPI documentation."""

from __future__ import annotations

import datetime

from pydantic import BaseModel, Field


# --- Request Models ---


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
        description="Return decks containing those cards (case insensitive card names or IDs).",
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
        description='Response format: "name" returns card names, "full" returns full card JSON.',
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

    Accepts dynamic keyword arguments for search dimensions since
    ``vtes.VTES.search()`` accepts ``**kwargs``.
    """

    mode: str | None = Field(
        default=None,
        description='Response format: "name" returns card names, "full" returns full card JSON.',
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
        description="Card text to search for - also matches card names and flavor text.",
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


# --- Response Models ---


class RulingReference(BaseModel):
    """A reference to a ruling source."""

    text: str = Field(description="Full reference text.")
    label: str = Field(description="Short label.")
    url: str = Field(description="URL to the ruling source.")


class Ruling(BaseModel):
    """A ruling for a card."""

    text: str = Field(description="The ruling text.")
    references: list[RulingReference] = Field(default_factory=list)
    model_config = {"extra": "allow"}


class SetPrinting(BaseModel):
    """A card printing in a specific set."""

    release_date: str | None = Field(default=None, description="Set release date.")
    rarity: str | None = Field(default=None, description="Booster rarity.")
    precon: str | None = Field(default=None, description="Preconstructed deck name.")
    copies: int | None = Field(default=None, description="Number of copies in precon.")


class CardResponse(BaseModel):
    """Full card information.

    Underscore-prefixed fields (``_name``, ``_set``) are internal and pass
    through via ``extra="allow"``; they appear in responses but not in the
    schema since ``name`` and ``sets`` are the user-facing equivalents.
    """

    id: int = Field(description="Unique card ID.")
    name: str = Field(description="Canonical English card name.")
    printed_name: str = Field(description="Name as printed on the card.")
    url: str = Field(description="URL to card scan image.")
    types: list[str] = Field(description="Card types.")
    card_text: str = Field(description="Card text.")
    sets: dict[str, list[SetPrinting]] = Field(
        description="Sets the card was printed in."
    )
    scans: dict[str, str] = Field(description="Per-set scan image URLs.")
    artists: list[str] = Field(description="Card artists.")
    ordered_sets: list[str] = Field(description="Sets in chronological order.")
    legality: str = Field(description="Date of first legal printing.")
    rulings: list[Ruling] = Field(default_factory=list, description="Card rulings.")
    # Optional fields (crypt-only or card-specific)
    capacity: int | None = Field(default=None, description="Capacity (crypt only).")
    disciplines: list[str] | None = Field(
        default=None, description="Disciplines (crypt or library)."
    )
    clans: list[str] | None = Field(default=None, description="Clans (crypt only).")
    group: str | None = Field(default=None, description="Group (crypt only).")
    title: str | None = Field(default=None, description="Title (crypt only).")
    flavor_text: str | None = Field(default=None, description="Flavor text.")
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "id": 100038,
                    "_name": "Alastor",
                    "_set": "Gehenna:R, KMW:PAl, KoT:R, 30th:1",
                    "name": "Alastor",
                    "printed_name": "Alastor",
                    "url": "https://static.krcg.org/card/alastor.jpg",
                    "types": ["Political Action"],
                    "card_text": (
                        "Requires a justicar or Inner Circle member.\n"
                        "Choose a ready Camarilla vampire. Successful referendum "
                        "means you search your library for an equipment card and "
                        "put this card and the equipment on the chosen vampire "
                        "(ignore requirements; shuffle afterward); pay half the "
                        "cost rounded down of the equipment. The attached vampire "
                        "can enter combat with a vampire as a +1 stealth \u24b9 "
                        "action. The attached vampire cannot commit diablerie. "
                        "A vampire can have only one Alastor."
                    ),
                    "sets": {
                        "Gehenna": [{"rarity": "Rare", "release_date": "2004-05-17"}],
                        "Keepers of Tradition": [
                            {"rarity": "Rare", "release_date": "2008-11-19"}
                        ],
                        "Kindred Most Wanted": [
                            {
                                "copies": 1,
                                "precon": "Alastors",
                                "release_date": "2005-02-21",
                            }
                        ],
                    },
                    "ordered_sets": [
                        "Gehenna",
                        "Kindred Most Wanted",
                        "Keepers of Tradition",
                    ],
                    "scans": {
                        "Gehenna": "https://static.krcg.org/card/set/gehenna/alastor.jpg",
                    },
                    "artists": ["Monte Moore"],
                    "legality": "2004-05-17",
                    "rulings": [
                        {
                            "text": (
                                "If the weapon retrieved costs blood, that cost is "
                                "paid by the vampire chosen by the terms. "
                                "[LSJ 20040518]"
                            ),
                            "references": [
                                {
                                    "label": "LSJ 20040518",
                                    "text": "[LSJ 20040518]",
                                    "url": (
                                        "https://groups.google.com/g/"
                                        "rec.games.trading-cards.jyhad/"
                                        "c/4emymfUPwAM/m/B2SCC7L6kuMJ"
                                    ),
                                }
                            ],
                        }
                    ],
                }
            ]
        },
    }


# --- Deck response models ---


class DeckCardEntry(BaseModel):
    """A card entry in a deck section."""

    id: int = Field(description="Card ID.")
    count: int = Field(description="Number of copies.")
    name: str = Field(description="Card name.")
    comments: str | None = Field(
        default=None, description="Player comments on the card."
    )


class DeckLibrarySection(BaseModel):
    """A library section grouped by card type."""

    type: str = Field(description="Card type for this section.")
    count: int = Field(description="Total cards in this section.")
    cards: list[DeckCardEntry] = Field(description="Cards in this section.")


class DeckCrypt(BaseModel):
    """Crypt portion of a deck."""

    count: int = Field(description="Total crypt cards.")
    cards: list[DeckCardEntry] = Field(description="Crypt cards.")


class DeckLibrary(BaseModel):
    """Library portion of a deck."""

    count: int = Field(description="Total library cards.")
    cards: list[DeckLibrarySection] = Field(
        description="Library sections by card type."
    )


class DeckResponse(BaseModel):
    """Full deck information."""

    id: str | None = Field(default=None, description="Deck ID (TWDA ID or external).")
    event: str | None = Field(default=None, description="Tournament event name.")
    place: str | None = Field(default=None, description="Tournament location.")
    date: str | None = Field(default=None, description="Tournament date.")
    tournament_format: str | None = Field(
        default=None, description="Tournament format (e.g. 2R+F)."
    )
    players_count: int | None = Field(
        default=None, description="Number of players in the tournament."
    )
    player: str | None = Field(default=None, description="Winning player name.")
    author: str | None = Field(default=None, description="Deck author or alias.")
    score: str | None = Field(default=None, description="Final score (e.g. 1GW5+3).")
    name: str | None = Field(default=None, description="Deck name.")
    comments: str | None = Field(default=None, description="Player or deck comments.")
    crypt: DeckCrypt = Field(description="Crypt portion of the deck.")
    library: DeckLibrary = Field(description="Library portion of the deck.")
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "id": "2020bf3hf",
                    "event": "Black Forest Base 3",
                    "place": "Hyvinkää, Finland",
                    "date": "2020-09-05",
                    "name": "My stick is better than bacon",
                    "tournament_format": "2R+F",
                    "players_count": 14,
                    "player": "Niko Vanhatalo",
                    "score": "1GW5+3",
                    "crypt": {
                        "count": 12,
                        "cards": [
                            {"count": 3, "id": 200848, "name": "Lodin (Olaf Holte)"},
                            {"count": 2, "id": 200533, "name": "Graham Gottesman"},
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
                                        "count": 1,
                                        "id": 100058,
                                        "name": "Anarch Troublemaker",
                                    },
                                    {
                                        "count": 2,
                                        "id": 102121,
                                        "name": "Villein",
                                    },
                                ],
                            },
                            {
                                "type": "Action",
                                "count": 14,
                                "cards": [
                                    {
                                        "count": 11,
                                        "id": 100845,
                                        "name": "Govern the Unaligned",
                                    }
                                ],
                            },
                        ],
                    },
                }
            ]
        },
    }


class DeckListEntry(BaseModel):
    """Summary entry for a deck in a list."""

    name: str | None = Field(default=None, description="Deck name.")
    id: str = Field(description="Deck ID.")
    date: str | datetime.date | None = Field(
        default=None, description="Tournament date."
    )
    author: str | None = Field(default=None, description="Deck author.")


class DeckListResponse(BaseModel):
    """Paginated list of deck summaries."""

    count: int = Field(description="Total number of matching decks.")
    decks: list[DeckListEntry] = Field(description="Deck summaries.")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "count": 2,
                    "decks": [
                        {
                            "name": "My stick is better than bacon",
                            "id": "2020bf3hf",
                            "date": "2020-09-05",
                            "author": "Niko Vanhatalo",
                        },
                        {
                            "name": "Royal Kebab (sauce blanche)",
                            "id": "2018ncqvvf",
                            "date": "2018-04-22",
                            "author": "Orpheus",
                        },
                    ],
                }
            ]
        }
    }


# --- Candidate response models (for OpenAPI documentation) ---


class CandidateNameResponse(BaseModel):
    """Candidate card entry in name mode."""

    card: str = Field(description="Card name.")
    score: float = Field(description="Relevance score.")
    average: int = Field(description="Average number of copies in matching decks.")
    deviation: float = Field(description="Standard deviation of copies.")


class CandidateFullResponse(BaseModel):
    """Candidate card entry in full mode."""

    card: CardResponse = Field(description="Full card information.")
    score: float = Field(description="Relevance score.")
    average: int = Field(description="Average number of copies in matching decks.")
    deviation: float = Field(description="Standard deviation of copies.")


# --- Search dimensions model ---


class CardSearchDimensionsResponse(BaseModel):
    """Available search dimensions and their possible values."""

    type: list[str] = Field(description="Card types.")
    clan: list[str] = Field(description="Clans and creeds.")
    discipline: list[str] = Field(description="Discipline trigrams.")
    sect: list[str] = Field(description="Vampiric sects.")
    title: list[str] = Field(description="Titles.")
    group: list[str] = Field(description="Groups.")
    trait: list[str] = Field(description="Traits.")
    bonus: list[str] = Field(description="Bonuses.")
    capacity: list[str] = Field(description="Capacities.")
    city: list[str] = Field(description="Cities.")
    set: list[str] = Field(description="Sets.")
    rarity: list[str] = Field(description="Rarities.")
    precon: list[str] = Field(description="Preconstructed decks.")
    artist: list[str] = Field(description="Artists.")
    model_config = {
        "extra": "allow",
        "json_schema_extra": {
            "examples": [
                {
                    "type": [
                        "Action",
                        "Action Modifier",
                        "Ally",
                        "Combat",
                        "Equipment",
                        "Master",
                        "Political Action",
                        "Reaction",
                        "Retainer",
                        "Vampire",
                    ],
                    "clan": [
                        "Brujah",
                        "Gangrel",
                        "Malkavian",
                        "Nosferatu",
                        "Toreador",
                        "Tremere",
                        "Ventrue",
                    ],
                    "discipline": [
                        "AUS",
                        "CEL",
                        "DOM",
                        "OBF",
                        "POT",
                        "PRE",
                        "aus",
                        "cel",
                        "dom",
                        "obf",
                        "mono",
                        "multi",
                        "combo",
                        "none",
                    ],
                    "sect": [
                        "Anarch",
                        "Camarilla",
                        "Independent",
                        "Laibon",
                        "Sabbat",
                    ],
                    "title": [
                        "1 vote",
                        "2 votes",
                        "Archbishop",
                        "Baron",
                        "Prince",
                        "Primogen",
                        "Justicar",
                        "Inner Circle",
                    ],
                    "group": ["1", "2", "3", "4", "5", "6", "7"],
                    "trait": [
                        "Black Hand",
                        "Infernal",
                        "Red List",
                        "Scarce",
                        "Seraph",
                    ],
                    "bonus": [
                        "Bleed",
                        "Intercept",
                        "Stealth",
                        "Votes",
                    ],
                    "capacity": [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                    ],
                    "city": [
                        "Chicago",
                        "London",
                        "New York",
                        "Paris",
                        "Washington, D.C.",
                    ],
                    "set": [
                        "Fifth Edition",
                        "Jyhad",
                        "Keepers of Tradition",
                        "New Blood",
                        "Sabbat War",
                        "Vampire: The Eternal Struggle",
                    ],
                    "rarity": ["Common", "Rare", "Uncommon", "Vampire"],
                    "precon": [
                        "Fifth Edition: Malkavian",
                        "Fifth Edition: Ventrue",
                        "First Blood: Tremere",
                        "New Blood: Nosferatu",
                    ],
                    "artist": [
                        "Melissa Benson",
                        "Monte Moore",
                        "Ginés Quiñonero-Santiago",
                        "Tim Bradstreet",
                    ],
                }
            ]
        },
    }
