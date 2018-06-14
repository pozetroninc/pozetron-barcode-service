import datetime

from requests.exceptions import Timeout

from pozetron_barcode.settings import (
    RECAPTCHA_ALLOWED_HOSTNAMES,
    RECAPTCHA_EXPIRES_IN
)

# Example data
SOME_VALID_RECAPTCHA_API_URL = 'https://www.google.com/validapi'
SOME_TIMING_OUT_RECAPTCHA_API_URL = 'https://www.google.com/timeout'
SOME_UNVALID_JSON_RECAPTCHA_API_URL = 'https://www.google.com/unvalidjson'

SOME_EXAMPLE_ALLOWED_HOSTNAMES = ['qrbarco.de', 'www.qrbarco.de']
SOME_UNVALID_HOSTNAME = 'www.unval.id'

SOME_VALID_RECAPTCHA_TOKEN = 'validtoken'
SOME_UNVALID_RECAPTCHA_TOKEN = 'unvalidtoken'
SOME_EXPIRED_RECAPTCHA_TOKEN = 'expiredtoken'

# Example recaptcha verification responses
SUCCESSFUL_RECAPTCHA_RESPONSE = {
    'success': True,
    'hostname': RECAPTCHA_ALLOWED_HOSTNAMES[0],
    'challenge_ts': datetime.datetime.now(datetime.timezone.utc).isoformat()
}

UNSUCCESSFUL_RECAPTCHA_RESPONSE = {
    'success': False
}

EXPIRED_RECAPTCHA_RESPONSE = {
    'success': True,
    'hostname': RECAPTCHA_ALLOWED_HOSTNAMES[0],
    'challenge_ts': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=RECAPTCHA_EXPIRES_IN+10)).isoformat()
}


def mocked_requests_post(*args, **kwargs):
    '''Mock for requests.post'''

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            if args[0] == SOME_UNVALID_JSON_RECAPTCHA_API_URL:
                raise ValueError
            return self.json_data
    
    if args[0] == SOME_VALID_RECAPTCHA_API_URL:
        if kwargs['data']['response'] == SOME_VALID_RECAPTCHA_TOKEN:
            return MockResponse(SUCCESSFUL_RECAPTCHA_RESPONSE, 200)
        if kwargs['data']['response'] == SOME_UNVALID_RECAPTCHA_TOKEN:
            return MockResponse(UNSUCCESSFUL_RECAPTCHA_RESPONSE, 200)
        if kwargs['data']['response'] == SOME_EXPIRED_RECAPTCHA_TOKEN:
            return MockResponse(EXPIRED_RECAPTCHA_RESPONSE, 200)

    # Unvalid url! timeout request.
    raise Timeout('Timeout error details')
