from decouple import config
from datetime import timedelta

SECRET_KEY = config("BLOG_SECRET_KEY", cast=str)
ENV_ID = config("BLOG_ENV_ID", cast=str)
REDIS_URL=config("BLOG_REDIS_URL",cast=str)


#DJANGO REST FRAMEWORK

REST_FRAMEWORK={
    "DEFAULT_PERMISSION_CLASSES":(
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES":(
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ),
}


#Simple JWT
ACCESS_TOKEN_MINUTES=15
REFRESH_TOKEN_LIFESTYLE_DAYS=1

SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME":timedelta(minutes=ACCESS_TOKEN_MINUTES),
    "REFRESH_TOKEN_LIFETIME":timedelta(days=REFRESH_TOKEN_LIFESTYLE_DAYS),
    "SIGNING_KEY":SECRET_KEY,
    "AUTH_HEADER_TYPES":("Bearer",),
    "USER_ID_FIELD":"id",
    "USER_ID_CLAIM":"user_id",
    "CHECK_USER_IS_ACTIVE":True,
}

#Cache

CACHES={
    "default":{
        "BACKEND":"django.core.cache.backends.redis.RedisCache",
        "LOCATION":REDIS_URL
    }
}

#Celery
CELERY_BROKER_URL=REDIS_URL
CELERY_ACCEPT_CONTENT=("json",)
CELERY_TASK_SERIALIZER="json"
     
