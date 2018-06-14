# barcode-service

This is the microservice used to generate barcodes (mostly QR codes)

## Quickstart

Configure service

    cp .env.example .env

    nano .env

Start Docker

    docker-compose up

Get QR code using [HTTPie](https://httpie.org/):

    http -v --form POST http://localhost:9001 text=abracadabra --download -o qrcode.png
    http -v --form POST http://localhost:9001 base64=YWJyYWNhZGFicmE= --download -o qrcode.png

Note that only `application/x-www-form-urlencoded` is allowed.

## Testing

Using tox:

    tox

Or running pytest only:

    pip install -r requirements/test-requirements.txt
    pytest tests --cov=pozetron_barcode
