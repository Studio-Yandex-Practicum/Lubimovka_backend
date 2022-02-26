from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    IN_PROCESS = "IN_PROCESS", _("В работе")
    REVIEW = "REVIEW", _("На проверке")
    READY_FOR_PUBLICATION = "READY_FOR_PUBLICATION", _("Готово к публикации")
    PUBLISHED = "PUBLISHED", _("Опубликовано")
    REMOVED_FROM_PUBLICATION = "REMOVED_FROM_PUBLICATION", _("Снято с публикации")


def get_status_info_for_app(app_name: str) -> dict:
    status_info = {
        "IN_PROCESS": {
            "button_name": "Вернуть в работу",
            "access_level": (
                f"{app_name}.access_level_1",
                f"{app_name}.access_level_2",
                f"{app_name}.access_level_3",
            ),
            "access_to_delete": (
                f"{app_name}.access_level_1",
                f"{app_name}.access_level_2",
                f"{app_name}.access_level_3",
            ),
            "possible_changes": (
                "REVIEW",
                "READY_FOR_PUBLICATION",
            ),
        },
        "REVIEW": {
            "button_name": "Отправить на проверку",
            "access_level": (
                f"{app_name}.access_level_2",
                f"{app_name}.access_level_3",
            ),
            "access_to_delete": (
                f"{app_name}.access_level_2",
                f"{app_name}.access_level_3",
            ),
            "possible_changes": (
                "IN_PROCESS",
                "READY_FOR_PUBLICATION",
            ),
        },
        "READY_FOR_PUBLICATION": {
            "button_name": "Подготовить к публикации",
            "access_level": (
                f"{app_name}.access_level_2",
                f"{app_name}.access_level_3",
            ),
            "access_to_delete": (f"{app_name}.access_level_3",),
            "possible_changes": (
                "IN_PROCESS",
                "PUBLISHED",
            ),
        },
        "PUBLISHED": {
            "button_name": "ОПУБЛИКОВАТЬ",
            "access_level": (f"{app_name}.access_level_3",),
            "access_to_delete": (f"{app_name}.access_level_3",),
            "possible_changes": (
                "IN_PROCESS",
                "REMOVED_FROM_PUBLICATION",
            ),
        },
        "REMOVED_FROM_PUBLICATION": {
            "button_name": "Снять с публикации",
            "access_level": (f"{app_name}.access_level_3",),
            "access_to_delete": (f"{app_name}.access_level_3",),
            "possible_changes": (
                "IN_PROCESS",
                "PUBLISHED",
            ),
        },
    }
    return status_info
