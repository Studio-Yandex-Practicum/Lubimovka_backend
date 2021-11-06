from django.db import models

from apps.content_pages.models import AbstractContent, AbstractContentPage


class BlogItem(AbstractContentPage):
    image = models.ImageField(
        upload_to="images/blog/",
        blank=True,
        verbose_name="Заглавная картинка записи",
    )
    author_url = models.URLField(
        verbose_name="Ссылка на автора записи",
    )
    author_url_title = models.CharField(
        max_length=50,
        verbose_name="Подпись/название ссылки на автора",
    )

    def __str__(self):
        return f"Запись блога {self.title}"

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Блог"


class BlogItemContent(AbstractContent):
    """Custom ContentPage model for BlogItem models.

    It's required to set 'content_page' foreign key to concrete or proxy
    model.
    """

    content_page = models.ForeignKey(
        BlogItem,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Запись блога с конструктором",
    )

    class Meta:
        verbose_name = "Блок/элемент конструктора записи блога"
        verbose_name_plural = "Блоки/элементы конструктора записей блога"
        ordering = ("order",)
