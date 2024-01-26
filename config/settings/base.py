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
DEBUG = env.bool("DJANGO_DEBUG", default=True)

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[]) + ["127.0.0.1", "localhost", "backend"]

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "localhost"]

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
    "easy_thumbnails",
    "apps.filer.apps.FilerCustomConfig",
    "private_storage",
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
    "apps.feedback",
    "apps.postfix",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#specifying-authentication-backends
AUTHENTICATION_BACKENDS = [
    "apps.users.backends.admin_user.AdminUserModelBackend",
]

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
        "OPTIONS": {
            "min_length": 6,
        }
    },
    {
        "NAME": "apps.core.validators.MaximumLengthValidator",
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

# DJANGO-CKEDITOR
# ------------------------------------------------------------------------------
# https://django-ckeditor.readthedocs.io/en/latest/#
CKEDITOR_TOOLBAR_BASE = (
    ("Undo", "Redo"),
    ("Typograf",),
    ("Bold", "Italic", "Link", "Unlink", "RemoveFormat"),
    ("Styles", "Font", "FontSize"),
    ("Blockquote",),
    ("NumberedList", "BulletedList"),
)
CKEDITOR_BASE = {
    "height": 300,
    "autoGrow_bottomSpace": 30,
    "autoGrow_minHeight": 300,
    "autoGrow_maxHeight": 500,
    "extraPlugins": ("autogrow", "typograf"),
    "basicEntities": False,
    "toolbar": "base",
    "toolbar_base": CKEDITOR_TOOLBAR_BASE,
}
CKEDITOR_CONFIGS = {
    "default": CKEDITOR_BASE,
    "lubimovka_styles": CKEDITOR_BASE | {
        "contentsCss": "/static/core/ckeditor/lubimovka_styles.css",
        "stylesSet": (
            {"name": "Заголовок", "element": "h3"},
            {"name": "Подзаголовок", "element": "h4"},
        ),
    },
    "press_release_styles": CKEDITOR_BASE | {
        "contentsCss": "/static/core/ckeditor/press-release-styles.css",
        "stylesSet": (
            {"name": "Подзаголовок", "element": "h2"},
            {"name": "Обычный", "element": "p"}
        ),
    }
}

# Google Sheets Export integration keys
# ------------------------------------------------------------------------------
GOOGLE_PRIVATE_KEY = env("GOOGLE_PRIVATE_KEY", default="private_key").replace("\\n", "\n")
GOOGLE_PRIVATE_KEY_ID = env("GOOGLE_PRIVATE_KEY_ID", default="private_key_id")


# Export to Yandex.Disk integration key
# ------------------------------------------------------------------------------
YNDX_DISK_TOKEN = env("YNDX_DISK_TOKEN", default="yndx_token")

# Logging settings
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/topics/logging/#configuring-logging
LOGGING = LOGGING_SETTINGS

LOGIN_URL = "/admin/login/"

# https://anymail.readthedocs.io/en/stable/esps/mailjet/#settings
ANYMAIL = {
    "MAILJET_API_KEY": env("MAILJET_API_KEY", default=None),
    "MAILJET_SECRET_KEY": env("MAILJET_SECRET_KEY", default=None),
}

# Templates for mailjet
# ------------------------------------------------------------------------------
# https://anymail.dev/en/stable/esps/mailjet/
MAILJET_TEMPLATE_ID_QUESTION = env("MAILJET_TEMPLATE_ID_QUESTION", default="0000000")
MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION = env("MAILJET_TEMPLATE_ID_PARTICIPATION_APPLICATION", default="0000000")
MAILJET_TEMPLATE_ID_REGISTRATION_USER = env("MAILJET_TEMPLATE_ID_REGISTRATION_USER", default="0000000")
MAILJET_TEMPLATE_ID_RESET_PASSWORD_USER = env("MAILJET_TEMPLATE_ID_RESET_PASSWORD_USER", default="0000000")

ADMIN_SITE_APPS_ORDER = (
    "Библиотека",
    "Новости, Проекты, Блог",
    "Афиша",
    "Информация",
    "Общие ресурсы приложений",
    "Настройки приложения",
    "Обратная связь",
    "Пользователи",
)

ADMIN_SITE_MODELS_ORDER = {
    "Библиотека": [
        "Авторы",
        "Пьесы",
        "Программы",
    ],
    "Афиша": [
        "Афиша",
        "Спектакли",
        "Специальные события",
        "Медиа отзывы на спектакль",
        "Отзывы зрителей на спектакль",
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
        "Отборщики фестиваля",
    ],
    "Общие ресурсы приложений": [
        "Люди",
        "Должности/позиции",
    ],
    "Настройки приложения": [
        "Банеры на главной странице",
        "Настройки афиши",
        "Настройки главной страницы",
        "Настройки обратной связи",
        "Настройки первой страницы",
        "Настройки подачи пьес",
        "Общие настройки",
    ],
    "Пользователи": [
        "Пользователи",
        "Группы",
    ],
    "Обратная связь": [
        "Вопросы или предложения",
        "Заявки на участие",
    ]
}

SPECTACULAR_SETTINGS = {
    "ENUM_NAME_OVERRIDES": {
        "event_type": "apps.afisha.models.events.Event.EventType",
        "partner_type": "apps.info.models.people.Partner.PartnerType",
    },
    'COMPONENT_SPLIT_REQUEST': True,
}

CSRF_FAILURE_VIEW = 'apps.core.views.csrf_failure'

# https://anymail.readthedocs.io/en/stable/installation/?highlight=SERVER_EMAIL#configuring-django-s-email-backend
SERVER_EMAIL = env("SERVER_EMAIL", default=None)

# https://docs.djangoproject.com/en/3.0/ref/django-admin/#django-admin-createsuperuser
DJANGO_SUPERUSER_USERNAME = env("DJANGO_SUPERUSER_USERNAME", default="admin")
DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default="admin@admin.com")
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default="admin")

# Use PostgreSQL
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

# SECURE_PROXY_SSL_HEADER
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# DJANGO-FILER
FILER_CANONICAL_URL = 'sharing/'
FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True
FILER_STORAGES = {
    'public': {
        'main': {
            'UPLOAD_TO': 'apps.filer.utils.folder_slug',
        }
    }
}

# Translations
LOCALE_PATHS = [Path(STATIC_ROOT) / "core" / "locale", ]


# Private storage settings
PRIVATE_STORAGE_ROOT = ROOT_DIR / "protected_media"
PRIVATE_STORAGE_AUTH_FUNCTION = "private_storage.permissions.allow_staff"
PRIVATE_STORAGE_SERVER = "nginx"
PRIVATE_STORAGE_INTERNAL_URL = "/private-redirect/"

# APP SETTINGS
AFISHA_REGISTRATION_OPENS_HOURS_BEFORE = 12
POSTFIX_MAIL_DOMAIN = os.environ.get("POSTFIX_MAIL_DOMAIN")
POSTFIX_DB_PASSWORD = os.environ.get("POSTFIX_DB_PASSWORD")
