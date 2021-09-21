from django.db import models

from apps.core.models import BaseModel


class NewsItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название новости",
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class ArticleBlog(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Project(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название проекта",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
