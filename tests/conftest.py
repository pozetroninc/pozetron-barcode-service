from falcon.testing import TestClient
import pytest
import os


class CustomTestClient(TestClient):
    """DRY test client for barcode-related stuff."""

    def simulate_get_png(self, *args, **kw):
        self._add_file_wrapper(kw)
        return super().simulate_get(*args, **kw)

    def simulate_post_png(self, *args, **kw):
        self._add_file_wrapper(kw)
        # If Content-Type is not specified explicitly, set application/x-www-form-urlencoded
        try:
            headers = kw['headers']
        except KeyError:
            headers = kw['headers'] = {}
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return super().simulate_post(*args, **kw)

    def _add_file_wrapper(self, kw):
        # Tests are a bit different from real WSGI server: they don't have env['wsgi.file_wrapper'].
        # We add it here, but Falcon app removes it from request
        # to make it work with BytesIO.
        # This is just to avoid unnecessary try-except code in production.
        if 'file_wrapper' not in kw:
            kw['file_wrapper'] = lambda x: x


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setitem(os.environ, 'DEBUG', 'true')
    from pozetron_barcode.app import app
    return CustomTestClient(app)
