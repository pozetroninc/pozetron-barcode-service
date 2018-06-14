# -*- coding: utf-8 -*-
"""
Base settings file
"""
# System imports
import json
import os

# Third-party imports
# Local imports


RECAPTCHA_SECRET = os.environ['RECAPTCHA_SECRET']
RECAPTCHA_ALLOWED_HOSTNAMES = json.loads(os.environ['RECAPTCHA_ALLOWED_HOSTNAMES_JSON'])
