from django.db import models
from django.utils.translation import gettext_lazy as _


class AgeLimit(models.IntegerChoices):
    NO_LIMIT = (0, "0+")
    CHILD_LIMIT = (6, "6+")
    TEENAGE_LIMIT = (12, "12+")
    TEENAGE_LIMIT_USA = (13, "13+")
    YOUNG_LIMIT = (16, "16+")
    YOUNG_LIMIT_USA = (17, "17+")
    ADULTS_ONLY = (18, "18+")


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
        "min_level_to_change": 1,
        "min_level_to_delete": 1,
        "possible_changes": (
            "REVIEW",
            "READY_FOR_PUBLICATION",
        ),
    },
    "REVIEW": {
        "button_name": "Отправить на проверку",
        "min_access_level": 1,
        "min_level_to_change": 2,
        "min_level_to_delete": 2,
        "possible_changes": (
            "IN_PROCESS",
            "READY_FOR_PUBLICATION",
        ),
    },
    "READY_FOR_PUBLICATION": {
        "button_name": "Подготовить к публикации",
        "min_access_level": 2,
        "min_level_to_change": 2,
        "min_level_to_delete": 2,
        "possible_changes": (
            "IN_PROCESS",
            "PUBLISHED",
        ),
    },
    "PUBLISHED": {
        "button_name": "ОПУБЛИКОВАТЬ",
        "min_access_level": 2,
        "min_level_to_change": 3,
        "min_level_to_delete": 3,
        "possible_changes": (
            "IN_PROCESS",
            "REMOVED_FROM_PUBLICATION",
        ),
    },
    "REMOVED_FROM_PUBLICATION": {
        "button_name": "Снять с публикации",
        "min_access_level": 2,
        "min_level_to_change": 2,
        "min_level_to_delete": 2,
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

YOUTUBE_VIDEO_LINKS = [
    "https://www.youtube.com/watch?v=NJp9ZdRcJJE",
    "https://www.youtube.com/watch?v=EXt79hq_xbE",
    "https://www.youtube.com/watch?v=9UiQaRZd8j0",
    "https://www.youtube.com/watch?v=8bkupH49uCk",
    "https://www.youtube.com/watch?v=WJwmUrCeVfM",
    "https://www.youtube.com/watch?v=OR9hmtwjz0E",
    "https://www.youtube.com/watch?v=p7GkTm2ulFo",
    "https://www.youtube.com/watch?v=X-J6s35FKH8",
    "https://www.youtube.com/watch?v=c3rd14kOJrI",
    "https://www.youtube.com/watch?v=cUjZsth0zP8",
    "https://www.youtube.com/watch?v=NkvP2jR8xlw",
    "https://www.youtube.com/watch?v=BnORroiGX3U",
    "https://www.youtube.com/watch?v=FCjOBPY1kTw",
    "https://www.youtube.com/watch?v=JiZk95ewxAA",
    "https://www.youtube.com/watch?v=znz2cdqivBk",
    "https://www.youtube.com/watch?v=ECf2dnwmRuQ",
    "https://www.youtube.com/watch?v=dIGk5UDQkNw",
    "https://www.youtube.com/watch?v=g7-XK06qxgY",
    "https://www.youtube.com/watch?v=1tNJRDXGgU8",
    "https://www.youtube.com/watch?v=ksSmoTW2_Yc",
    "https://www.youtube.com/watch?v=sXmXP5Sl30Y",
    "https://www.youtube.com/watch?v=XMIwlMsEOgk",
    "https://www.youtube.com/watch?v=IpFVmlej_Ok",
    "https://www.youtube.com/watch?v=rfhJSFuUZXw",
    "https://www.youtube.com/watch?v=Ae1hUGycs40",
    "https://www.youtube.com/watch?v=S_M8I1aHVpM",
    "https://www.youtube.com/watch?v=0EeI_UjEozE",
    "https://www.youtube.com/watch?v=Hlrqa8-_sJs",
    "https://www.youtube.com/watch?v=-UYCpXEdL8I",
    "https://www.youtube.com/watch?v=OvDe1Ebqr-8",
]

AUTHORS_COUNT = [1, 1, 1, 1, 2, 2, 3]
