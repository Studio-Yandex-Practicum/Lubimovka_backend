from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class BlogItem(BaseModel):
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


class BlockTitle(BaseModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Блок заголовок",
    )

    def __str__(self) -> str:
        return self.title


class BlockText(BaseModel):
    text = models.TextField(
        max_length=500,
        verbose_name="Блок с текстом",
    )

    def __str__(self) -> str:
        return self.text


class Content(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )
    project = models.ForeignKey(
        Project,
        related_name="modules",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "blocktitle",
                "blocktext",
            )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name
