from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Image, Person


class Partner(BaseModel):
    class PartnerType(models.IntegerChoices):
        GENERAL_PARTNER = 1, _("Генеральный партнер")
        FESTIVAL_PARTNER = 2, _("Партнер фестиваля")
        INFO_PARTNER = 3, _("Информационный партнер")

    name = models.CharField(
        max_length=200,
        verbose_name="Наименование",
    )
    type = models.CharField(
        max_length=2,
        choices=PartnerType.choices,
        verbose_name="Тип",
    )
    url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на сайт",
    )
    picture = models.ImageField(
        upload_to="images/info/partnerslogo",
        verbose_name="Логотип",
    )
    image = models.CharField(
        max_length=200,
        verbose_name="Логотип",
    )

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return f"{self.name} - {self.type}"


class Question(BaseModel):
    question = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Текст вопроса",
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class FestivalTeam(BaseModel):
    class TeamType(models.IntegerChoices):
        ART_DIRECTION = 1, _("Арт-дирекция фестиваля")
        FESTIVAL_TEAM = 2, _("Команда фестиваля")

    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    team = models.SmallIntegerField(
        choices=TeamType.choices,
        verbose_name="Тип команды",
    )
    position = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )

    class Meta:
        verbose_name = "Команда фестиваля"
        verbose_name_plural = "Команды фестиваля"
        constraints = [
            UniqueConstraint(
                fields=["person", "team"],
                name="unique_person_team",
            )
        ]

    def __str__(self):
        return (
            f"{self.person.first_name} {self.person.last_name} - "
            f"{self.team}"
        )

    def clean(self):
        team_person = FestivalTeam.objects.filter(
            person=self.person, team=self.team
        )
        if self not in team_person and team_person:
            raise ValidationError("Этот человек уже есть в этой команде")


class Sponsor(BaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    position = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )

    class Meta:
        verbose_name = "Попечитель фестиваля"
        verbose_name_plural = "Попечители фестиваля"
        constraints = [
            UniqueConstraint(
                fields=["person", "position"],
                name="unique_sponsor",
            )
        ]

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"


class Volunteer(BaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(1990), MaxValueValidator(2500)],
        verbose_name="Год участия в фестивале",
    )
    review = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Волонтёр фестиваля"
        verbose_name_plural = "Волонтёры фестиваля"
        constraints = [
            UniqueConstraint(
                fields=["person", "year"],
                name="unique_volunteer",
            )
        ]

    def __str__(self):
        return (
            f"{self.person.first_name} {self.person.last_name} - волонтёр "
            f"фестиваля {self.year} года"
        )

    def clean(self):
        volunteer = Volunteer.objects.filter(
            person=self.person, year=self.year
        )
        if self not in volunteer and volunteer:
            raise ValidationError("Волонтёр уже в участниках фестиваля")


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
    teams = models.ManyToManyField(
        FestivalTeam,
        related_name="festivalteams",
        verbose_name="Арт-дирекция и команда",
        blank=False,
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name="festivalsponsors",
        verbose_name="Попечители фестиваля",
        blank=False,
    )
    volunteers = models.ManyToManyField(
        Volunteer,
        related_name="volunteers",
        verbose_name="Волонтёры фестиваля",
        blank=False,
    )
    reviews = models.CharField(  # Не придумал ещё реализацию
        max_length=3,
        verbose_name="Отзывы волонтёров о фестивале",
    )
    images = models.ManyToManyField(
        Image,
        related_name="festivalimages",
        verbose_name="Изображения",
    )
    programms = models.CharField(
        max_length=10,
        verbose_name="Программы фестиваля",  # Ждет создание сущности
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
        verbose_name="Количество учавствующих городов",
    )
    video_link = models.URLField(
        max_length=250,
        verbose_name="Ссылка на видео о фестивале",
    )
    blog_entries = models.CharField(
        max_length=10,
        verbose_name="Записи в блоге о фестивале",  # Ждет создание сущности
    )

    class Meta:
        verbose_name = "Фестиваль"
        verbose_name_plural = "Фестивали"
        ordering = ["-year"]

    def __str__(self):
        return f"Фестиваль {self.year} года"
