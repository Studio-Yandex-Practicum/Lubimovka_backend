from django.db import models

from apps.core.models import BaseModel


class History(BaseModel):
    class Meta:
        verbose_name = "История"


class HistoryQuestion(BaseModel):
    question = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Текст вопроса",
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
