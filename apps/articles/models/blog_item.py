from django.db import models

from apps.core.models import BaseModel


class BlogItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
