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


class ContentUnitRichText(BaseModel):
    """HTML text item for `content` block.

    Text field with limited HTML tags support. In real life the content of the field is
    produced by CKEditor plugin. Acceptable tags are configured in CKEDITOR settings.
    """

    rich_text = RichTextField(
        config_name="lubimovka_styles",
        verbose_name="Форматированный текст",
    )

    class Meta:
        verbose_name = "Форматированный текст"
        verbose_name_plural = "Форматированные тексты"

    def __str__(self):
        text = strip_tags(self.rich_text)
        return text if len(text) <= 100 else text[:97] + "..."


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
