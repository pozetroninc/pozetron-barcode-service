import datetime

from requests.exceptions import Timeout

# Example data
SOME_VALID_RECAPTCHA_SECRET = 'validrecaptchasecret'
SOME_UNVALID_RECAPTCHA_SECRET = 'unvalidrecaptchasecret'
SOME_VALID_RECAPTCHA_API_URL = 'https://www.google.com/validapi'
SOME_TIMING_OUT_RECAPTCHA_API_URL = 'https://www.google.com/timeout'
SOME_UNVALID_JSON_RECAPTCHA_API_URL = 'https://www.google.com/unvalidjson'

SOME_EXAMPLE_EXPIRY_TIME = 60

SOME_EXAMPLE_ALLOWED_HOSTNAMES = ['qrbarco.de', 'www.qrbarco.de']
SOME_UNVALID_HOSTNAME = 'www.unval.id'

SOME_VALID_RECAPTCHA_TOKEN = 'validtoken'
SOME_UNVALID_RECAPTCHA_TOKEN = 'unvalidtoken'
SOME_EXPIRED_RECAPTCHA_TOKEN = 'expiredtoken'
SOME_UNVALID_HOSTNAME_RECAPTCHA_TOKEN = 'unvalidhostnametoken'

# Example recaptcha verification responses
SUCCESSFUL_RECAPTCHA_RESPONSE = {
    'success': True,
    'hostname': SOME_EXAMPLE_ALLOWED_HOSTNAMES[0],
    'challenge_ts': datetime.datetime.now(datetime.timezone.utc).isoformat()
}

UNSUCCESSFUL_RECAPTCHA_RESPONSE = {
    'success': False
}

EXPIRED_RECAPTCHA_RESPONSE = {
    'success': True,
    'hostname': SOME_EXAMPLE_ALLOWED_HOSTNAMES[0],
    'challenge_ts': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=SOME_EXAMPLE_EXPIRY_TIME+10)).isoformat()
}

UNVALID_HOSTNAME_RECAPTCHA_RESPONSE = {
    'success': True,
    'hostname': SOME_UNVALID_HOSTNAME,
    'challenge_ts': (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=SOME_EXAMPLE_EXPIRY_TIME+10)).isoformat()
}

UNVALID_RECAPTCHA_SECRET_RESPONSE = {
    'success': False,
}


def mocked_requests_post(*args, **kwargs):
    '''Mock for requests.post'''

    url = args[0]
    data = kwargs['data']
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            if url == SOME_UNVALID_JSON_RECAPTCHA_API_URL:
                raise ValueError()
            return self.json_data
    
    if data['secret'] != SOME_VALID_RECAPTCHA_SECRET:
        return MockResponse(UNVALID_RECAPTCHA_SECRET_RESPONSE, 400)

    if url == SOME_VALID_RECAPTCHA_API_URL:
        if data['response'] == SOME_VALID_RECAPTCHA_TOKEN:
            return MockResponse(SUCCESSFUL_RECAPTCHA_RESPONSE, 200)
        if data['response'] == SOME_UNVALID_RECAPTCHA_TOKEN:
            return MockResponse(UNSUCCESSFUL_RECAPTCHA_RESPONSE, 200)
        if data['response'] == SOME_EXPIRED_RECAPTCHA_TOKEN:
            return MockResponse(EXPIRED_RECAPTCHA_RESPONSE, 200)
        if data['response'] == SOME_UNVALID_HOSTNAME_RECAPTCHA_TOKEN:
            return MockResponse(UNVALID_HOSTNAME_RECAPTCHA_RESPONSE, 200)
    elif url == SOME_TIMING_OUT_RECAPTCHA_API_URL:
        raise Timeout('Timeout error details')
    
    return MockResponse(None, 404)
