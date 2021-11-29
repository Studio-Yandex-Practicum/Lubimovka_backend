from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class Banner(BaseModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка",
    )
    image = models.ImageField(
        upload_to="images/main/banner",
        verbose_name="Картинка",
    )

    class Meta:
        verbose_name = "Банер для главной странице"
        verbose_name_plural = "Банеры для главной странице"

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if Banner.objects.count() >= 3 and not self.id:
            raise ValidationError("Can not create more than 3 banners")
