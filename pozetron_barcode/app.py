# -*- coding: utf-8 -*-
"""
App runner
"""
# System imports
from __future__ import absolute_import
# Third-party imports
import falcon
from falcon_cors import CORS


# Local imports
try:
    from barcode.models import BarcodeResource
    from healthcheck.healthz import HealthCheck  # pragma: nocover
except ImportError:
    from pozetron_barcode.barcode.models import BarcodeResource
    from pozetron_barcode.healthcheck.healthz import HealthCheck


cors = CORS(allow_origins_regex='http://localhost:')


# Create resources
barcode = BarcodeResource()
health_check = HealthCheck()


# Create falcon app
app = falcon.API(middleware=[cors.middleware])
app.req_options.auto_parse_form_urlencoded = True
app.add_route('/healthz/', health_check)
app.add_route('/', barcode)


# Useful for debugging problems in API, it works with pdb
if __name__ == '__main__':
    from wsgiref import simple_server  # NOQA  # pragma: nocover
    httpd = simple_server.make_server('127.0.0.1', 9001, app)  # pragma: nocover
    httpd.serve_forever()  # pragma: nocover
