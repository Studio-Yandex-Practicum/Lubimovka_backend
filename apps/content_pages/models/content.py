from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import BaseModel


class ContentPage(BaseModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок блока элементов сложной верстки",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание что будет в блоке сложной верстки",
    )

    class Meta:
        verbose_name = "Блок элементов сложной верстки"
        verbose_name_plural = "Блоки элементов сложной верстки"
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
        ordering = ["order"]
        verbose_name = "Элемент сложной верстки"
        verbose_name_plural = "Элементы сложной верстки"

    def __str__(self):
        return f"Блок сложной верстки — {self.item}"
