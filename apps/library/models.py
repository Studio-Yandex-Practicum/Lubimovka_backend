import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import BaseModel


class Play(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название пьесы",
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name="Черновик",
    )

    class Meta:
        verbose_name = "Пьеса"
        verbose_name_plural = "Пьесы"


class Performance(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название спектакля",
    )

    class Meta:
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"


class Author(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя автора",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class PerformanceMediaReview(BaseModel):
    text = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Медиа отзыв на спектакль"
        verbose_name_plural = "Медиа отзывы на спектакль"


class PerformanceReview(BaseModel):
    text = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Отзыв зрителя на спектакль"
        verbose_name_plural = "Отзывы зрителей на спектакль"


class ParticipationApplicationFestival(BaseModel):
    first_name = models.CharField(max_length=200, verbose_name="Имя")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="День рождения")
    city = models.CharField(max_length=50, verbose_name="Город проживания")
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=100, verbose_name="Электронная почта")
    title = models.CharField(max_length=200, verbose_name="Название пьесы")
    year = models.CharField(
        max_length=4,
        verbose_name="Год написания",
        default=datetime.date.today().year,
    )
    file_link = models.URLField(verbose_name="Ссылка на файл")
    status = models.BooleanField(verbose_name="Статус")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Заявления на участие'
        verbose_name = 'Заявление на участие'
