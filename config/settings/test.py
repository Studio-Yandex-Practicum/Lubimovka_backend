"""With these settings, tests run faster."""
from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "p6kew3&vhfm^stv7v8t6(v(^eare9+820#yb^zv8=j!2z6k!_p"

ALLOWED_HOSTS += ["test.dev.lubimovka.ru"]

DEBUG = False

# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"
