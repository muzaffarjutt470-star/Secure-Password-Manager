from .conftest import register, login


def test_security_headers(client):
    r = client.get('/')

    assert r.headers['X-Content-Type-Options'] == 'nosniff'
    assert r.headers['X-Frame-Options'] == 'DENY'
    assert 'default-src' in r.headers['Content-Security-Policy']


def test_csrf_required(client):
    register(client)
    login(client)

    r = client.post(
        '/vault/new',
        data={
            'title': 'x',
            'password': 'y'
        }
    )

    assert r.status_code == 400
