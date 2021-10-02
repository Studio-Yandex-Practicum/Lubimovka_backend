from django.db import models

from apps.core.models import BaseModel, Person
from apps.info.models import Festival


class EventHeader(BaseModel):

    class Meta:
        ordering = ("-created",)
        verbose_name = "Заголовок события"
        verbose_name_plural = "Заголовки событий"


class Author(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя автора",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Program(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название программы",
    )

    def __str__(self):
        return self.name


class Play(BaseModel):
    author = models.ManyToManyField(
        Author,
        related_name="author_play",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название пьесы",
    )
    city = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Город",
    )
    url_download = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка на скачивание пьесы",
        unique=True,
    )
    url_reading = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка на читку",
        unique=True,
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="program_play",
        verbose_name="Программа",
    )
    festival = models.ForeignKey(
        Festival,
        on_delete=models.PROTECT,
        related_name="festival_play",
        verbose_name="Фестиваль",
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name="Черновик",
    )

    class Meta:
        unique_together = ('name', 'festival')
        verbose_name = "Пьеса"
        verbose_name_plural = "Пьесы"

    def __str__(self):
        return self.name


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
        upload_to="reviews/",
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
        ordering = ("-created",)
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
        ordering = ("-created",)
        verbose_name = "Отзыв зрителя на спектакль"
        verbose_name_plural = "Отзывы зрителей на спектакль"

    def __str__(self):
        return self.reviewer_name


class Reading(BaseModel):
    play = models.ForeignKey(
        Play,
        on_delete=models.PROTECT,
        related_name="play_reading",
        verbose_name="Пьеса",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    director = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="director_reading",
        verbose_name="Режиссер",
    )
    dramatist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="dramatist_reading",
        verbose_name="Драматург",
    )
    event = models.OneToOneField(
        EventHeader,
        on_delete=models.PROTECT,
        related_name="event_reading",
        verbose_name="Заголовок события",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Читка"
        verbose_name_plural = "Читки"

    def __str__(self):
        return self.name


class MasterClass(BaseModel):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    director = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="director_masterclass",
        verbose_name="Режиссер",
    )
    dramatist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="dramatist_masterclass",
        verbose_name="Драматург",
    )
    leading = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="leading_masterclass",
        verbose_name="Ведущий",
    )
    event = models.OneToOneField(
        EventHeader,
        on_delete=models.PROTECT,
        related_name="event_masterclass",
        verbose_name="Заголовок события",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Мастер-класс"
        verbose_name_plural = "Мастер-классы"

    def __str__(self):
        return self.name
