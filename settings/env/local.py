from settings.base import *

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

DEFAULT_FROM_EMAIL="noreply@blog.local"

#SQL LOGGING:every query is printed to the terminal
LOGGING={
    "version":1,
    "disable_existing_loggers":False,
    "handlers":{
        "console":{
            "class":"logging.StreamHandler"
        },
    },
    "loggers":{
        "django.db.backends":{
            "handlers":("console",),
            "level":"DEBUG"
    },
    },

}