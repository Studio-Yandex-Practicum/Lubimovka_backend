from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import strip_tags

from apps.core.models import BaseModel


class AbstractItemWithTitle(BaseModel):
    """Base abstract model for 1-item `content` block."""

    title = models.CharField(
        max_length=250,
        verbose_name="Заголовок",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Link(AbstractItemWithTitle):
    """Link with title for `content` blocks."""

    description = models.TextField(
        max_length=250,
        verbose_name="Описание ссылки",
    )
    url = models.URLField()

    class Meta:
        verbose_name = "Ссылка с описанием"
        verbose_name_plural = "Ссылки с описанием"


class Preamble(BaseModel):
    """Preamble item for `content` blocks."""

    preamble = models.TextField(
        max_length=500,
        verbose_name="Преамбула",
    )

    class Meta:
        verbose_name = "Преамбула"
        verbose_name_plural = "Преамбулы"

    def __str__(self):
        return self.preamble


class Quote(BaseModel):
    """Quote item for `content` blocks."""

    quote = models.TextField(
        max_length=500,
        verbose_name="Цитата",
    )

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return self.quote


class Text(BaseModel):
    """Text item for `content` blocks."""

    text = RichTextField()

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"

    def __str__(self):
        return strip_tags(self.text)


class Title(BaseModel):
    """Text item for `content` blocks."""

    title = models.CharField(
        max_length=250,
        verbose_name="Заголовок",
    )

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"

    def __str__(self):
        return self.title
