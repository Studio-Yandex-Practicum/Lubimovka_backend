from django.db import models

from apps.core.models import BaseModel


class Event(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название события",
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
