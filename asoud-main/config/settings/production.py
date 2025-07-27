# -----------------------------------------------------------------------------
# This file contains settings specific to the production environment,
# such as disabling debug mode, configuring the production database,
# and other production-related settings.
# -----------------------------------------------------------------------------

import os
import re
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

# Security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# CSRF security - Ruthless protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = False  # Disable for API compatibility
CSRF_COOKIE_AGE = 3600  # 1 hour
CSRF_TRUSTED_ORIGINS = ['https://asoud.ir', 'https://*.asoud.ir']
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Data Upload Security
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Ruthless Database Security
DATABASES['default']['OPTIONS'].update({
    'connect_timeout': 5,
    'options': '-c default_transaction_isolation=serializable -c statement_timeout=30000'
})

# Logging Security - No sensitive data exposure
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'secure': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'logs', 'security.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'secure',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'asoud': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Cache Security
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': redis_url,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'asoud',
        'VERSION': 1,
    }
}

# Email Security
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 10

# Additional Security Settings
SILENCED_SYSTEM_CHECKS = []
DISALLOWED_USER_AGENTS = [
    re.compile(r'Googlebot'),
    re.compile(r'bingbot'), 
    re.compile(r'slurp'),
    re.compile(r'DuckDuckBot'),
    re.compile(r'BaiduSpider'),
    re.compile(r'YandexBot'),
    re.compile(r'facebookexternalhit'),
    re.compile(r'twitterbot'),
    re.compile(r'WhatsApp')
]

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
