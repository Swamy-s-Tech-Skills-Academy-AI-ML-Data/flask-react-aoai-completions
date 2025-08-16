import json


def test_completions_missing_prompt(client):
    resp = client.post('/api/completions', data=json.dumps({}),
                       content_type='application/json')
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['error']


def test_completions_success(client):
    resp = client.post('/api/completions', json={'prompt': 'Hello'})
    # content_type currently text/event-stream; read raw text
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert 'Test completion response' in text
