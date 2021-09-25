import datetime

from django.db import models
from django.core.validators import RegexValidator

from apps.core.models import BaseModel


class NewsItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название новости",
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class BlogItem(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Project(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название проекта",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class PresentPiece(BaseModel):
    first_name = models.CharField(max_length=200, verbose_name="Имя")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="День рождения")
    city = models.CharField(max_length=50, verbose_name="Город проживания")
    phone_regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    phone_number = models.CharField(
        max_length=12,
        validators=[RegexValidator(regex=phone_regex)],
        verbose_name="Номер телефона",
    )
    email = models.EmailField(max_length=100, verbose_name="Электронная почта")
    title = models.CharField(max_length=200, verbose_name="Название пьесы")
    year = models.CharField(
        max_length=4,
        verbose_name="Год написания",
        default=datetime.date.today().year,
    )
    file_link = models.URLField(verbose_name="Ссылка на файл")
    status = models.BooleanField(verbose_name="Статус")
