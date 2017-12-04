from falcon.testing import TestClient
import pytest

from pozetron_barcode.app import app


class CustomTestClient(TestClient):
    """DRY test client for barcode-related stuff."""

    def simulate_get_png(self, *args, **kw):
        self._add_file_wrapper(kw)
        return super().simulate_get(*args, **kw)

    def _add_file_wrapper(self, kw):
        # Tests are a bit different from real WSGI server: they don't have env['wsgi.file_wrapper'].
        # We add it here, but Falcon app removes it from request
        # to make it work with BytesIO.
        # This is just to avoid unnecessary try-except code in production.
        if 'file_wrapper' not in kw:
            kw['file_wrapper'] = lambda x: x


@pytest.fixture
def client():
    return CustomTestClient(app)
