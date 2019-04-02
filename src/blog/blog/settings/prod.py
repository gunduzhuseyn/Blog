from .base import *

ALLOWED_HOSTS = []

if os.environ['HTTPS_ENABLED']:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
