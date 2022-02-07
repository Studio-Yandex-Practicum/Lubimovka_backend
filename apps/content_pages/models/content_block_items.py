from django.db import models

from apps.core.models import BaseModel


class AbstractContentBlockItem(BaseModel):
    """Abstract model for `contet_block`.

    The model have common `order` field that is required to order items in block.
    """

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядок в блоке",
    )

    class Meta:
        verbose_name = "Содержимое блока"
        verbose_name_plural = "Содержимое блоков"
        abstract = True
        ordering = ("order",)

    def __str__(self):
        return f"{self.order} — {self.item}"


class ContentImagesBlockItem(AbstractContentBlockItem):
    title = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Заголовок",
        help_text="Заголовок/подпись для картинки. Может быть пустым",
    )
    image = models.ImageField(
        upload_to="content_images",
        verbose_name="Изображение",
    )
    block = models.ForeignKey(
        "ImagesBlock",
        on_delete=models.CASCADE,
        related_name="block_items",
    )

    def __str__(self):
        return f"Изображение {self.order}"
