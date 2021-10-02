from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Person


class Play(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название пьесы",
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name="Черновик",
    )

    class Meta:
        verbose_name = "Пьеса"
        verbose_name_plural = "Пьесы"


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
        related_name="authors",
    )
    other_plays_links = models.ManyToManyField(
        "OtherPlay",
        blank=True,
        verbose_name="Ссылки на другие пьесы",
        related_name="authors",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.person


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
                name="unique_social_networ",
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
                name="unique_play",
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
