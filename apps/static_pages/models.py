from django.db import models

from apps.core.models import BaseModel


class MarkdownModel(BaseModel):
    title = models.CharField(
        max_length=150,
        verbose_name="Название статичной страницы",
    )
    data = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = "Статическая страница"
        verbose_name_plural = "Статические страницы"
