from pathlib import Path

import environ

env = environ.Env()

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
LOGS_DIR = ROOT_DIR / "logs"
DEBUG_LOGS_DIR = LOGS_DIR / "debug"
ERROR_LOGS_DIR = LOGS_DIR / "errors"

DJANGO_LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="DEBUG")


LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "debug_to_file": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "config.logging.logger_handler.TimedRotatingFileHandlerWithZip",
            "filename": DEBUG_LOGS_DIR / "debug.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 3,
            "oldbackupCount": 10,
            "formatter": "verbose",
        },
        "errors_to_file": {
            "level": "ERROR",
            "class": "config.logging.logger_handler.TimedRotatingFileHandlerWithZip",
            "filename": ERROR_LOGS_DIR / "error.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 3,
            "oldbackupCount": 10,
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["debug_to_file", "errors_to_file", "console"],
            "level": DJANGO_LOG_LEVEL,
        },
    },
}
