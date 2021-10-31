from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class StaticPagesModel(BaseModel):
    class PageType(models.TextChoices):
        WHAT_WE_DO = "what-we-do", _('Страница "Что мы делаем"')
        IDEOLOGY = "ideology", _('Страница "Идеология"')
        HISTORY = "history", _('Страница "История"')

    page_type = models.CharField(
        max_length=10,
        choices=PageType.choices,
        verbose_name="Название страницы",
    )
    data = models.TextField(
        verbose_name="Данные, отображаемые на странице",
        help_text=format_lazy(
            """
            Для того, чтобы загурзить картинку, перетащите её в поле.
            Как пользоваться разметкой Markdown, нажмите <a href='{}'>СЮДА</a>.
            """,
            "https://ru.wikipedia.org/wiki/Markdown",
        ),
    )

    class Meta:
        verbose_name = "Статическая страница"
        verbose_name_plural = "Статические страницы"
        constraints = (
            UniqueConstraint(
                fields=("page_type",),
                name="unique_static_page",
            ),
        )

    def __str__(self):
        return self.page_type
