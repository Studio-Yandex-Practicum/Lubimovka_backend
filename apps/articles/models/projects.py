from django.db import models
from django.db.models.constraints import UniqueConstraint

from apps.content_pages.models import AbstractContent, AbstractContentPage
from apps.content_pages.utilities import path_by_app_label_and_class_name


class Project(AbstractContentPage):
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Заглавная картинка",
    )
    intro = models.TextField(
        max_length=200,
        verbose_name="Интро к проекту",
        help_text="Короткое интро к проекту. Показывается в списке проектов с заголовком.",
    )

    def __str__(self):
        return f"Проект {self.title}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("intro", "description", "title"),
                name="unique_project",
            ),
        ]
        ordering = ("-pub_date",)
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        permissions = (
            ("access_level_1", "Права журналиста"),
            ("access_level_2", "Права редактора"),
            ("access_level_3", "Права главреда"),
        )


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
