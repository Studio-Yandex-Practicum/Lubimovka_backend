from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.content_pages.models import AbstractContent, AbstractContentPage


class Project(AbstractContentPage):
    image = models.ImageField(
        upload_to="images/projects/",
        verbose_name="Заглавная картинка проекта",
    )

    def __str__(self):
        return f"Проект {self.title}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class ProjectContent(AbstractContent):
    """Custom ContentPage model for Project models.

    1. It's required to set 'content_page' foreign key to concrete or proxy
    model.
    2. Limit a set of models that could be used with GenericForeginKey. It's
    not a DRY, but other methods to limit choices more complicated and
    dedicated from model.
    """

    content_page = models.ForeignKey(
        Project,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Блок элементов сложной верстки",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "app_label": "content_pages",
            "model__in": [
                "video",
                "videosblock",
                "imagesblock",
                "performancesblock",
                "playsblock",
                "personsblock",
                "link",
            ],
        },
    )

    class Meta:
        verbose_name = "Блок сложной верстки проекта"
        verbose_name_plural = "Блоки сложной верстки проектов"
        ordering = ["order"]
