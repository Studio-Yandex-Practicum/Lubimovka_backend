from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q, UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Image, Person


class FestivalTeamMember(BaseModel):
    class TeamType(models.TextChoices):
        ART_DIRECTION = "art", _("Арт-дирекция фестиваля")
        FESTIVAL_TEAM = "fest", _("Команда фестиваля")

    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
        blank=True,
        null=True,
    )
    team = models.CharField(
        max_length=5,
        choices=TeamType.choices,
        verbose_name="Тип команды",
    )
    position = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )
    is_pr_manager = models.BooleanField(
        default=False,
        verbose_name="PR-директор",
        help_text="Поставьте галочку, чтобы назначить человека PR-директором",
    )

    class Meta:
        verbose_name = "Команда фестиваля"
        verbose_name_plural = "Команды фестиваля"
        ordering = ("person__last_name", "person__first_name")
        constraints = [
            UniqueConstraint(
                fields=("person", "team"),
                name="unique_person_team",
            )
        ]

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - " f"{self.team}"

    def clean(self):
        if not self.person:
            raise ValidationError("Необходимо указать человека для создания команды фестиваля")
        if not self.person.email:
            raise ValidationError("Для члена команды необходимо указать email")
        if not self.person.city:
            raise ValidationError("Для члена команды необходимо указать город")
        if not self.person.image:
            raise ValidationError("Для члена команды необходимо выбрать фото")
        if not FestivalTeamMember.objects.filter(Q(team=self.team) & Q(person=self.person)).exists():
            raise ValidationError("Этот человек уже в составе команды.")
        if not self.is_pr_manager:
            hasAnotherPrManager = FestivalTeamMember.objects.filter(
                Q(is_pr_manager=True) & Q(person=self.person)
            ).exists()
            if hasAnotherPrManager:
                raise ValidationError(
                    "Для того чтобы снять с должности PR-директора, "
                    "нужно назначить другого человека на эту должность"
                )

    def delete(self, *args, **kwargs):
        if self.is_pr_manager:
            raise ValidationError("Перед удалением назначьте на должность PR-директора другого человека")
        super().delete(*args, **kwargs)


class ArtTeamMember(FestivalTeamMember):
    class Meta:
        proxy = True
        verbose_name = "Арт-дирекция фестиваля"
        verbose_name_plural = "Арт-дирекция фестиваля"


class FestTeamMember(FestivalTeamMember):
    class Meta:
        proxy = True
        verbose_name = "Команда фестиваля"
        verbose_name_plural = "Команда фестиваля"


class Festival(BaseModel):
    start_date = models.DateField(
        verbose_name="Дата начала фестиваля",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания фестиваля",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Описание фестиваля",
    )
    year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(1990), MaxValueValidator(2500)],
        unique=True,
        verbose_name="Год фестиваля",
    )
    images = models.ManyToManyField(
        Image,
        related_name="festivalimages",
        verbose_name="Изображения",
    )
    plays_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Общее количество пьес",
    )
    selected_plays_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество отобранных пьес",
    )
    selectors_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество отборщиков пьес",
    )
    volunteers_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество волонтёров фестиваля",
    )
    events_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество событий фестиваля",
    )
    cities_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Количество участвующих городов",
    )
    video_link = models.URLField(
        max_length=250,
        verbose_name="Ссылка на видео о фестивале",
    )
    blog_entries = models.CharField(
        max_length=100,
        verbose_name="Записи в блоге о фестивале",  # Ждет создание сущности
        blank=True,
    )  # При изменении - скорректировать фабрику в части создания данного поля
    press_release_image = models.ImageField(
        upload_to="images/info/press_releases",
        blank=True,
        verbose_name="Изображение для страницы пресс-релизов",
    )

    class Meta:
        verbose_name = "Фестиваль"
        verbose_name_plural = "Фестивали"
        ordering = ["-year"]
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date")),
            )
        ]

    def __str__(self):
        return f"Фестиваль {self.year} года"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError({"end_date": _("Дата окончания фестиваля должна быть позже даты его начала.")})
        return super().clean()


class PressRelease(BaseModel):
    title = models.CharField(max_length=500, unique=True, verbose_name="Заголовок")
    text = RichTextField(verbose_name="Текст")
    festival = models.OneToOneField(
        Festival,
        on_delete=models.CASCADE,
        related_name="press_releases",
        verbose_name="Фестиваль",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Пресс-релиз"
        verbose_name_plural = "Пресс-релизы"

    def __str__(self):
        return f"Пресс-релиз {self.festival__year} года"

    @property
    def festival__year(self):
        return self.festival.year
