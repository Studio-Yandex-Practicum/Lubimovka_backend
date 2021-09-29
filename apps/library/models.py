from django.db import models

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

    def __str__(self):
        return self.name


class Author(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя автора",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class PerformanceMediaReview(BaseModel):
    media_name = models.CharField(
        max_length=100,
        verbose_name="Название медиа ресурса",
    )
    text = models.TextField(
        max_length=500,
        verbose_name="Текст отзыва",
    )
    image = models.ImageField(
        upload_to='reviews/',
        verbose_name="Изображение",
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.PROTECT,
        related_name="media_reviews",
        verbose_name="Спектакль",
    )
    url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка на отзыв",
        unique=True,
    )
    pub_date = models.DateTimeField(
        blank=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Медиа отзыв на спектакль"
        verbose_name_plural = "Медиа отзывы на спектакль"

    def __str__(self):
        return self.media_name


class PerformanceReview(BaseModel):
    reviewer_name = models.CharField(
        max_length=100,
        verbose_name="Имя зрителя",
    )
    text = models.TextField(
        max_length=500,
        verbose_name="Текст отзыва",
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.PROTECT,
        related_name="reviews",
        verbose_name="Спектакль",
    )
    url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка на отзыв",
        unique=True,
    )
    pub_date = models.DateTimeField(
        blank=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Отзыв зрителя на спектакль"
        verbose_name_plural = "Отзывы зрителей на спектакль"

    def __str__(self):
        return self.reviewer_name
