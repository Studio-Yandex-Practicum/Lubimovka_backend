from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel, Person


class MainSettings(BaseModel):

    festival = models.BooleanField(
        verbose_name="Состояние Фестиваль или нет",
    )

    persons_how_get_questions = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Люди, получающие вопросы на почту",
    )

    def clean(self):
        if MainSettings.objects.count() == 1:
            raise ValidationError("Объект настроек уже создан")
