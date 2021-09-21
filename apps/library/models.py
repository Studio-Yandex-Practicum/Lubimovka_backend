from django.db import models

from apps.core.models import BaseModel


class Play(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название пьесы",
    )

    class Meta:
        verbose_name = "Пьеса"
        verbose_name_plural = "Пьесы"


class Spectacle(BaseModel):
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


class MediaReviewSpectacle(BaseModel):
    text = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Медиа отзыв на спектакль"
        verbose_name_plural = "Медиа отзывы на спектакль"


class WatcherReviewSpectacle(BaseModel):
    text = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Отзыв зрителя на спектакль"
        verbose_name_plural = "Отзывы зрителей на спектакль"


class DraftPlay(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название пьесы",
    )

    class Meta:
        verbose_name = "Черновик пьесы"
        verbose_name_plural = "Черновики пьес"
