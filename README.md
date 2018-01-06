# barcode-service

This is a microservice used to generate barcodes (currently QR codes)

## Quickstart

Start Docker

    docker-compose up

Get a QR code using [HTTPie](https://httpie.org/):

    http -v --form POST http://localhost:9001 text=abracadabra --download -o qrcode.png
    http -v --form POST http://localhost:9001 base64=YWJyYWNhZGFicmE= --download -o qrcode.png

Note that only `application/x-www-form-urlencoded` is allowed.

## Testing

Using tox:

    tox

Or running pytest only:

    pip install -r requirements/test-requirements.txt
    pytest tests --cov=pozetron_barcode

## License
    Copyright 2018 Pozetron Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
