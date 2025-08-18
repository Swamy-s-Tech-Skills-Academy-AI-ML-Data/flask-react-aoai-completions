import pytest


def test_404_returns_json_error(client):
    resp = client.get('/definitely-not-here')
    assert resp.status_code == 404
    data = resp.get_json()
    # Should have consistent JSON error shape
    assert isinstance(data, dict)
    assert 'error' in data
    assert data['error']


def test_unhandled_exception_returns_500_json(client):
    app = client.application

    # Dynamically add a route that will raise an exception
    @app.route('/boom-test')
    def boom():  # pragma: no cover
        raise RuntimeError("Boom")

    resp = client.get('/boom-test')
    assert resp.status_code == 500
    data = resp.get_json()
    assert data == {'error': 'Internal server error'}
