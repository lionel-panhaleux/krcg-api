import arrow
import babel
import flask
import io
import json
import logging
import math
import os
import pkg_resources  # part of setuptools
import random
import requests
import urllib.parse
import urllib.request

from krcg import analyzer
from krcg import deck
from krcg import twda
from krcg import utils as krcg_utils
from krcg import vtes

from . import config


class KRCG(flask.Flask):
    """Base API class for Access-Control headers handling."""

    def make_default_options_response(self) -> flask.Response:
        response = super().make_default_options_response()
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    def process_response(self, response: flask.Response) -> flask.Response:
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(levelname)7s] %(message)s")
base = flask.Blueprint("base", "krcg")


def create_app():
    vtes.VTES.load()
    twda.TWDA.load()
    logger.info("launching app")
    app = KRCG(__name__)
    app.register_blueprint(base)
    return app


@base.route("/")
@base.route("/index.html")
def swagger():
    """Swagger doc display."""
    return flask.render_template("index.html")


@base.route("/openapi.yaml")
def openapi():
    """OpenAPI schema."""
    return flask.render_template(
        "openapi.yaml",
        version=pkg_resources.require("krcg-api")[0].version,
    )


@base.route("/card/<text>")
def card(text):
    """Get a card."""
    try:
        text = int(text)
    except ValueError:
        text = urllib.parse.unquote(text)
    try:
        return flask.jsonify(vtes.VTES[text].to_json())
    except KeyError:
        return "Card not found", 404


@base.route("/twda", methods=["POST"])
def deck_search():
    """Get decks containing cards."""
    data = flask.request.get_json() or {}
    if data and data.get("player"):
        decks = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data["player"])]
        ]
    else:
        decks = twda.TWDA.values()
    if data and data.get("players_count"):
        decks = [
            d for d in decks if (d.players_count or 0) >= int(data["players_count"])
        ]
    if data and data.get("date_from"):
        decks = [d for d in decks if d.date >= arrow.get(data["date_from"]).date()]
    if data and data.get("date_to"):
        decks = [d for d in decks if d.date < arrow.get(data["date_to"]).date()]
    if data and data.get("cards"):
        try:
            cards = set(vtes.VTES[c] for c in data["cards"])
        except KeyError as e:
            return f"Invalid card name: {e.args}", 400
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        return "No result in TWDA", 404
    return flask.jsonify([d.to_json() for d in decks])


@base.route("/twda/list", methods=["POST"])
def deck_list():
    """Get list of available TWDA decks"""
    data = flask.request.get_json() or {}
    if data and data.get("player"):
        decks = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data["player"])]
        ]
    else:
        decks = twda.TWDA.values()
    if data and data.get("players_count"):
        decks = [
            d for d in decks if (d.players_count or 0) >= int(data["players_count"])
        ]
    if data and data.get("date_from"):
        decks = [d for d in decks if d.date >= arrow.get(data["date_from"]).date()]
    if data and data.get("date_to"):
        decks = [d for d in decks if d.date < arrow.get(data["date_to"]).date()]
    if data and data.get("cards"):
        try:
            cards = set(vtes.VTES[c] for c in data["cards"])
        except KeyError as e:
            return f"Invalid card name: {e.args}", 400
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        return "No result in TWDA", 404

    decklist = {
        "count": len(decks),
        "decks": [
            {"name": d.name, "id": d.id, "date": d.date, "author": d.author}
            for d in decks
        ],
    }
    return flask.jsonify(decklist)


@base.route("/twda/<twda_id>")
def deck_by_id(twda_id):
    """Get a deck given its ID."""
    if not twda_id:
        return "Bad Request", 400
    if twda_id not in twda.TWDA:
        return "Not Found", 404
    return flask.jsonify(twda.TWDA[twda_id].to_json())


@base.route("/twda/random", methods=["POST"])
def random_deck():
    """Get TWDA decks containing cards."""
    data = flask.request.get_json() or {}
    if data and data.get("player"):
        decks = [
            twda.TWDA[id_]
            for id_ in twda.TWDA.by_author[krcg_utils.normalize(data["player"])]
        ]
    else:
        decks = list(twda.TWDA.values())
    if data and data.get("players_count"):
        decks = [
            d for d in decks if (d.players_count or 0) >= int(data["players_count"])
        ]
    if data and data.get("date_from"):
        decks = [d for d in decks if d.date >= arrow.get(data["date_from"]).date()]
    if data and data.get("date_to"):
        decks = [d for d in decks if d.date < arrow.get(data["date_to"]).date()]
    if data and data.get("cards"):
        try:
            cards = set(vtes.VTES[c] for c in data["cards"])
        except KeyError as e:
            return f"Invalid card name: {e.args}", 400
        decks = [d for d in decks if all(c in d for c in cards)]
    if not decks:
        return "No result in TWDA", 404

    return flask.jsonify(random.choice(decks).to_json())


@base.route("/convert", methods=["POST"])
@base.route("/convert/<format>", methods=["POST"])
def convert(format="json"):
    raw_data = flask.request.get_data()
    if flask.request.json:
        d = deck.Deck()
        d.from_json(flask.request.json)
    else:
        try:
            text = io.StringIO(raw_data.decode("utf-8"))
            d = deck.Deck.from_txt(text)
        except UnicodeDecodeError:
            return "Failed to decode text/plain data in utf-8", 400
    if format in ["twd", "lackey", "jol"]:
        return d.to_txt(format).encode("utf-8")
    else:
        return flask.jsonify(d.to_json())


@base.route("/amaranth", methods=["POST"])
def amaranth():
    data = flask.request.form or flask.request.json
    if "url" not in data:
        return "Missing required parameter: url", 400
    url = data["url"]
    if url[:34] != "https://amaranth.vtes.co.nz/#deck/":
        return "Amaranth URL required", 400
    return flask.jsonify(deck.Deck.from_amaranth(url[34:]).to_json())


@base.route("/vdb", methods=["POST"])
def vdb():
    data = flask.request.form or flask.request.json
    if "url" not in data:
        return "Missing required parameter: url", 400
    url = data["url"]
    if url[:32] != "https://vdb.smeea.casa/decks?id=":
        return "VDB URL required", 400
    return flask.jsonify(deck.Deck.from_vdb(url[32:]).to_json())


@base.route("/candidates", methods=["POST"])
def candidates():
    data = flask.request.get_json() or {}
    full = data.pop("mode", "") == "full"
    decks = twda.TWDA.values()
    if data and data.get("players_count"):
        decks = [
            d for d in decks if (d.players_count or 0) >= int(data.pop("players_count"))
        ]
    if data and data.get("date_from"):
        date = data.pop("date_from")
        decks = [d for d in decks if d.date >= arrow.get(date).date()]
    if data and data.get("date_to"):
        date = data.pop("date_to")
        decks = [d for d in decks if d.date < arrow.get(date).date()]
    try:
        cards = [vtes.VTES[c] for c in data.pop("cards", [])]
        A = analyzer.Analyzer(decks)
        A.refresh(*cards)
        if len(A.examples) < 4:
            return "Too few examples in TWDA", 404
        if cards:
            ret = A.candidates(*cards, spoiler_multiplier=1)[:10]
        else:
            ret = A.played.most_common()[:10]
        if full:
            return flask.jsonify(
                [
                    {
                        "card": c.to_json(),
                        "score": round(s / (1 if cards else len(decks)), 4),
                        "average": round(A.average[c]),
                        "deviation": round(math.sqrt(A.variance[c]), 2),
                    }
                    for c, s in ret
                ]
            )
        else:
            return flask.jsonify(
                [
                    {
                        "card": c.name,
                        "score": round(s / (1 if cards else len(decks)), 4),
                        "average": round(A.average[c]),
                        "deviation": round(math.sqrt(A.variance[c]), 2),
                    }
                    for c, s in ret
                ]
            )
    except KeyError as e:
        return f"Invalid card name: {e.args}", 400


@base.route("/complete/<text>")
def complete(text):
    """Card name completion."""
    lang = _negotiate_locale(flask.request.accept_languages.values())
    return flask.jsonify(vtes.VTES.complete(urllib.parse.unquote(text), lang))


@base.route("/card_search", methods=["POST"])
def card_search():
    """Card search."""
    data = flask.request.get_json() or {}
    full = data.pop("mode", "") == "full"
    if data.get("lang"):
        data["lang"] = _negotiate_locale([data["lang"]])
    try:
        result = sorted(vtes.VTES.search(**data), key=lambda c: c.name)
    except ValueError as e:
        return str(e), 400
    if full:
        result = [c.to_json() for c in result]
    else:
        result = [c.name for c in result]
    return flask.jsonify(result)


@base.route("/card_search", methods=["GET"])
def card_search_dimensions():
    """Card search dimensions."""
    return flask.jsonify(vtes.VTES.search_dimensions)


@base.route("/submit-ruling/<card>", methods=["POST"])
def submit_ruling(card):
    """Submit a new ruling proposal.

    This posts an issue on the project Github repository.
    """
    try:
        card = int(card)
    except ValueError:
        pass
    try:
        card = vtes.VTES[card].name
    except KeyError:
        return "Card not found", 404
    data = flask.request.get_json() or {}
    text = data.get("text")
    link = data.get("link")
    if not (text and link):
        return "Invalid ruling data", 400
    if urllib.parse.urlparse(link).hostname not in {
        "boardgamegeek.com",
        "www.boardgamegeek.com",
        "groups.google.com",
        "www.vekn.net",
    }:
        return "Invalid ruling link", 400
    tryout = requests.get(link, stream=True)
    if not tryout.ok:
        return "Invalid ruling link", tryout.status_code

    url = "https://api.github.com/repos/lionel-panhaleux/krcg/issues"
    issue = {
        "title": card,
        "body": f"- **text:** {text}\n- **link:** {link}",
    }
    session = requests.session()
    session.auth = (os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"))
    response = session.post(url, json.dumps(issue))
    if response.ok:
        return flask.jsonify(response.json()), response.status_code
    else:
        return response.text, response.status_code


def _negotiate_locale(preferred):
    res = babel.negotiate_locale(
        [x.replace("_", "-") for x in preferred],
        ["en"] + list(config.SUPPORTED_LANGUAGES),
        sep="-",
    )
    # negotiation is case-insensitive but the result uses the case of the first argument
    if res:
        res = res[:2]
    return res
