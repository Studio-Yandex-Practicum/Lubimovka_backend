from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Content(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "content_pages"},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()

    class Meta:
        verbose_name = "Блок сложной верстки"
        verbose_name_plural = "Блоки сложной верстки"

    def __str__(self):
        return f"Блок сложной верстки — {self.item}"
