from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Image


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


class Person(BaseModel):
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
    )
    email = models.EmailField(
        max_length=200,
        verbose_name="Электронная почта",
    )
    image = models.ImageField(
        upload_to="images/person_avatars",
        verbose_name="Фотография",
    )

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ("last_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    appointment = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )

    class Meta:
        verbose_name = "Команда фестиваля"
        verbose_name_plural = "Команды фестиваля"

    def __str__(self):
        return (
            f"{self.person.first_name} {self.person.last_name} - "
            f"{self.team}"
        )


class Trustee(BaseModel):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name="Человек",
    )
    appointment = models.CharField(
        max_length=150,
        verbose_name="Должность",
    )

    class Meta:
        verbose_name = "Попечитель фестиваля"
        verbose_name_plural = "Попечители фестиваля"

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"


class FestivalVolunteer(BaseModel):
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

    class Meta:
        verbose_name = "Волонтёр фестиваля"
        verbose_name_plural = "Волонтёры фестиваля"

    def __str__(self):
        return (
            f"{self.person.first_name} {self.person.last_name} - волонтёр "
            f"фестиваля {self.year} года"
        )


class VolunteerReview(BaseModel):
    volunteer = models.ForeignKey(
        FestivalVolunteer,
        on_delete=models.PROTECT,
        verbose_name="Волонтёр",
    )
    review = models.TextField(
        verbose_name="Текст отзыва",
    )

    class Meta:
        verbose_name = "Отзыв волонтёра"
        verbose_name_plural = "Отзывы волнтёров"

    def __str__(self):
        return (
            f"Отзыв волонтёра {self.volunteer.person.first_name} "
            f"{self.volunteer.person.last_name}"
        )


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
        verbose_name="Год фестиваля",
    )
    team = models.ManyToManyField(
        FestivalTeam,
        related_name="festivalteams",
        verbose_name="Арт-дирекция и команда",
        blank=False,
    )
    trustees = models.ManyToManyField(
        Trustee,
        related_name="festivaltrustees",
        verbose_name="Попечители фестиваля",
        blank=False,
    )
    volunteers = models.ManyToManyField(
        FestivalVolunteer,
        related_name="festivalvolunteers",
        verbose_name="Волонтёры фестиваля",
        blank=False,
    )
    reviews = models.ManyToManyField(
        VolunteerReview,
        related_name="volunteerreviews",
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
    video_linl = models.URLField(
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
