from django.db import models

from apps.core.models import BaseModel

PARTNERS_CHOICES = (
    (1, "Генеральный партнер"),
    (2, "Партнер фестиваля"),
    (3, "Информационный партнер"),
)


class Partner(BaseModel):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    type = models.CharField(
        max_length=2, choices=PARTNERS_CHOICES, verbose_name="Тип"
    )
    url = models.URLField(max_length=200, verbose_name="Ссылка на сайт")
    # picture = models.ImageField(
    #    upload_to='info/',
    #    verbose_name='Логотип'
    # )
    image = models.CharField(max_length=200, verbose_name="Логотип")

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return "{} {}".format(self.name, self.type)
