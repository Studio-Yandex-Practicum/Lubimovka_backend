from django.db import models

from apps.content_pages.models import Content, ContentPage


class Project(ContentPage):
    image = models.ImageField(
        upload_to="images/projects/",
        verbose_name="Заглавная картинка проекта",
    )

    def __str__(self):
        return f"Проект {self.title}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class ProjectContent(Content):
    """Custom ContentPage model for Project models."""

    content_page = models.ForeignKey(
        Project,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Блок элементов сложной верстки",
    )

    class Meta:
        verbose_name = "Блок сложной верстки проекта"
        verbose_name_plural = "Блоки сложной верстки проектов"
        ordering = ["order"]
