from base64 import b64encode
import pytest


BAD_REQUEST_INVALID_PARAMS = {
    'title': '400 Bad Request',
    'description': 'Invalid parameters. Required: "text" or "base64"'
}


@pytest.fixture
def abracadabra_png(datadir):
    with open(datadir['abracadabra_scale4.png'].strpath, 'rb') as file:
        return file.read()


def test_get_barcode(client):
    response = client.simulate_get_png('/', query_string='text=abracadabra')
    assert response.status_code == 405
    assert response.content == b''


def test_post_barcode(client, abracadabra_png):
    # No params
    response = client.simulate_post_png('/')
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_PARAMS

    # Invalid params
    response = client.simulate_post_png('/', params={'invalid': 'invalid'})
    assert response.status_code == 400
    assert response.json == BAD_REQUEST_INVALID_PARAMS

    # Get barcode from text
    response = client.simulate_post_png('/', params={'text': 'abracadabra'})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert response.content == abracadabra_png

    # Get barcode from base64
    abracadabra_base64 = b64encode(b'abracadabra').decode('ascii')
    response = client.simulate_post_png('/', params={'base64': abracadabra_base64})
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert response.content == abracadabra_png

    # Invalid base64
    response = client.simulate_post_png('/', params={'base64': 'AAA'})
    assert response.status_code == 400
    assert response.json == {
        'title': '400 Bad Request',
        'description': 'Invalid base64'
    }
