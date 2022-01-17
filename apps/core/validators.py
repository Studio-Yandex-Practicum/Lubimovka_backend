import re

from django.core.exceptions import ValidationError


def name_validator(lastname):
    """Проверяет написание ФИО.

    ФИО может быть написано с использованием букв русского алфавита,
    тире и пробела (последние два - необязательны.
    """
    example = r"^[а-яА-ЯёЁ]+[а-яА-ЯёЁ\s-]*[а-яА-ЯёЁ]+$"
    match = re.search(example, lastname, re.I)
    if not bool(match):
        raise ValidationError("ФИО может содержать буквы русского алфавита, тире и пробел")
