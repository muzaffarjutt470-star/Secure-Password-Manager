import secrets
from flask import session

TOKEN_KEY = "csrf_token"


def csrf_token():
    if TOKEN_KEY not in session:
        session[TOKEN_KEY] = secrets.token_urlsafe(32)
    return session[TOKEN_KEY]


def validate_csrf(token):
    return bool(token) and secrets.compare_digest(token, session.get(TOKEN_KEY, ""))
