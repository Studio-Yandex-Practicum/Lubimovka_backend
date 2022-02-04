from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError("Год должен быть не ранее 1900го и не позднее текущего.")
