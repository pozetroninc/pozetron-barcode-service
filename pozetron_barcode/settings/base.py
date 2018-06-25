# -*- coding: utf-8 -*-
"""
Base settings file
"""
# System imports
import json
import os

# Third-party imports
# Local imports


DEBUG = bool(json.loads(os.environ['DEBUG'])) if hasattr(os.environ, 'DEBUG') else False

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 0)

RECAPTCHA_API_URL = "https://www.google.com/recaptcha/api/siteverify"
RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET', None)
RECAPTCHA_ALLOWED_HOSTNAMES = json.loads(os.environ.get('RECAPTCHA_ALLOWED_HOSTNAMES_JSON')) if hasattr(os.environ, 'RECAPTCHA_ALLOWED_HOSTNAMES_JSON') else []
RECAPTCHA_EXPIRES_IN = int(os.environ.get('RECAPTCHA_EXPIRES_IN')) if hasattr(os.environ, 'RECAPTCHA_EXPIRES_IN') else 60
RECAPTCHA_MAX_RETRY_TIME = int(os.environ.get('RECAPTCHA_MAX_RETRY_TIME')) if hasattr(os.environ, 'RECAPTCHA_MAX_RETRY_TIME') else 60
RECAPTCHA_SHOULD_LOG_RETRIES = bool(json.loads(os.environ.get('RECAPTCHA_SHOULD_LOG_RETRIES'))) if hasattr(os.environ, 'RECAPTCHA_SHOULD_LOG_RETRIES') else False
