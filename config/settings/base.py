import os  # os 모듈 임포트 확인

import logging
from pathlib import Path
from datetime import timedelta

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ["*"]

# settings.py


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        # asctime, module, message를 포함하도록 format string 수정
        # record.getMessage()는 메시지 인자를 포맷팅하여 반환
        message = super().format(record)  # 기본 포맷팅된 메시지 가져오기
        return f"{log_color}{message}{self.RESET}"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "colored": {
            "()": ColoredFormatter,
            # message를 {message}로 변경
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": "DEBUG",  # 콘솔에는 DEBUG 레벨부터 모두 출력
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join('/app/logs', 'debug.log'),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "DEBUG",  # 파일에는 DEBUG 레벨부터 모두 출력 (info 포함)
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join('/app/logs', 'error.log'),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "ERROR",  # 에러 파일에는 ERROR 레벨만 출력 (이건 그대로 유지)
        },
    },

    "loggers": {
        # 'prod' 로거: 네 애플리케이션 코드에서 사용하는 주 로거
        "prod": {
            "handlers": ["console", "file", "error_file"],  # 모든 핸들러 연결
            "level": "INFO",  # INFO 레벨부터 로그를 처리 (DEBUG는 너무 많을 수 있음)
            "propagate": False,  # 상위 로거로 전달 안 함
        },
        # 'django' 로거: Django 프레임워크 자체의 로그
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",  # Django 로그는 INFO 레벨부터 (기본 권장)
            "propagate": False,
        },
        # 'django.request' 로거: HTTP 요청/응답 관련 로그
        "django.request": {
            "handlers": ["console", "error_file"],  # console과 error_file에만
            "level": "INFO",  # 요청 로그도 INFO 레벨부터 (기존 ERROR에서 변경)
            "propagate": False,
        },
        # 'allauth' 로거: django-allauth 라이브러리 로그
        'allauth': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # allauth 로그는 INFO 레벨부터
            'propagate': False,
        },
        # 'django_prometheus' 로거: Prometheus 관련 로그
        'django_prometheus': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        # 루트 로거: 명시적으로 설정되지 않은 모든 로거의 상위
        "": {
            "handlers": ["console", "file"],
            "level": "WARNING",  # 루트 로거는 WARNING 레벨부터 (너무 많은 로그 방지)
            "propagate": False,
        },
    },
}

VANILA_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'django_prometheus',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'channels'
]

LOCAL_APPS = ['board']

INSTALLED_APPS = VANILA_APPS + THIRD_PARTY_APPS + LOCAL_APPS

VANILA_MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
THIRD_PARTY_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
                          'allauth.account.middleware.AccountMiddleware']
MIDDLEWARE = VANILA_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 5))),

    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 1))),


    'ROTATE_REFRESH_TOKENS': os.environ.get('JWT_ROTATE_REFRESH_TOKENS', 'True').lower() == 'true',

    'BLACKLIST_AFTER_ROTATION': os.environ.get('JWT_BLACKLIST_AFTER_ROTATION', 'True').lower() == 'true',
    'UPDATE_LAST_LOGIN': False,


    'ALGORITHM': os.environ.get('JWT_ALGORITHM', 'HS256'),

    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,


    'AUDIENCE': os.environ.get('JWT_AUDIENCE', None),
    'ISSUER': os.environ.get('JWT_ISSUER', None),
    'JWK_URL': None,
    'LEEWAY': 0,


    'AUTH_HEADER_TYPES': (os.environ.get('JWT_AUTH_HEADER_TYPE', 'Bearer'),),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',


    'USER_ID_CLAIM': os.environ.get('JWT_USER_ID_CLAIM', 'user_id'),

    'USER_ID_FIELD': os.environ.get('JWT_USER_ID_FIELD', 'id'),


    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',


    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    'TOKEN_TYPE_CLAIM': 'token_type',

    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',


    'JTI_CLAIM': os.environ.get('JWT_JTI_CLAIM', 'jti'),


    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_SLIDING_TOKEN_LIFETIME_MINUTES', 5))),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=int(os.environ.get('JWT_SLIDING_TOKEN_REFRESH_LIFETIME_DAYS', 1))),
}



ROOT_URLCONF = 'config.urls'



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/app/collected_static_board/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/uploaded_media_board/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
