from django.db import models

from apps.core.models import BaseModel


class AbstractItemBase(BaseModel):
    """Base abstract model for 1-item 'content' block."""

    title = models.CharField(
        max_length=250,
        verbose_name="Заголовок",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Image(AbstractItemBase):
    """Image with title for 'content' blocks."""

    image = models.ImageField(
        upload_to="content_images",
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Link(AbstractItemBase):
    """Link with title for 'content' blocks."""

    description = models.TextField(
        max_length=250,
        verbose_name="Описание ссылки",
    )
    url = models.URLField()

    class Meta:
        verbose_name = "Ссылка с описанием"
        verbose_name_plural = "Ссылки с описанием"


class Video(AbstractItemBase):
    """Video with title for 'content' blocks."""

    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Описание видео",
    )
    url = models.URLField()

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
