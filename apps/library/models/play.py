from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint

from apps.content_pages.utilities import path_by_file_app_label_and_class_name
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


class Play(BaseModel):
    name = models.CharField(
        max_length=70,
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
        verbose_name="Год написания пьесы",
        blank=True,
        null=True,
    )
    url_download = models.FileField(
        validators=(FileExtensionValidator(ALLOWED_FORMATS_FILE_FOR_PLAY),),
        max_length=200,
        upload_to=path_by_file_app_label_and_class_name,
        verbose_name="Текст пьесы",
        help_text=f"Файл пьесы должен быть в одном из следующих форматов: " f"{ALLOWED_FORMATS_FILE_FOR_PLAY}",
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
        blank=True,
        null=True,
        help_text="Для пьес Любимовки должна быть выбрана Программа",
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
        ordering = ("-year", "name")

    def __str__(self):
        return (
            self.name
            + ("" if self.published else " <— 🔴 пьеса не опубликована —>")
            + ("" if not self.other_play else " <— Другая пьеса —>")
        )

    def clean(self):
        if self.other_play:
            self.festival = None
            self.program = None
            self.url_reading = None
        elif not self.program:
            raise ValidationError({"program": "У пьесы Любимовки должна быть программа"})
        elif not self.festival:
            raise ValidationError({"festival": "У пьесы Любимовки должен быть фестиваль"})
        return super().clean()
