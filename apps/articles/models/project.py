from django.db import models

from apps.content_pages.models import ContentPage
from apps.core.models import BaseModel


class ProjectContentPage(ContentPage):
    """
    Custom proxy ContentPage model to limit actions and avaliable content
    blocks for Project object. It also uses to register in admin page.
    """

    class Meta:
        proxy = True
        verbose_name = "Блок сложной верстки проекта"
        verbose_name_plural = "Блоки сложной верстки проектов"
        ordering = ["-modified"]


class Project(BaseModel):
    name = models.CharField(
        max_length=20,
        verbose_name="Название проекта",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание проекта",
    )
    image = models.ImageField(
        upload_to="images/projects/",
        verbose_name="Заглавная картинка проекта",
    )
    content_page = models.OneToOneField(
        ProjectContentPage,
        on_delete=models.PROTECT,
        verbose_name="Блок элементов сложной верстки проекта",
    )

    def __str__(self):
        return f"Проект {self.name}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
