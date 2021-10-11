from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.afisha.models import CommonEvent
from apps.core.models import BaseModel, Person
from apps.info.models import Festival


class ProgramType(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название программы",
    )

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.name


class Play(BaseModel):
    authors = models.ManyToManyField(
        "Author",
        related_name="plays",
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
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1990),
            MaxValueValidator(timezone.now().year),
        ],
        unique=True,
        verbose_name="Год написания пьесы",
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
        constraints = [
            UniqueConstraint(
                fields=["name", "festival"],
                name="unique_play",
            )
        ]
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


class Achievement(BaseModel):
    tag = models.CharField(
        max_length=40,
        verbose_name="Достижения в виде тега",
        help_text="Не более 40 символов",
    )

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return self.tag


class Author(BaseModel):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    quote = models.CharField(
        max_length=200,
        verbose_name="Цитата",
    )
    biography = models.TextField(
        max_length=3000,
        verbose_name="Текст про автора",
    )
    achievements = models.ManyToManyField(
        Achievement,
        verbose_name="Достижения",
    )
    social_network_links = models.ManyToManyField(
        "SocialNetworkLink",
        verbose_name="Ссылки на социальные сети",
        related_name="authors",
    )
    other_links = models.ManyToManyField(
        "OtherLink",
        verbose_name="Ссылки на внешние ресурсы",
        related_name="authors",
    )
    authors_plays_links = models.ManyToManyField(
        Play,
        verbose_name="Ссылки на пьесы автора",
        related_name="authors_links",
    )
    other_plays_links = models.ManyToManyField(
        "OtherPlay",
        blank=True,
        verbose_name="Ссылки на другие пьесы",
        related_name="authors_links",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name}"

    def clean(self):
        if not self.person.email:
            raise ValidationError("Для автора необходимо указать email")
        if not self.person.city:
            raise ValidationError("Для автора необходимо указать город")
        if not self.person.image:
            raise ValidationError("Для автора необходимо выбрать фото")


class SocialNetworkLink(BaseModel):
    class SocialNetwor(models.TextChoices):
        FACEBOOK = "fb", _("Facebook")
        INSTAGRAM = "inst", _("Instagram")
        YOUTUBE = "ytube", _("YouTube")
        TELEGRAM = "tlgrm", _("Telegram")
        VKONTAKTE = "vk", _("Вконтакте")

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=200,
        choices=SocialNetwor.choices,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=500,
        verbose_name="Ссылка",
    )

    class Meta:
        verbose_name = "Ссылка на социальную сеть"
        verbose_name_plural = "Ссылки на социальные сети"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "name"],
                name="unique_social_network",
            )
        ]

    def __str__(self):
        return self.name


class OtherLink(BaseModel):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=500,
        verbose_name="Ссылка",
    )
    is_pinned = models.BooleanField(
        verbose_name="Закрепить ссылку",
        help_text="Закрепить ссылку вверху страницы?",
    )
    order_number = models.PositiveSmallIntegerField(
        verbose_name="Порядковый номер",
        help_text="Указывается для формирования порядка вывода информации",
    )

    class Meta:
        ordering = ["order_number"]
        verbose_name = "Ссылка на сторонний ресурс"
        verbose_name_plural = "Ссылки на стороннии ресурсы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "name"],
                name="unique_link",
            )
        ]

    def __str__(self):
        return self.name


class OtherPlay(BaseModel):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=40,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=1000,
        verbose_name="Ссылка на скачивание файла",
    )

    class Meta:
        verbose_name = "Другая пьеса"
        verbose_name_plural = "Другие пьесы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "name"],
                name="unique_other_play",
            )
        ]

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
        related_name="readings",
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
        related_name="director_readings",
        verbose_name="Режиссер",
    )
    dramatist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="dramatist_readings",
        verbose_name="Драматург",
    )
    event = models.OneToOneField(
        CommonEvent,
        on_delete=models.PROTECT,
        related_name="readings",
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
        related_name="director_masterclasses",
        verbose_name="Режиссер",
    )
    dramatist = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="dramatist_masterclasses",
        verbose_name="Драматург",
    )
    host = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="leading_masterclasses",
        verbose_name="Ведущий",
    )
    event = models.OneToOneField(
        CommonEvent,
        on_delete=models.PROTECT,
        related_name="masterclasses",
        verbose_name="Заголовок события",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Мастер-класс"
        verbose_name_plural = "Мастер-классы"

    def __str__(self):
        return self.name


class ParticipationApplicationFestival(BaseModel):
    first_name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name="Фамилия",
    )
    birthday = models.DateField(
        verbose_name="День рождения",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
    )
    phone_number = PhoneNumberField()
    email = models.EmailField(
        max_length=100,
        verbose_name="Электронная почта",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название пьесы",
    )
    year = models.CharField(
        max_length=4,
        verbose_name="Год написания",
    )
    file_link = models.URLField(
        verbose_name="Ссылка на файл",
    )
    status = models.BooleanField(
        verbose_name="Статус",
    )

    class Meta:
        verbose_name_plural = "Заявления на участие"
        verbose_name = "Заявление на участие"

    def __str__(self):
        return self.title
