from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import BaseModel


class AbstractContentPage(BaseModel):
    """Model with basic CMS functionality.

    The model is abstract. Please subclass it and 'Content' model to create
    new model with CMS functionality.
    """

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок страницы",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание страницы",
    )

    class Meta:
        abstract = True
        verbose_name = "Шаблон объекта с сложной версткой"
        verbose_name_plural = "Шаблоны объектов с сложной версткой"
        ordering = ["-modified"]

    def __str__(self):
        return self.title


class AbstractContent(models.Model):
    """The base block of the CMS ='ContentPage' object.

    The model is abstract. Please subclass it and set the right 'ContenPage'
    model in 'content_type' field.
    You can also limit available models for 'content' with 'limit_choices_to'
    attribute.

    The block has several fields/attributes:
        1. foreign key to 'parent' ContentPage object
        2. 'content' element. The type of 'content' objects may vary.
            To handle it we have to use GenereForeginKey relation and 3 fields:
                - content_type
                - object_id
                - item
            Please go through django-docs for any question.
        3. 'order' field. It is used for managing the order of the 'content'
            elements in 'parent' object.
    """

    content_page = models.ForeignKey(
        AbstractContentPage,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Блок элементов сложной верстки",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "content_pages"},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True
        ordering = ["order"]
        verbose_name = "Элемент сложной верстки"
        verbose_name_plural = "Элементы сложной верстки"

    def __str__(self):
        return f"Блок сложной верстки — {self.item}"
