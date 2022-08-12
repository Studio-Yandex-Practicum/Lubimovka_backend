import re

from django.core.exceptions import ValidationError


def email_validator(email):
    """Задаем настройки паттерна для проверки почтового адреса.

    Допускается использование латинских букв, цифр и символов @/./+/-/_.
    Ограничение длины в 150 символов.
    """
    pattern = r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
    max_length = 150
    match = re.match(pattern, email, re.IGNORECASE)
    if match is None or len(email) > max_length:
        raise ValidationError(
            "Используйте корректный адрес электронной почты. Адрес должен быть не длиннее 150 символов. "
            "Допускается использование латинских букв, цифр и символов @/./+/-/_"
        )


class MaximumLengthValidator:
    def __init__(self, max_length=16):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError((f"Длина пароля не должна превышать {self.max_length} символов."))

    def get_help_text(self):
        return f"Длина пароля не должна превышать {self.max_length} символов."
