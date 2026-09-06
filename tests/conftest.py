import re

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SECRET_KEY": "test-secret-key",
        "RATELIMIT_ENABLED": False,
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def csrf(client):
    r = client.get("/auth/register")
    assert r.status_code == 200

    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        r.get_data(as_text=True)
    )

    assert match is not None, "CSRF token not found on registration page"
    return match.group(1)


def token(client, path):
    r = client.get(path)
    assert r.status_code == 200

    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        r.get_data(as_text=True)
    )

    assert match is not None, f"CSRF token not found on {path}"
    return match.group(1)


def register(client, username="testuser", password="StrongPassword123!"):
    token_value = csrf(client)

    return client.post(
        "/auth/register",
        data={
            "username": username,
            "password": password,
            "csrf_token": token_value,
        },
        follow_redirects=False,
    )


def login(client, username="testuser", password="StrongPassword123!"):
    token_value = csrf(client)

    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
            "csrf_token": token_value,
        },
        follow_redirects=False,
    )
