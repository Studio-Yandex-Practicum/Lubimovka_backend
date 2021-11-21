from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.content_pages.models import AbstractContent, AbstractContentPage
from apps.core.models import BaseModel, Person


class BlogPerson(BaseModel):
    class BlogAuthorRole(models.TextChoices):
        TEXT = "TEXT", _("Текст")
        PHOTO = "PHOTO", _("Фото")
        ILLUSTRATION = "ILLUSTRATION", _("Иллюстрации")

    person = models.ForeignKey(
        Person,
        on_delete=models.RESTRICT,
        related_name="blog_persons",
        verbose_name="Соавтор блога",
    )
    blog = models.ForeignKey(
        "BlogItem",
        on_delete=models.CASCADE,
        related_name="blog_persons",
        verbose_name="Блог",
    )
    role = models.CharField(
        max_length=50,
        choices=BlogAuthorRole.choices,
        verbose_name="Роль в соавторстве",
    )

    class Meta:
        ordering = ("role",)
        verbose_name = "Соавтор блога"
        verbose_name_plural = "Соавторы блогов"

    def __str__(self):
        return f"{self.role} - {self.person}"


class BlogItem(AbstractContentPage):
    author_url = models.URLField(
        verbose_name="Ссылка на автора записи",
    )
    author_url_title = models.CharField(
        max_length=50,
        verbose_name="Подпись/название ссылки на автора",
    )
    image = models.ImageField(
        upload_to="images/blog/",
        blank=True,
        verbose_name="Заглавная картинка записи",
    )
    blogs = models.ManyToManyField(
        "BlogItem",
        blank=True,
        related_name="linked_blogs",
        verbose_name="Другие записи блогов",
    )
    persons = models.ManyToManyField(
        Person,
        through=BlogPerson,
        related_name="blogs",
        verbose_name="Соавторы",
    )
    preamble = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Преамбула",
    )

    def __str__(self):
        return f"Запись блога {self.title}"

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Блог"


class BlogItemContent(AbstractContent):
    """Custom ContentPage model for BlogItem models.

    It's required to set 'content_page' foreign key to concrete or proxy
    model.
    """

    content_page = models.ForeignKey(
        BlogItem,
        related_name="contents",
        on_delete=models.CASCADE,
        verbose_name="Запись блога с конструктором",
    )

    class Meta:
        verbose_name = "Блок/элемент конструктора записи блога"
        verbose_name_plural = "Блоки/элементы конструктора записей блога"
        ordering = ("order",)
