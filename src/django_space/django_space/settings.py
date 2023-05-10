import os
from pathlib import Path

import pygments.formatters
from logrich.logger_ import errlog, log  # noqa

from src.auth.config import config as fastapi_config
from src.django_space.config import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config.DJANGO_SECRET_KEY

DEBUG = fastapi_config.DEBUG

# https://docs.djangoproject.com/en/4.2/ref/settings/#time-format
TIME_INPUT_FORMATS = [
    "%H:%M",  # '14:30'
]

USE_L10N = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.django_space.indicators.apps.IndicatorsConfig",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.django_space.django_space.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.django_space.django_space.wsgi.application"
ASGI_APPLICATION = "src.django_space.django_space.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.POSTGRES_DB,
        "USER": config.POSTGRES_USER.get_secret_value(),
        "PASSWORD": config.POSTGRES_PASSWORD.get_secret_value(),
        "HOST": config.POSTGRES_HOSTNAME,
        "PORT": config.POSTGRES_PORT,
    },
}

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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/django/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True  # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect

CORS_ALLOW_CREDENTIALS = True

APPEND_SLASH = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "X-My-Header",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.db.backends": {
            "level": "DEBUG",
        },
    },
}

SHELL_PLUS = "bpython"
# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# Specify sqlparse configuration options when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

# print SQL queries in shell_plus
SHELL_PLUS_PRINT_SQL = True

SHELL_PLUS_IMPORTS = ["from logrich.logger_ import errlog, log", "from rich import inspect", "import rich"]
