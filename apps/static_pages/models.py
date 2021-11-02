from django.db import models
from django.utils.text import format_lazy

from apps.core.models import BaseModel


class StaticPagesModel(BaseModel):
    title = models.CharField(
        max_length=30,
        verbose_name="Название страницы",
        unique=True,
    )
    static_page_url = models.SlugField(
        max_length=30,
        verbose_name="Путь к странице",
        unique=True,
    )
    data = models.TextField(
        verbose_name="Данные, отображаемые на странице",
        help_text=format_lazy(
            """
            Для того, чтобы загрузить картинку, перетащите её в поле.
            Как пользоваться разметкой Markdown, нажмите <a href='{}'>СЮДА</a>.
            """,
            "https://www.markdownguide.org/basic-syntax/",
        ),
    )

    class Meta:
        verbose_name = "Статическая страница"
        verbose_name_plural = "Статические страницы"

    def __str__(self):
        return self.title
