import requests


def test_submit_ruling(client, monkeypatch):
    class SessionMock:
        called = False

        @classmethod
        def post(cls, *args, **kwargs):
            cls.called = True
            cls.args = args
            cls.kwargs = kwargs
            cls.ok = True
            cls.status_code = 201
            return cls

        @classmethod
        def json(cls):
            return {"response": "ok"}

    monkeypatch.setattr(requests, "session", lambda: SessionMock)
    response = client.post(
        "/submit-ruling/Arson", json={"text": "foo", "link": "http://example.com"}
    )
    assert response.status_code == 400
    response = client.post(
        "/submit-ruling/Arson", json={"text": "foo", "link": "http://www.vekn.net"}
    )
    assert response.status_code == 201
    assert response.json == {"response": "ok"}
    assert SessionMock.called
    assert SessionMock.auth == (None, None)
    assert SessionMock.args == (
        "https://api.github.com/repos/lionel-panhaleux/krcg/issues",
        '{"title": "Arson", "body": "- **text:** foo\\n- **link:** '
        'http://www.vekn.net"}',
    )
    assert SessionMock.kwargs == {}
    assert SessionMock.ok
