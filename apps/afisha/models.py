from django.db import models

from apps.core.models import BaseModel


class Event(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название события",
    )
