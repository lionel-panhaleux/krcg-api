def test(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json is None
    assert (
        response.data[:95]
        == b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>KRCG API</title>
"""
    )
