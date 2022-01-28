from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

from apps.core.models import BaseModel
from apps.core.utilities import slugify
from apps.info.models import Festival


class ProgramType(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название программы",
    )
    slug = models.SlugField(
        max_length=40,
        verbose_name="Slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Play(BaseModel):
    name = models.CharField(
        max_length=70,
        unique=True,
        verbose_name="Название пьесы",
    )
    city = models.CharField(
        max_length=200,
        verbose_name="Город",
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2200),
        ],
        verbose_name="Год написания пьесы",
    )
    url_download = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на скачивание пьесы",
        unique=True,
    )
    url_reading = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на читку",
        unique=True,
    )
    program = models.ForeignKey(
        ProgramType,
        on_delete=models.PROTECT,
        related_name="plays",
        verbose_name="Программа",
    )
    festival = models.ForeignKey(
        Festival,
        on_delete=models.PROTECT,
        related_name="plays",
        verbose_name="Фестиваль",
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name="Черновик",
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("name", "festival"),
                name="unique_play",
            ),
        )
        verbose_name = "Пьеса"
        verbose_name_plural = "Пьесы"

    def __str__(self):
        return self.name

    def clean(self):
        if self.year > timezone.now().year:
            raise ValidationError("Год написания пьесы не может быть больше текущего")
        return super().clean()
