from base64 import b64decode
from datetime import datetime, timezone
from io import BytesIO

import backoff
import dateutil.parser
import falcon
import pyqrcode as qrcode
import requests

from pozetron_barcode.settings import (
    RECAPTCHA_API_URL,
    RECAPTCHA_SECRET,
    RECAPTCHA_ALLOWED_HOSTNAMES,
    RECAPTCHA_EXPIRES_IN,
    RECAPTCHA_MAX_RETRY_TIME
)

class RecaptchaRequestException(Exception):
    pass


def backoff_handler(details):
    raise falcon.HTTPBadRequest(description='Could not verify you are not a robot')


class BarcodeResource:

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        RecaptchaRequestException,
        max_time=RECAPTCHA_MAX_RETRY_TIME,
        on_backoff=backoff_handler
    )
    def on_post(req, resp):
        if not req.content_type or req.content_type.split(';')[0] != 'application/x-www-form-urlencoded':
            raise falcon.HTTPUnsupportedMediaType(description='Use application/x-www-form-urlencoded')
        # Get data (bytes) from request
        try:
            if 'base64' in req.params:
                try:
                    data = b64decode(req.params['base64'])
                except ValueError:
                    raise falcon.HTTPBadRequest(description='Invalid base64')
            elif 'text' in req.params:
                data = req.params['text'].encode('ascii')
            else:
                raise KeyError
        except KeyError:
            raise falcon.HTTPBadRequest(description='Invalid parameters. Required: "text" or "base64"')
        
        # Verify recaptcha
        if 'recaptcha' in req.params:
            try:
                r = requests.post(RECAPTCHA_API_URL, data = {
                    'secret': RECAPTCHA_SECRET,
                    'response': req.params['recaptcha']
                })
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                raise RecaptchaRequestException()
            try:
                result = r.json()
            except ValueError:
                raise falcon.HTTPBadRequest(description='Could not verify you are not a robot')
            if not result.get('success'):
                raise falcon.HTTPBadRequest(description='Invalid recaptcha')
            if result.get('hostname') not in RECAPTCHA_ALLOWED_HOSTNAMES:
                raise falcon.HTTPBadRequest(description='Invalid recaptcha')
            challenge_time = dateutil.parser.parse(result.get('challenge_ts'))
            now = datetime.now(timezone.utc)
            if (now - challenge_time).total_seconds() > RECAPTCHA_EXPIRES_IN:
                raise falcon.HTTPBadRequest(description='Recaptcha token expired')
        else:
            raise falcon.HTTPBadRequest(description='Recaptcha token required')
        
        return BarcodeResource._generate_barcode(req, resp, data)

    @staticmethod
    def _generate_barcode(req, resp, data):
        # Disable file_wrapper to make BytesIO work
        # See https://github.com/unbit/uwsgi/issues/1126#issuecomment-166687767
        del req.env['wsgi.file_wrapper']

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_PNG
        qr = qrcode.create(data)
        file = BytesIO()
        qr.png(file, scale=4)
        resp.stream_len = file.tell()  # set Content-Length
        file.seek(0)
        resp.stream = file
