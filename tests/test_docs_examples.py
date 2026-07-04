"""Guard the documented request examples against drift.

The ``json_schema_extra`` examples on the request models are the API
documentation shown in the docs UIs. If one stops matching the schema or the
handler, these tests fail (a 422 means the example is no longer valid input;
a 500 means it crashes the handler).
"""

from krcg_api.models import (
    CandidatesRequest,
    CardSearchRequest,
    DeckSearchRequest,
)


def _examples(model) -> list[dict]:
    return model.model_config["json_schema_extra"]["examples"]


def _assert_handled(response, path):
    assert response.status_code not in (422, 500), (
        f"{path} rejected its own documented example "
        f"({response.status_code}): {response.text}"
    )


def test_deck_search_examples_round_trip(client):
    for example in _examples(DeckSearchRequest):
        for path in ("/twda", "/twda/list", "/twda/random"):
            _assert_handled(client.post(path, json=example), path)


def test_candidates_example_round_trips(client):
    for example in _examples(CandidatesRequest):
        _assert_handled(client.post("/candidates", json=example), "/candidates")


def test_card_search_example_round_trips(client):
    for example in _examples(CardSearchRequest):
        response = client.post("/card_search", json=example)
        _assert_handled(response, "/card_search")
        assert isinstance(response.json(), list)


def test_path_filter_is_wired(client):
    """The ``path`` dimension reaches krcg's search()."""
    response = client.post("/card_search", json={"path": ["Caine"]})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
