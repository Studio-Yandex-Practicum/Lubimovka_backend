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

    It's required to set 'content_page' foreign key to concrete or proxy
    model.
    """

    content_page = models.ForeignKey(
        Project,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Проект с конструктором",
    )

    class Meta:
        verbose_name = "Блок/элемент конструктора проекта"
        verbose_name_plural = "Блоки/элементы конструктора проектов"
        ordering = ("order",)
