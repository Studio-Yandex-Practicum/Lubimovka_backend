from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.deletion import CASCADE

from apps.content_pages.fields import OrderField
from apps.core.models import BaseModel


class ContentPage(BaseModel):
    title = models.CharField(max_length=200)
    overview = models.TextField()

    class Meta:
        ordering = ["-modified"]

    def __str__(self):
        return self.title


class Content(models.Model):
    content_page = models.ForeignKey(
        ContentPage,
        related_name="contents",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "video",
                "image",
                "file",
                "imagesblock",
            )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey()
    order = OrderField(
        blank=True,
        for_fields=["content_page"],
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Блок сложной верстки — {self.item}"


class ItemBase(BaseModel):
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class ImagesBlock(ItemBase):
    images = models.ManyToManyField(
        to=Image,
        through="OrderedImage",
    )


class OrderedImage(models.Model):
    image = models.ForeignKey(
        Image,
        on_delete=CASCADE,
        related_name="ordered_images",
    )
    image_block = models.ForeignKey(
        ImagesBlock,
        on_delete=CASCADE,
        related_name="ordered_images",
    )
    order = OrderField(
        blank=True,
        for_fields=["image_block"],
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} — {self.image}"


class Video(ItemBase):
    url = models.URLField()


class ExampleObject(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Имя примера",
    )
    conten_page = models.ForeignKey(
        ContentPage,
        related_name="examples",
        verbose_name="Страница с сложной версткой",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Пример с сложной версткой"
        verbose_name_plural = "Примеры с сложной версткой"
