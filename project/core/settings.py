import os
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# python manage.py check --deploy
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

# доступ тільки з дозволених хостів
# 'Host' Header
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
# дозволені Origin (заголовок) для unsafe-запитів (POST, PUT, DELETE, PATCH)
# але CSRF token все одно обов'язковий (whitelist),
# тобто з яких frontend-origin дозволено unsafe requests
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1").split(
    ","
)

# JavaScript не має доступу до sessionid cookie
SESSION_COOKIE_HTTPONLY = True
# сесія завершується і видаляється при закритті браузера
# але працює не для всіх браузерів
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# передача sessionid
# та csrftoken cookies тільки через HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Lax - cookies передаються у звичайних переходах між сайтами
# None — cookies передаються і в cross-site запитах (тільки через HTTPS)
# same-site = однаковий registrable domain (google.com)
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# автоматично перенаправляє HTTP -> HTTPS при DEBUG=False
SECURE_SSL_REDIRECT = not DEBUG
# якщо додаток працює через Nginx, то Django буде довіряти
# заголовку HTTP_X_FORWARDED_PROTO, який встановлює Nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# цей ендпоінт може бути використаний через HTTP
# переадресація на HTTPS не буде застосована автоматично
SECURE_REDIRECT_EXEMPT = [
    r"check_pod/",
]

STATIC_ROOT = BASE_DIR / "static"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "books",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "core.middlewares.RequestIdMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

POSTGRES_URL = os.environ.get("POSTGRES_URL")

if POSTGRES_URL is None:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB_NAME", None),
            "USER": os.environ.get("POSTGRES_USER", None),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", None),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        },
    }

else:
    parsed_postgres_url = urlparse(POSTGRES_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed_postgres_url.path.replace("/", ""),
            "USER": parsed_postgres_url.username,
            "PASSWORD": parsed_postgres_url.password,
            "HOST": parsed_postgres_url.hostname,
            "PORT": 5432,
            "OPTIONS": dict(parse_qsl(parsed_postgres_url.query)),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication"
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
        "user": "1000/day",
    },
    "NUM_PROXIES": 2,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[ %(asctime)s - %(request_id)s - %(levelname)s ] %(message)s [ %(name)s - %(module)s.%(funcName)s() ]",
            "style": "%",
        },
        "json": {
            "()": "config.logging.formatters.FileJSONFormatter",
        },
    },
    "filters": {
        "request_uid": {
            "()": "config.logging.filters.RequestFilter",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["request_uid"],
        },
        "json_file": {
            "class": "config.logging.handlers.JSONFileHandler",
            "filename": "logs/app.json",
            "filters": ["request_uid"],
            "formatter": "json",
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "filters": ["request_uid"],
            "formatter": "simple",
            "level": "INFO",
            "propagate": True,
        },
        "books": {
            "handlers": ["json_file"],
            "filters": ["request_uid"],
            "level": "INFO",
        },
    },
}
