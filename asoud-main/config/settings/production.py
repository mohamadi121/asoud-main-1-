# -----------------------------------------------------------------------------
# This file contains settings specific to the production environment,
# such as disabling debug mode, configuring the production database,
# and other production-related settings.
# -----------------------------------------------------------------------------

import os
from .base import *
import json
from django.conf import settings


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS_FILE = os.path.join(settings.BASE_DIR, 'allowed_hosts.json')
def get_persisted_allowed_hosts():
    try:
        with open(ALLOWED_HOSTS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return settings.ALLOWED_HOSTS

# TODO: Update this to match your domain(s)
BASE_ALLOWED_HOSTS = [
    '37.32.11.190',
    'asoud.ir',
    'app.asoud.ir',
    'asoud.asoud.ir',
    'sinahashemi1.asoud.ir',
    '0019431351.asoud.ir'
]
ALLOWED_HOSTS = get_persisted_allowed_hosts() + BASE_ALLOWED_HOSTS
# Use a more secure secret key in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# TODO: Add below lines after domain is submitted
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
