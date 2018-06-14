# -*- coding: utf-8 -*-
"""
Base settings file
"""
# System imports
import json
import os

# Third-party imports
# Local imports


RECAPTCHA_API_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_SECRET = os.environ['RECAPTCHA_SECRET']
RECAPTCHA_ALLOWED_HOSTNAMES = json.loads(os.environ['RECAPTCHA_ALLOWED_HOSTNAMES_JSON'])
RECAPTCHA_EXPIRES_IN = int(os.environ['RECAPTCHA_EXPIRES_IN'])
RECAPTCHA_MAX_RETRY_TIME = int(os.environ['RECAPTCHA_MAX_RETRY_TIME'])
