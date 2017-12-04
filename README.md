# barcode-service

This is the microservice used to generate barcodes (mostly QR codes)

## Quickstart

Start Docker

    docker-compose up

Get QR code via browser:

- http://localhost:9001?text=some-text

- http://localhost:9001?base64=c29tZS10ZXh0

## Testing

Using tox:

    tox

Or running pytest only:

    pip install -r requirements/test-requirements.txt
    pytest tests --cov=pozetron_barcode
