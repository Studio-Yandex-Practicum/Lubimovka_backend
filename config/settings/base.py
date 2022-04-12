"""Base settings to build other settings files upon."""
import os
from pathlib import Path

import environ

from config.logging.logging_settings import LOGGING_SETTINGS

env = environ.Env()
# Root folder of the project
# ------------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "apps"

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# Application definition
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "adminsortable2",
    "phonenumber_field",
    "drf_multiple_model",
    "ckeditor",
    "anymail",
]
LOCAL_APPS = [
    "apps.users",
    "apps.core",
    "apps.main",
    "apps.afisha",
    "apps.library",
    "apps.articles",
    "apps.info",
    "apps.content_pages",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.admin_versioning",
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "ru-Ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = ROOT_DIR / "media"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# Default primary key field type
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/api/.*$"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# Use CKEditor (Configuration)
# ------------------------------------------------------------------------------
CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "elementspath",
        "removeDialogTabs": "dialog:advanced",
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Undo", "Redo"],
            ["Bold", "Italic", "Underline", "Strike"],
            ["Link", "Unlink"],
        ],
    }
}
GOOGLE_PRIVATE_KEY = env("GOOGLE_PRIVATE_KEY", default="private_key").replace("\\n", "\n")
GOOGLE_PRIVATE_KEY_ID = env("GOOGLE_PRIVATE_KEY_ID", default="private_key_id")
YNDX_DISK_TOKEN = env("YNDX_DISK_TOKEN", default="yndx_token")

# https://docs.djangoproject.com/en/4.0/topics/logging/#configuring-logging
LOGGING = LOGGING_SETTINGS

# Templates for mailjet
# https://anymail.dev/en/stable/esps/mailjet/
# ------------------------------------------------------------------------------
MAILJET_TEMPLATE_ID_QUESTION = env("MAILJET_TEMPLATE_ID_QUESTION", default="0000000")
MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION = env("MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION", default="0000000")

ADMIN_SITE_APPS_ORDER = (
    "Библиотека",
    "Новости, Проекты, Блог",
    "Афиша",
    "Информация",
    "Общие ресурсы приложений",
    "Настройки приложения",
    "Пользователи",
)

ADMIN_SITE_MODELS_ORDER = {
    "Библиотека": [
        "Авторы",
        "Пьесы",
        "Программы",
        "Спектакли",
        "Мастер-классы",
        "Читки",
    ],
    "Информация": [
        "Фестивали",
        "Пресс-релизы",
        "Волонтёры фестиваля",
        "Команда фестиваля",
        "Попечители фестиваля",
        "Арт-дирекция фестиваля",
        "Партнеры",
        "Площадки",
        "Вопросы или предложения",
    ],
    "Общие ресурсы приложений": [
        "Люди",
    ],
    "Пользователи": [
        "Пользователи",
    ],
}

SPECTACULAR_SETTINGS = {
    "ENUM_NAME_OVERRIDES": {
        "event_type": "apps.afisha.models.Event.EventType",
        "partner_type": "apps.info.models.people.Partner.PartnerType"
    }
}
