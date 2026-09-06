import re

from .conftest import register, login


def token(client, path):
    response = client.get(path)
    assert response.status_code == 200

    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        response.get_data(as_text=True)
    )

    assert match is not None, f"CSRF token not found on {path}"
    return match.group(1)


def test_create_view_edit_delete(client):
    register(client)
    login(client)

    # Create credential
    t = token(client, "/vault/new")

    response = client.post(
        "/vault/new",
        data={
            "csrf_token": t,
            "title": "GitHub",
            "username": "alice",
            "password": "Very-Strong-Secret-123!",
            "url": "https://github.com",
            "category": "Work",
            "notes": "private",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"GitHub" in response.data

    # View credential
    response = client.get("/vault/1/view")

    assert response.status_code == 200
    assert b"Very-Strong-Secret-123!" in response.data

    # Edit credential
    t = token(client, "/vault/1/edit")

    response = client.post(
        "/vault/1/edit",
        data={
            "csrf_token": t,
            "title": "GitHub 2",
            "username": "alice2",
            "password": "New-Secret-123!",
            "url": "https://github.com",
            "category": "Work",
            "notes": "updated",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"GitHub 2" in response.data

    # Delete credential
    t = token(client, "/vault/1/edit")

    response = client.post(
        "/vault/1/delete",
        data={
            "csrf_token": t,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    # Dashboard should show an empty-vault state
    assert (
        b"No credentials yet" in response.data
        or b"No credentials" in response.data
        or b"Your vault is empty" in response.data
    )


def test_user_cannot_access_other_users_entry(client):
    # User Alice creates a credential
    register(client, "alice")
    login(client, "alice")

    t = token(client, "/vault/new")

    client.post(
        "/vault/new",
        data={
            "csrf_token": t,
            "title": "Alice Secret",
            "username": "a",
            "password": "Secret-123456!",
            "url": "",
            "category": "General",
            "notes": "",
        },
    )

    # Alice logs out
    logout_token = token(client, "/vault/")

    client.post(
        "/auth/logout",
        data={
            "csrf_token": logout_token,
        },
    )

    # User Bob logs in
    register(client, "bob")
    login(client, "bob")

    # Bob must not access Alice's credential
    response = client.get("/vault/1/view")

    assert response.status_code == 404


def test_export_contains_only_encrypted_fields(client):
    register(client)
    login(client)

    t = token(client, "/vault/new")

    client.post(
        "/vault/new",
        data={
            "csrf_token": t,
            "title": "Secret",
            "username": "alice",
            "password": "TopSecret-123!",
            "url": "",
            "category": "General",
            "notes": "hidden",
        },
    )

    response = client.get("/vault/export")
    text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "securevault-encrypted-v1" in text

    # Plaintext secrets must not appear in export
    assert "TopSecret-123!" not in text
    assert "alice" not in text
