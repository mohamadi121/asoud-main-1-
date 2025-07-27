# -----------------------------------------------------------------------------
# This file contains settings specific to the development environment,
# such as enabling debug mode, using a local database, and
# configuring other development-related settings.
# -----------------------------------------------------------------------------

from .base import *
import uuid

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '.localhost', 
    '127.0.0.1',
    'aasoud.ir',
    'asoud.ir',
    '.aasoud.ir',
    '*',  # For Docker development
]

# Override database for development if using Docker
import os
if os.environ.get('DATABASE_HOST') == 'db':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME', 'asoud_dev'),
            'USER': os.environ.get('DATABASE_USER', 'postgres'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'postgres123'),
            'HOST': os.environ.get('DATABASE_HOST', 'db'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
            'OPTIONS': {},  # No SSL for local development
        }
    }

ZARINPAL_URL = "sandbox"

