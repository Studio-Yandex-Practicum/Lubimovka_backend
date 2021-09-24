from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Partner(BaseModel):
    class PartnerType(models.IntegerChoices):
        GENERAL_PARTNER = 1, _("Генеральный партнер")
        FESTIVAL_PARTNER = 2, _("Партнер фестиваля")
        INFO_PARTNER = 3, _("Информационный партнер")

    name = models.CharField(
        max_length=200,
        verbose_name="Наименование",
    )
    type = models.CharField(
        max_length=2,
        choices=PartnerType.choices,
        verbose_name="Тип",
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на сайт",
    )
    picture = models.ImageField(
        upload_to="info/",
        verbose_name="Логотип",
    )
    image = models.CharField(
        max_length=200,
        verbose_name="Логотип",
    )

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return "{} {}".format(self.name, self.type)


class Question(BaseModel):
    question = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Текст вопроса",
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Place(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    city = models.CharField(max_length=50, verbose_name="Город")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    map_link = models.URLField(verbose_name="Ссылка на карту")

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"

    def __str__(self):
        return self.name

    def clean(self):
        place = Place.objects.filter(name=self.name, city=self.city)
        if place and self not in place:
            raise ValidationError("Такая площадка уже существует")
