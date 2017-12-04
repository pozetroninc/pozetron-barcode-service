from base64 import b64decode
from io import BytesIO

import falcon
import pyqrcode as qrcode


class BarcodeResource:

    @staticmethod
    def on_get(req, resp):
        # Get data (bytes) from request
        try:
            if len(req.params) != 1:
                raise KeyError
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
