def test_heathz(monkeypatch, client):
    # With Debug = True
    with monkeypatch.context() as mp:
        mp.setattr('pozetron_barcode.app.DEBUG', True)
        response = client.simulate_get('/healthz/')
        assert response.status_code == 200
        # NOTE: this is actually wrong because content is not a valid JSON
        assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
        assert response.content == b'GOOD'
    
    # With Debug = False
    with monkeypatch.context() as mp:
        mp.setattr('pozetron_barcode.app.DEBUG', False)
        response = client.simulate_get('/healthz/')
        assert response.status_code == 200
        # NOTE: this is actually wrong because content is not a valid JSON
        assert response.headers['Content-Type'] == 'application/json; charset=UTF-8'
        assert response.content == b'GOOD'
