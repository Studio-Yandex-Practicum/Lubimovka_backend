from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars

from apps.content_pages.querysets import PublishedContentQuerySet
from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.constants import AgeLimit, Status
from apps.core.mixins import FileCleanUpMixin
from apps.core.models import CORE_ROLES, BaseModel, Person
from apps.library.utilities import get_team_roles

User = get_user_model()


class Performance(FileCleanUpMixin, BaseModel):
    cleanup_fields = ("main_image", "bottom_image")
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
        "library.Play",
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
        blank=True,
    )
    intro = models.TextField(
        max_length=500,
        verbose_name="Дополнительное описание",
        blank=True,
        help_text="Описание, расположенное под изображением",
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
        through="library.TeamMember",
        related_name="performances",
        verbose_name="Члены команды",
    )
    duration = models.DurationField(
        default=timedelta(minutes=85),
        verbose_name="Продолжительность",
        help_text="Введите продолжительность в формате ЧЧ:ММ",
    )
    block_images_description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default=None,
        verbose_name="Заголовок для фотографий",
        help_text="Опишите блок с фотографиями",
    )
    objects = PublishedContentQuerySet.as_manager()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель",
    )

    @property
    def custom_type(self):
        return "Спектакль"

    class Meta:
        ordering = ("name",)
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
        """Return team members filtered by roles specified in this method."""
        return get_team_roles(self, {"team_members__performance": self, "slug__in": CORE_ROLES})

    @property
    def short_name(self):
        """Get short performace name."""
        return truncatechars(self.name, 70)

    @property
    def short_description(self):
        """Get short description."""
        return truncatechars(self.description, 70)

    short_name.fget.short_description = "Название cпектакля"
    short_description.fget.short_description = "Краткое описание"
