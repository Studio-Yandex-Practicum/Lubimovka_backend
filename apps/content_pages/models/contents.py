from typing import Tuple

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from apps.content_pages.querysets import PublishedContentQuerySet
from apps.content_pages.services import content_delete_generic_related_items
from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.constants import Status
from apps.core.models import BaseModel


class AbstractContentPage(BaseModel):
    """Шаблон модели с конструктором.

    Для создания полноценной модели с конструктором создайте две новые модели
    унаследовав их от 'AbstractContentPage' и 'AbstractContent'.

    Модель обладает обычными полями (title, description, image, status,
    pub_date). К ней подключается блок с конструктором.

    Дополнена расширенным manager (`ext_objects`) для более простого
    доступа к часто используемым данным (пример: получить только опубликованные
    записи)
    """

    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        blank=True,
        verbose_name="Заглавная картинка",
    )
    status = models.CharField(
        choices=Status.choices,
        default=Status.IN_PROCESS,
        max_length=35,
        verbose_name="Статус",
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата публикации",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )

    objects = PublishedContentQuerySet.as_manager()

    class Meta:
        abstract = True
        verbose_name = "Шаблон объекта с сложной версткой"
        verbose_name_plural = "Шаблоны объектов с сложной версткой"
        ordering = ("-modified",)

    def __str__(self):
        return self.title


class AbstractContent(models.Model):
    """Шаблон базового блока конструктора.

    При наследовании укажите модель к которой будут подключаться блоки
    конструктора (реальную модель вместо 'AbstractContentPage' в поле
    'content_page').

    Для ограничения количества типов объектов в конструкторе задайте их список
    переопределив поле 'content' и атрибут 'limit_choices_to'.

    Описание полей:
        1. 'content_page' - foreign key для подключения к родительской
            'AbstractContentPage' модели
        2. 'item' - элемент 'контента'. Так как элементы контента могут быть
            разных типов реализуется с помощью ключа GenereForeginKey и двух
            дополнительных полей.
                - content_type = указывает на модель с типом контента
                - object_id = указывает на id объекта типа 'content_type'
            Т.е. 3 поля в сумме дают GenereForeginKey.
            Если остаются вопросы по реализации пожалуйста смотрите
            документацию django.
        3. 'order' — поле для упорядочивания блоков конструктора относительно
            родительского 'AbstractContentPage' объекта.
    """

    content_page = models.ForeignKey(
        AbstractContentPage,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Страница с конструктором",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "app_label": "content_pages",
            "model__in": (
                "contentunitrichtext",
                "eventsblock",
                "imagesblock",
                "link",
                "personsblock",
                "playsblock",
                "videosblock",
            ),
        },
        verbose_name="Тип объекта",
    )
    object_id = models.PositiveIntegerField(
        verbose_name="ID объекта",
    )
    item = GenericForeignKey()
    order = models.PositiveSmallIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок",
    )

    class Meta:
        abstract = True
        ordering = ("order",)
        verbose_name = "Блок/элемент конструктора"
        verbose_name_plural = "Блоки/элементы конструктора"

    def __str__(self):
        return f"Блок/элемент — {self.item}"

    def delete(self, *args, **kwargs) -> Tuple[int, dict[str, int]]:
        """Delete related item with generic relation."""
        super_delete_result = super().delete(*args, **kwargs)
        return content_delete_generic_related_items(self, super_delete_result)
