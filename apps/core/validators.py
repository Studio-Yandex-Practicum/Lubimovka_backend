import re

from django.core.exceptions import ValidationError


def name_validator(lastname):
    """Проверяет написание ФИО.

    ФИО может быть написано с использованием букв русского и английского
    алфавита, тире и пробела (последние два - необязательны).
    """
    pattern = r"(^[a-zA-Zа-яА-ЯёЁ]+[a-zA-Zа-яА-ЯёЁ\s-]*[a-zA-Zа-яА-ЯёЁ]+$)|(^[a-zA-Zа-яА-яёЁ]+$)"
    match = re.match(pattern, lastname)
    if match is None:
        raise ValidationError(
            "ФИО может содержать только буквы русского или английского алфавита, "
            "между ними может присутствовать тире и пробел"
        )
