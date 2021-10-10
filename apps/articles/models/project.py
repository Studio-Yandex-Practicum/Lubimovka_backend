from django.db import models
from django.db.models.deletion import CASCADE

from apps.content_pages.models import Content
from apps.core.models import BaseModel


class ProjectContent(Content):
    class Meta:
        proxy = True
        verbose_name = "Блок сложной верстки для проекта"
        verbose_name_plural = "Блоки сложной верстки проектов"


class OrderedProjectContent(BaseModel):
    content_item = models.ForeignKey(
        ProjectContent,
        on_delete=CASCADE,
        related_name="project_contents",
        verbose_name="Модуль страницы",
    )
    project_item = models.ForeignKey(
        "Project",
        on_delete=CASCADE,
        related_name="project_contents",
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    def __str__(self):
        return (
            f"{self.project_item.name} - {self.content_item.content_type.name}"
        )

    class Meta:
        ordering = ["order"]
        verbose_name = "Модуль проекта"
        verbose_name_plural = "Модули проектов"


class Project(BaseModel):
    name = models.CharField(
        max_length=20,
        verbose_name="Название проекта",
    )
    description = models.TextField(
        max_length=500, verbose_name="Описание проекта"
    )
    image = models.ImageField(
        upload_to="images/projects/",
        verbose_name="Заглавная картинка проекта",
    )
    contents = models.ManyToManyField(
        ProjectContent,
        through=OrderedProjectContent,
        verbose_name="Контент сложной верстки",
    )

    def __str__(self):
        return f"Проект {self.name}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
