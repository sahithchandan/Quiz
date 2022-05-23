from settings.base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT = "local"

API_HOST = '0.0.0.0:8000'
API_BASE_URL = 'http://{}'.format(API_HOST)
ALLOWED_HOSTS += ['0.0.0.0']

# Silk for Profiling
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
