def test_completions_missing_prompt(client):
    resp = client.post('/api/completions', json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_completions_success(client):
    resp = client.post('/api/completions', json={'prompt': 'Hello'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['response'] == 'Test completion response'
    assert 'usage' in data and 'prompt_chars' in data['usage']
