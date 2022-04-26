from django.db import models

from apps.content_pages.models import AbstractContent, AbstractContentPage


class NewsItem(AbstractContentPage):
    def __str__(self):
        return f"Новость {self.title}"

    def get_class_name(self):
        return self.__class__.__name__

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        permissions = (
            ("access_level_1", "Права журналиста"),
            ("access_level_2", "Права редактора"),
            ("access_level_3", "Права главреда"),
        )


class NewsItemContent(AbstractContent):
    """Custom ContentPage model for NewsItem models.

    It's required to set 'content_page' foreign key to concrete or proxy
    model.
    """

    content_page = models.ForeignKey(
        NewsItem,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Запись блога с конструктором",
    )

    class Meta:
        verbose_name = "Блок/элемент конструктора новости"
        verbose_name_plural = "Блоки/элементы конструктора новостей"
        ordering = ("order",)
