from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.afisha.models import CommonEvent
from apps.core.models import BaseModel, Image, Person
from apps.core.utilities.slugify import slugify
from apps.info.models import Festival
from apps.library.validators import year_validator


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
        blank=True,
    )
    social_network_links = models.ManyToManyField(
        "SocialNetworkLink",
        verbose_name="Ссылки на социальные сети",
        related_name="authors",
        blank=True,
    )
    other_links = models.ManyToManyField(
        "OtherLink",
        verbose_name="Ссылки на внешние ресурсы",
        related_name="authors",
        blank=True,
    )
    author_plays_links = models.ManyToManyField(
        Play,
        verbose_name="Ссылки на пьесы автора",
        related_name="authors_links",
        blank=True,
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


class Performance(BaseModel):
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
    event = models.OneToOneField(
        CommonEvent,
        on_delete=models.PROTECT,
        related_name="performances",
        verbose_name="Базовое событие",
    )
    main_image = models.ImageField(
        upload_to="performances/",
        verbose_name="Главное изображение",
    )
    bottom_image = models.ImageField(
        upload_to="performances/",
        verbose_name="Изображение внизу страницы",
    )
    images_in_block = models.ManyToManyField(
        Image,
        verbose_name="Фотографии спектакля в блоке фотографий",
        blank=True,
    )
    video = models.URLField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name="Видео",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Краткое описание",
    )
    text = models.TextField(
        verbose_name="Полное описание",
    )
    age_limit = models.PositiveSmallIntegerField(
        verbose_name="Возрастное ограничение",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(18),
        ],
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Спектакль"
        verbose_name_plural = "Спектакли"

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

    @property
    def director_full_name(self):
        return f"{self.director.first_name} {self.director.last_name}"

    @property
    def dramatist_ful_name(self):
        return f"{self.dramatist.first_name} {self.dramatist.last_name}"

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

    @property
    def host_full_name(self):
        return f"{self.host.first_name} {self.host.last_name}"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Мастер-класс"
        verbose_name_plural = "Мастер-классы"

    def __str__(self):
        return self.name


def get_upload_to(instance, filename):
    festival = Festival.objects.last()
    return f"application/{festival.year}/{filename}"


class ParticipationApplicationFestival(BaseModel):
    """
    Участники, отправившие свои заявки
    """

    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
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
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        verbose_name="Год написания",
    )
    file = models.FileField(
        validators=[
            FileExtensionValidator(["doc", "docx", "txt", "odt", "pdf"])
        ],
        verbose_name="Файл",
        upload_to=get_upload_to,
    )

    BOOL_CHOICES = ((True, "Да"), (False, "Нет"))
    verified = models.BooleanField(
        default=False,
        verbose_name="Проверена?",
        choices=BOOL_CHOICES,
    )

    class Meta:
        verbose_name_plural = "Заявления на участие"
        verbose_name = "Заявление на участие"

    def __str__(self):
        return self.get_filename

    @property
    def get_filename(self):
        first_name = slugify(self.first_name)
        if "-" in first_name:
            first_name = first_name.replace("-", "_")

        title = slugify(self.title)
        if "-" in title:
            title = title.replace("-", "_")
        return (
            f"{first_name.title()}-{title.title()}.{self.get_file_extension}"
        )

    @property
    def get_file_extension(self):
        return self.file.name.split(".")[1]

    def save(self, *args, **kwargs):
        """
        Generate new filename as "First_name-Title" format
        """

        self.file.name = self.get_filename
        super().save(*args, **kwargs)
