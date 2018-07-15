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


## App configuration (`.env`)

| Key                                   | Type     | Description     |
| :---                                  | :---     | :---            |
| **FALCON_SETTINGS_MODULE**            | Required | Which python settings module from `poztron_barcode/settings/` to use.  |
| **DEBUG**                             | Optional | If set to `true`, enables logging of http requests into `stdout`. Defaults to `false`.  |
| **REDIS_HOST**                        | Optional | Redis hostname for frontend color scheme logging. Defaults to `redis` |
| **REDIS_PORT**                        | Optional | Redis port. Defaults to `6379` |
| **REDIS_DB**                          | Optional | Redis db. Defaults to `0` |
| **RECAPTCHA_SECRET**                  | Optional | Google Recaptcha v3 secret key. If provided, activates recaptcha checks, by requiring an extra `recaptch` arg in http requests. |
| **RECAPTCHA_ALLOWED_HOSTNAMES_JSON**  | Optional | List of allowed frontend hostnames in recaptcha checks. Required if `RECAPTCHA_SECRET` provided. |
| **RECAPTCHA_EXPIRES_IN**      | Optional | Seconds to frontend recaptcha tokens expiry. Defaults to `60` |
| **RECAPTCHA_MAX_RETRY_TIME**          | Optional | Max retry time in seconds for recaptcha check retries in case of network failures to Google servers. Defaults to `60` |
| **RECAPTCHA_SHOULD_LOG_RETRIES**      | Optional | If set to `true`, logs network failures of recaptcha checks into `stdout`. Defaults to `false` |


## Testing

Using tox:

    tox

Or running pytest only:

    pip install -r requirements/test-requirements.txt
    pytest tests --cov=pozetron_barcode
