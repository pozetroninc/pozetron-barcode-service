from base64 import b64encode
import json

import pytest


from .mocks.requests import (
    mocked_requests_post,
    SOME_VALID_RECAPTCHA_API_URL,
    SOME_TIMING_OUT_RECAPTCHA_API_URL,
    SOME_UNVALID_JSON_RECAPTCHA_API_URL,
    SOME_EXAMPLE_ALLOWED_HOSTNAMES,
    SOME_UNVALID_HOSTNAME,
    SOME_VALID_RECAPTCHA_TOKEN,
    SOME_UNVALID_RECAPTCHA_TOKEN,
    SOME_EXPIRED_RECAPTCHA_TOKEN,
    SOME_UNVALID_HOSTNAME_RECAPTCHA_TOKEN
)


BAD_REQUEST_INVALID_PARAMS = {
    'title': '400 Bad Request',
    'description': 'Invalid parameters. Required: "text" or "base64"'
}

BAD_REQUEST_RECAPTCHA_REQUIRED = {
    'title': '400 Bad Request',
    'description': 'reCAPTCHA token required'
}

BAD_REQUEST_COULD_NOT_VERIFY_ROBOT = {
    'title': '400 Bad Request',
    'description': 'Could not verify you are not a robot'
}

BAD_REQUEST_INVALID_RECAPTCHA = {
    'title': '400 Bad Request',
    'description': 'Invalid reCAPTCHA'
}

BAD_REQUEST_RECAPTCHA_EXPIRED = {
    'title': '400 Bad Request',
    'description': 'reCAPTCHA token expired'
}


@pytest.fixture
def abracadabra_png(datadir):
    with open(datadir['abracadabra_scale4.png'].strpath, 'rb') as file:
        return file.read()


def test_get_barcode(client):
    response = client.simulate_get_png('/', query_string='text=abracadabra')
    assert response.status_code == 405
    assert response.content == b''


def test_post_barcode_invalid(client):
    response = client.simulate_post_png('/',
                                        body='{"text":"abracadabra"}',
                                        headers={'Content-Type': 'application/json'})
    assert response.status_code == 415
    assert response.json == {
        'title': 'Unsupported media type',
        'description': 'Use application/x-www-form-urlencoded'
    }


def test_post_barcode(mocker, monkeypatch, client, abracadabra_png):
    
    # First, ensure predictable recaptcha configs
    monkeypatch.setattr('tests.mocks.requests.RECAPTCHA_ALLOWED_HOSTNAMES', SOME_EXAMPLE_ALLOWED_HOSTNAMES)
    monkeypatch.setattr('tests.mocks.requests.RECAPTCHA_EXPIRES_IN', 60)

    monkeypatch.setattr('pozetron_barcode.barcode.models.RECAPTCHA_API_URL', SOME_VALID_RECAPTCHA_API_URL)
    monkeypatch.setattr('pozetron_barcode.barcode.models.RECAPTCHA_ALLOWED_HOSTNAMES', SOME_EXAMPLE_ALLOWED_HOSTNAMES)
    monkeypatch.setattr('pozetron_barcode.barcode.models.RECAPTCHA_EXPIRES_IN', 60)
    monkeypatch.setattr('pozetron_barcode.barcode.models.RECAPTCHA_MAX_RETRY_TIME', 2) # in order for 'backoff' fails quickly
    
    # Then, mock requests.post, then continue with tests
    m = mocker.patch('pozetron_barcode.barcode.models.requests.post', side_effect=mocked_requests_post)
    
    # No params, no recaptcha
    response = client.simulate_post_png('/')
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_PARAMS
    
    # No params, valid recaptcha
    response = client.simulate_post_png('/', params={'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_PARAMS

    # Invalid params, valid recaptcha
    response = client.simulate_post_png('/', params={'invalid': 'invalid', 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_PARAMS

    # Valid params, no recaptcha
    response = client.simulate_post_png('/', params={'text': 'abracadabra'})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_RECAPTCHA_REQUIRED
    
    # Valid params, unvalid recaptcha
    response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_UNVALID_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_RECAPTCHA

    # Valid params, expired recaptcha
    response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_EXPIRED_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_RECAPTCHA_EXPIRED

    # Valid params, valid recaptcha, get barcode from text
    response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert response.content == abracadabra_png

    # Valid params, valid recaptcha but unvalid hostname
    response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_UNVALID_HOSTNAME_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_RECAPTCHA

    # Valid params, valid recaptcha, timeout
    with monkeypatch.context() as mp:
        mp.setattr('pozetron_barcode.barcode.models.RECAPTCHA_API_URL', SOME_TIMING_OUT_RECAPTCHA_API_URL)
        response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
        assert response.status_code == 400
        assert response.json == BAD_REQUEST_COULD_NOT_VERIFY_ROBOT

    # Valid params, valid recaptcha, unvalid recaptcha json response
    with monkeypatch.context() as mp:
        mp.setattr('pozetron_barcode.barcode.models.RECAPTCHA_API_URL', SOME_UNVALID_JSON_RECAPTCHA_API_URL)
        response = client.simulate_post_png('/', params={'text': 'abracadabra', 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
        assert response.status_code == 400
        assert response.json == BAD_REQUEST_COULD_NOT_VERIFY_ROBOT

    # Valid params, valid recaptcha, get barcode from base64
    abracadabra_base64 = b64encode(b'abracadabra').decode('ascii')
    response = client.simulate_post_png('/', params={'base64': abracadabra_base64, 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert response.content == abracadabra_png

    # Valid params, valid recaptcha, invalid base64
    response = client.simulate_post_png('/', params={'base64': 'AAA', 'recaptcha': SOME_VALID_RECAPTCHA_TOKEN})
    assert response.status_code == 400
    assert response.json == {
        'title': '400 Bad Request',
        'description': 'Invalid base64'
    }
