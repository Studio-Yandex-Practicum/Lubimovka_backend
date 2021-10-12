from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import BaseModel


class ContentPage(BaseModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок страницы",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание страницы",
    )

    class Meta:
        abstract = True
        verbose_name = "Шаблон объекта с сложной версткой"
        verbose_name_plural = "Шаблоны объектов с сложной версткой"
        ordering = ["-modified"]

    def __str__(self):
        return self.title


class Content(models.Model):
    content_page = models.ForeignKey(
        ContentPage,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Блок элементов сложной верстки",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "content_pages"},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ["order"]
        verbose_name = "Элемент сложной верстки"
        verbose_name_plural = "Элементы сложной верстки"

    def __str__(self):
        return f"Блок сложной верстки — {self.item}"
