

from .base import *
import os
import dj_database_url
DEBUG = False


allowed_hosts_string = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = allowed_hosts_string.split(
    ',')+['210.94.252.178'] if allowed_hosts_string else []


DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_COOKIE_DOMAIN = ".textneckhub.p-e.kr"
SESSION_COOKIE_DOMAIN = ".textneckhub.p-e.kr"  # 세션 쿠키도 함께 설정


CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_TRUSTED_ORIGINS = [
    "https://www.textneckhub.p-e.kr",
    "https://textneckhub.p-e.kr",
    "https://api.textneckhub.p-e.kr",
]
CORS_ALLOWED_ORIGINS = [
    "https://www.textneckhub.p-e.kr",
]
CORS_ALLOW_CREDENTIALS = True


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


FORCE_SCRIPT_NAME = '/board'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = None