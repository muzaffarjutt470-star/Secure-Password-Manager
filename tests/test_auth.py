import re

from .conftest import register, login


def get_csrf(client, path="/auth/register"):
    response = client.get(path)
    assert response.status_code == 200

    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        response.get_data(as_text=True)
    )

    assert match is not None, f"CSRF token not found on {path}"
    return match.group(1)


def test_register_and_login(client):
    response = register(client)

    assert response.status_code == 302

    response = login(client)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/vault/")


def test_short_password_rejected(client):
    token = get_csrf(client)

    response = client.post(
        "/auth/register",
        data={
            "csrf_token": token,
            "username": "alice",
            "password": "short",
        },
    )

    assert response.status_code == 400


def test_bad_login_rejected(client):
    register(client)

    token = get_csrf(client, "/auth/login")

    response = client.post(
        "/auth/login",
        data={
            "csrf_token": token,
            "username": "alice",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
