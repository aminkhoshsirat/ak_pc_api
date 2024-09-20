import os
from datetime import timedelta
from pathlib import Path

from .config import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*7ka_#@8d5k2&vv^6uud@w&7h^$9143+vdgnv_x)vvqk+jp7t='

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django_light',
    'admin_tools_stats',
    'django_nvd3',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'ckeditor',
    'djangobower',

    # Internal Apps
    'django_jalali',
    'storages',
    'channels',
    'ckeditor_uploader',
    'django_render_partial',
    'rest_framework',
    'rest_framework.authtoken',
    'boto3',
    'rest_framework_swagger',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_celery_beat',
    'azbankgateways',
    'django_ckeditor_5',
    'django_htmx',
    'rest_framework_tracking',

    # External Apps

    'apps.asemble.apps.AsembleConfig',
    'apps.user.apps.UserConfig',
    'apps.product.apps.ProductConfig',
    'apps.blog.apps.BlogConfig',
    'apps.bucket.apps.BucketConfig',
    'apps.panel.apps.PanelConfig',
    'apps.power_calculator.apps.PowerCalculatorConfig',
    'apps.benchmark.apps.BenchmarkConfig',
    'apps.notification.apps.NotificationConfig',
    'apps.chat.apps.ChatConfig',
    'apps.video.apps.VideoConfig',
]

AUTH_USER_MODEL = 'user.UserModel'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'akurtekPC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'akurtekPC.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# DATABASES = {
#     'default': postgres_config
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fa-iran'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

# Arvan Storage

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = arvan_cloud_config.get('access_key')

AWS_SECRET_ACCESS_KEY = arvan_cloud_config.get('secret_key')

AWS_S3_ENDPOINT_URL = arvan_cloud_config.get('simin_domain')

AWS_STORAGE_BUCKET_NAME = arvan_cloud_config.get('bucket_name')

AWS_SERVICE_NAME = 's3'

AWS_S3_FILE_OVERWRITE = False

AWS_QUERYSTRING_AUTH = False



# Liara Storages

# AWS_ACCESS_KEY_ID = 's7mtd3ecb1safiaq'
# AWS_SECRET_ACCESS_KEY = '50dfce50-11b3-45a6-a8ec-4029430c8ae5'
# AWS_STORAGE_BUCKET_NAME = 'akurtek'
# AWS_S3_ENDPOINT_URL = 'https://storage.c2.liara.space'
# AWS_S3_REGION_NAME = 'us-east-1'
#
# # Django-storages configuration
# STORAGES = {
#   "default": {
#       "BACKEND": "storages.backends.s3.S3Storage",
#   },
#   "staticfiles": {
#       "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#   },
# }


# Ckeditor Config

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    }
}

CKEDITOR_UPLOAD_PATH = "blog/uploads/"

# CELERY SETTINGS
CELERY_BACKEND = 'redis://localhost:6379/3'
CELERY_BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/5'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = False

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Rest Framework Settings

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AKURTEK Project API',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "custom_upload_file"