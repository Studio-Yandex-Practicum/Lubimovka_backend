from django.db import models

from apps.core.models import BaseModel


class Place(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(max_length=255, verbose_name="Описание")
    city = models.CharField(max_length=50, verbose_name="Город")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    map_link = models.URLField(verbose_name="Ссылка на карту")

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "city"),
                name="unique_place",
            ),
        ]

    def __str__(self):
        return self.name
