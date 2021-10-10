from django.db import models
from django.db.models.deletion import CASCADE

from apps.content_pages.models import ProjectContent as BaseProjectContent
from apps.core.models import BaseModel


class ProjectContent(BaseModel):
    content_item = models.ForeignKey(
        BaseProjectContent,
        on_delete=CASCADE,
        related_name="project_contents",
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
        verbose_name = "Объект содержимого проекта"
        verbose_name_plural = "Объекты содержимого проектов"


class Project(BaseModel):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    contents = models.ManyToManyField(
        BaseProjectContent,
        through=ProjectContent,
    )

    def __str__(self):
        return f"Проект {self.name}"

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class NewsItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название новости",
    )
    contents = models.ManyToManyField(BaseProjectContent)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class BlogItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
