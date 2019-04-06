from .base import *

ALLOWED_HOSTS = ['www.gunduzhuseyn.com', 'gunduzhuseyn.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

if os.environ['HTTPS_ENABLED']:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
