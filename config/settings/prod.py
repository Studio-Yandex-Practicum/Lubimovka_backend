import os

from .base import *  # noqa

# GENERAL
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS += [
    "2022.lubimovka.ru",
    "lubimovka.art",
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURE_PROXY_SSL_HEADER
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://anymail.readthedocs.io/en/stable/esps/mailjet/#settings
ANYMAIL = {
    "MAILJET_API_KEY": env("MAILJET_API_KEY", default=None),
    "MAILJET_SECRET_KEY": env("MAILJET_SECRET_KEY", default=None),
}
