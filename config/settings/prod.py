import os

from .base import *  # noqa

ALLOWED_HOSTS += [
    "2022.lubimovka.ru",
    "lubimovka.art",
    "backend"
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
