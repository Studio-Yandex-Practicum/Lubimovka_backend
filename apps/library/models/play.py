from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.content_pages.utilities import path_by_media_and_class_name
from apps.core.mixins import FileCleanUpMixin
from apps.core.models import BaseModel
from apps.core.utils import slugify
from apps.info.models import Festival
from apps.library.validators import year_validator


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
        ordering = ("id",)
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


ALLOWED_FORMATS_FILE_FOR_PLAY = (
    "doc",
    "docx",
    "txt",
    "odt",
    "pdf",
)


class Play(FileCleanUpMixin, BaseModel):
    cleanup_fields = ("url_download",)
    name = models.CharField(
        max_length=200,
        verbose_name="Название пьесы",
    )
    city = models.CharField(
        max_length=200,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        verbose_name="Год представления пьесы",
        blank=True,
        null=True,
    )
    url_download = models.FileField(
        validators=(FileExtensionValidator(ALLOWED_FORMATS_FILE_FOR_PLAY),),
        max_length=200,
        blank=True,
        null=True,
        upload_to=path_by_media_and_class_name,
        verbose_name="Текст пьесы",
        help_text=f"Файл пьесы должен быть в одном из следующих форматов: " f"{ALLOWED_FORMATS_FILE_FOR_PLAY}",
    )
    url_download_from = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на скачивание",
    )
    url_reading = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на читку",
        unique=True,
    )
    programs = models.ManyToManyField(
        ProgramType,
        related_name="plays",
        verbose_name="Программа",
        blank=True,
        help_text="Для пьес Любимовки должна быть выбрана хотя бы одна Программа.",
    )

    festival = models.ForeignKey(
        Festival,
        on_delete=models.PROTECT,
        related_name="plays",
        verbose_name="Фестиваль",
        blank=True,
        null=True,
        help_text="Для пьес Любимовки должен быть выбран Фестиваль",
    )
    published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )
    other_play = models.BooleanField(
        verbose_name="Сторонняя пьеса",
        default=False,
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
        ordering = ("name",)

    def __str__(self):
        return (
            self.name
            + ("" if self.published else " <— 🔴 пьеса не опубликована —>")
            + ("" if not self.other_play else " <— Другая пьеса —>")
        )

    def clean(self):
        if self.other_play:
            if self.pk:
                self.programs.clear()
            self.festival = None
            self.url_reading = None
        elif not self.festival:
            raise ValidationError({"festival": "У пьесы Любимовки должен быть фестиваль"})
        if (self.url_download and self.url_download_from) or (not self.url_download and not self.url_download_from):
            raise ValidationError(
                {
                    "url_download": "",
                    "url_download_from": _(
                        "Необходимо либо загрузить файл с текстом Пьесы, либо указать ссылку на скачивание",
                    ),
                }
            )
        return super().clean()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.url_download.path:
            return
        regular_play_file = Path(self.url_download.path)
        hidden_play_file: Path = settings.HIDDEN_MEDIA_ROOT / regular_play_file.relative_to(settings.MEDIA_ROOT)
        if self.published and not regular_play_file.is_file() and hidden_play_file.is_file():
            # Вернуть файл из скрытого хранилища в общее
            hidden_play_file.replace(regular_play_file)
        elif not self.published and regular_play_file.is_file():
            # Переместить файл из общего хранилища в скрытое
            regular_play_file.replace(hidden_play_file)
        return super().save(*args, **kwargs)
