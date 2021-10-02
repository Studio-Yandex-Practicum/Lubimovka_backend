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
        if not self.person.email:
            raise ValidationError("Для члена команды необходимо указать email")
        if not self.person.city:
            raise ValidationError("Для члена команды необходимо указать город")
        if not self.person.image:
            raise ValidationError("Для члена команды необходимо выбрать фото")


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

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"

    def clean(self):
        sponsor = Sponsor.objects.filter(person=self.person)
        if self not in sponsor and sponsor:
            raise ValidationError("Этот человек уже есть в попечителях")
        if not self.person.image:
            raise ValidationError("Для спонсора необходимо выбрать его фото")


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
        if not self.person.email:
            raise ValidationError("Укажите email для волонтёра")
        if not self.person.image:
            raise ValidationError("Для волонтёра необходимо выбрать его фото")


class Place(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    city = models.CharField(max_length=50, verbose_name="Город")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    map_link = models.URLField(verbose_name="Ссылка на карту")

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "city"], name="unique_place"
            ),
        ]

    def __str__(self):
        return self.name


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


class Question(BaseModel):
    question = models.CharField(
        max_length=500,
        verbose_name="Текст вопроса",
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    email = models.EmailField(
        max_length=50,
        verbose_name="Электронная почта",
    )

    class Meta:
        verbose_name = "Вопрос или предложение"
        verbose_name_plural = "Вопросы или предложения"

    def __str__(self):
        return f"{self.name} {self.question}"
