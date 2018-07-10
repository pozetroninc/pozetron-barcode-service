def test_heathz(monkeypatch, client):
    response = client.simulate_get('/healthz/')
    assert response.status_code == 200
    # NOTE: this is actually wrong because content is not a valid JSON
    assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
    assert response.content == b'GOOD'
