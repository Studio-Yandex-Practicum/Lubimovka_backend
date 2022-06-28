import re

from django.core.exceptions import ValidationError


def name_validator(name):
    """Проверяет написание ФИО.

    ФИО может быть написано с использованием букв русского и английского
    алфавита, тире и пробела (последние два - необязательны).
    """
    pattern = r"^[a-zA-Zа-яА-ЯёЁ]+[a-zA-Zа-яА-ЯёЁ\s-]*[a-zA-Zа-яА-ЯёЁ]+$"
    match = re.match(pattern, name)
    if match is None:
        raise ValidationError(
            "Это поле может содержать только буквы русского или английского алфавита, "
            "между ними может присутствовать тире и пробел"
        )


def nickname_validator(nickname):
    """Проверяет написание имени/псевдонима.

    Пснвдоним может быть написано с использованием букв русского и английского
    алфавита, цифр, тире и подчеркивания, между ними может присутствовать тире и пробел.
    """
    pattern = r"^[0-9a-zA-Zа-яА-ЯёЁ_-]+[0-9a-zA-Zа-яА-ЯёЁ\s_-]*[0-9a-zA-Zа-яА-ЯёЁ_-]+$"
    match = re.match(pattern, nickname)
    if match is None:
        raise ValidationError(
            "Это поле может содержать только буквы русского или английского алфавита, "
            "цифры, тире и подчеркивания, между ними может присутствовать пробел"
        )


class MaximumLengthValidator:
    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError((f"Длина пароля не должна превышать {self.max_length} символов."))

    def get_help_text(self):
        return f"Длина пароль не должна превышать {self.max_length} символов."
