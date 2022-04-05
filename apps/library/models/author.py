from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, Person

from .play import Play


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
        verbose_name="Человек",
        related_name="authors",
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
        related_name="authors",
        blank=True,
    )
    plays = models.ManyToManyField(
        Play,
        related_name="authors",
        blank=True,
        verbose_name="Пьесы автора",
        through="AuthorPlays",
    )
    slug = models.SlugField(
        "Транслит фамилии для формирования адресной строки",
        unique=True,
        help_text="Формируется автоматически, может быть изменен вручную",
        error_messages={"unique": "Такой транслит уже используется, введите иной"},
    )

    class Meta:
        ordering = ("person__last_name",)
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.person.last_name} {self.person.first_name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self._has_person_before_saving():
            if not self.person.city:
                raise ValidationError("Для автора необходимо указать город")

    def _has_person_before_saving(self):
        return self.person_id is not None

    @property
    def image(self):
        return self.person.image


class AuthorPlays(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="author_plays",
        verbose_name="Пьесы автора",
    )
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="author_plays",
        verbose_name="Пьесы автора",
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name="Порядковый номер пьесы у автора",
    )

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"Пьеса {self.play} - автор {self.author}"


class SocialNetworkLink(BaseModel):
    class SocialNetwork(models.TextChoices):
        FACEBOOK = "fb", _("Facebook")
        INSTAGRAM = "inst", _("Instagram")
        YOUTUBE = "ytube", _("YouTube")
        TELEGRAM = "tlgrm", _("Telegram")
        VKONTAKTE = "vk", _("Вконтакте")

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="social_networks",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=200,
        choices=SocialNetwork.choices,
        verbose_name="Название",
    )
    link = models.URLField(
        max_length=500,
        verbose_name="Ссылка",
    )

    class Meta:
        verbose_name = "Ссылка на социальную сеть"
        verbose_name_plural = "Ссылки на социальные сети"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "author",
                    "name",
                ),
                name="unique_social_network",
            ),
        )

    def __str__(self):
        return self.name


class OtherLink(BaseModel):
    author = models.ForeignKey(
        Author,
        related_name="other_links",
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
        ordering = ("order_number",)
        verbose_name = "Публикации и другие материалы"
        verbose_name_plural = "Публикации и другие материалы"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "author",
                    "name",
                ),
                name="unique_link",
            ),
        )

    def __str__(self):
        return self.name
