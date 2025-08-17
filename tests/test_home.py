def test_home_route_root(client):
    resp = client.get('/')
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert 'data' in json_data
    assert 'Welcome' in json_data['data']


def test_home_route_api_prefix(client):
    resp = client.get('/api/')
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert 'data' in json_data
