from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    IN_PROCESS = "IN_PROCESS", _("В работе")
    REVIEW = "REVIEW", _("На проверке")
    READY_FOR_PUBLICATION = "READY_FOR_PUBLICATION", _("Готово к публикации")
    PUBLISHED = "PUBLISHED", _("Опубликовано")
    REMOVED_FROM_PUBLICATION = "REMOVED_FROM_PUBLICATION", _("Снято с публикации")


STATUS_INFO = {
    "IN_PROCESS": {
        "button_name": "Вернуть в работу",
        "min_access_level": 1,
        "min_level_to_delete": 1,
        "possible_changes": (
            "REVIEW",
            "READY_FOR_PUBLICATION",
        ),
    },
    "REVIEW": {
        "button_name": "Отправить на проверку",
        "min_access_level": 1,
        "min_level_to_delete": 2,
        "possible_changes": (
            "IN_PROCESS",
            "READY_FOR_PUBLICATION",
        ),
    },
    "READY_FOR_PUBLICATION": {
        "button_name": "Подготовить к публикации",
        "min_access_level": 2,
        "min_level_to_delete": 3,
        "possible_changes": (
            "IN_PROCESS",
            "PUBLISHED",
        ),
    },
    "PUBLISHED": {
        "button_name": "ОПУБЛИКОВАТЬ",
        "min_access_level": 3,
        "min_level_to_delete": 3,
        "possible_changes": (
            "IN_PROCESS",
            "REMOVED_FROM_PUBLICATION",
        ),
    },
    "REMOVED_FROM_PUBLICATION": {
        "button_name": "Снять с публикации",
        "min_access_level": 3,
        "min_level_to_delete": 3,
        "possible_changes": (
            "IN_PROCESS",
            "PUBLISHED",
        ),
    },
}


ALPHABET = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "i",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
