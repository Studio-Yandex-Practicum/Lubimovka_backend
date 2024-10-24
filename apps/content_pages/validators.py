from django.core.exceptions import ValidationError


def iframe_validator(code: str):
    code = code.strip()
    if not (code.startswith("<iframe ") and code.endswith("</iframe>")):
        raise ValidationError("Встраиваемое содержимое должно быть заключено в теги <iframe></iframe>")
