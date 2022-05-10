from datetime import timedelta

from django.db import models

from apps.content_pages.querysets import PublishedContentQuerySet
from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.constants import AgeLimit, Status
from apps.core.models import BaseModel, Image, Person
from apps.library.utilities import get_team_roles

from .play import Play


class Performance(BaseModel):
    status = models.CharField(
        choices=Status.choices,
        default=Status.IN_PROCESS,
        max_length=35,
        verbose_name="Статус",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название спектакля",
    )
    play = models.ForeignKey(
        Play,
        on_delete=models.PROTECT,
        related_name="performances",
        verbose_name="Пьеса",
    )
    events = models.OneToOneField(
        "afisha.CommonEvent",
        on_delete=models.PROTECT,
        related_name="performance",
        verbose_name="События",
    )
    main_image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Главное изображение",
    )
    bottom_image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Изображение внизу страницы",
    )
    images_in_block = models.ManyToManyField(
        Image,
        blank=True,
        verbose_name="Фотографии спектакля в блоке фотографий",
    )
    video = models.URLField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Видео",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Краткое описание",
    )
    text = models.TextField(
        max_length=2000,
        verbose_name="Полное описание",
    )
    age_limit = models.IntegerField(
        verbose_name="Возрастное ограничение",
        choices=AgeLimit.choices,
        default=AgeLimit.NO_LIMIT,
    )
    persons = models.ManyToManyField(
        Person,
        through="TeamMember",
        related_name="performances",
        verbose_name="Члены команды",
    )
    project = models.ForeignKey(
        "articles.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="performances",
        verbose_name="Проект",
    )
    duration = models.DurationField(
        default=timedelta(minutes=85),
        verbose_name="Продолжительность",
    )
    objects = PublishedContentQuerySet.as_manager()

    class Meta:
        ordering = ("-created",)
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"
        permissions = (
            ("access_level_1", "Права журналиста"),
            ("access_level_2", "Права редактора"),
            ("access_level_3", "Права главреда"),
        )

    def __str__(self):
        if len(self.name) >= 25:
            return self.name[:25] + "..."
        return self.name

    @property
    def team(self):
        """Return all team members."""
        return get_team_roles(self, {"team_members__performance": self})

    @property
    def event_team(self):
        """Return directors and dramatists related with Performance."""
        return get_team_roles(self, {"team_members__performance": self, "slug__in": ["director", "dramatist"]})


class PerformanceMediaReview(BaseModel):
    media_name = models.CharField(
        max_length=100,
        verbose_name="Название медиа ресурса",
    )
    text = models.TextField(
        max_length=2000,
        verbose_name="Текст отзыва",
    )
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
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
        null=True,
        verbose_name="Ссылка на отзыв",
        unique=True,
    )
    pub_date = models.DateTimeField(
        blank=True,
        null=True,
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
        max_length=2000,
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
        null=True,
        verbose_name="Ссылка на отзыв",
        unique=True,
    )
    pub_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Отзыв зрителя на спектакль"
        verbose_name_plural = "Отзывы зрителей на спектакль"

    def __str__(self):
        return self.reviewer_name
