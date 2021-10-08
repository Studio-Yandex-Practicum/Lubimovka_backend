from django.db import models

from apps.core.models import BaseModel, Person


class MainSettings(BaseModel):

    festival = models.BooleanField(
        verbose_name="Состояние Фестиваль или нет",
    )

    persons_how_get_questions = models.ManyToManyField(
        Person,
        verbose_name="Люди, получающие вопросы на почту",
    )

    class Meta:
        verbose_name = "Основные настройки"
        verbose_name_plural = "Основные настройки"

    def __str__(self):
        return "Основные настройки"
