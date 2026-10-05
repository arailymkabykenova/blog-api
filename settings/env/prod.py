from settings.base import * #noqa
from settings.conf import * #noqa
DEBUG=False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("BLOG_POSTGRES_DB",cast=str),
        'USER':config("BLOG_POSTGRES_USER",casr=str),
        'PASSWORD':config("BLOG_POSTGRES_PASSWORD",cast=str),
        'HOST':config("BLOG_POSTGRES_HOST",cast=str),
        'PORT':config("BLOG_POSTGRES_PORT",cast=int)
        
    }
}