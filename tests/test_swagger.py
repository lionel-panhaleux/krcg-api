def test_root_redirects_to_scalar(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/scalar"


def test_docs_uis_are_served(client):
    """Scalar (pretty default), Swagger UI and ReDoc are all available."""
    for path in ("/scalar", "/docs", "/redoc"):
        response = client.get(path)
        assert response.status_code == 200, path
        assert "text/html" in response.headers["content-type"], path


def test_openapi_operation_ids_are_clean(client):
    """operationIds are the bare handler names, for tidy generated SDKs."""
    schema = client.get("/openapi.json").json()
    assert schema["info"]["title"] == "KRCG API"
    op_ids = {
        op["operationId"]
        for path in schema["paths"].values()
        for method, op in path.items()
        if method in {"get", "post", "put", "patch", "delete"}
    }
    assert {"card", "card_search", "candidates", "deck_search", "amaranth"} <= op_ids
    # No FastAPI-style "name_name_method" auto ids leaked through.
    assert not any("_post" in op_id or "_get" in op_id for op_id in op_ids)


def _array_enum(prop: dict) -> list | None:
    """Return the ``items.enum`` of an array property, optional or not."""
    candidates = [prop] if prop.get("type") == "array" else []
    candidates += [s for s in prop.get("anyOf", []) if s.get("type") == "array"]
    for arr in candidates:
        items = arr.get("items", {})
        if "enum" in items:
            return items["enum"]
    return None


def test_card_search_dimensions_injected_as_enums(client):
    """Every live search dimension is enumerated on the request schema."""
    dimensions = client.get("/card_search").json()
    schema = client.get("/openapi.json").json()
    props = schema["components"]["schemas"]["CardSearchRequest"]["properties"]
    for dimension, values in dimensions.items():
        assert dimension in props, dimension
        enum = _array_enum(props[dimension])
        assert enum is not None, f"{dimension} not enumerated"
        # Same set of values (normalise to str: group/capacity are ints in schema).
        assert {str(v) for v in enum} == {str(v) for v in values}, dimension
