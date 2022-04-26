from django.db import models
from django.db.models.constraints import UniqueConstraint

from apps.content_pages.models import AbstractContent, AbstractContentPage
from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.models import BaseModel, Person, Role


class BlogPerson(BaseModel):
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
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        limit_choices_to={"types__role_type": "blog_persons_role"},
        related_name="blog_persons",
        verbose_name="Роль в соавторстве",
    )

    class Meta:
        verbose_name = "Соавтор блога"
        verbose_name_plural = "Соавторы блогов"
        ordering = ("role",)
        constraints = (
            UniqueConstraint(
                fields=(
                    "person",
                    "blog",
                    "role",
                ),
                name="unique_person_role_per_blog",
            ),
        )

    def __str__(self):
        return f"{self.role} - {self.person.full_name}"


class BlogItem(AbstractContentPage):
    author_url = models.URLField(
        verbose_name="Ссылка на автора записи",
    )
    author_url_title = models.CharField(
        max_length=50,
        verbose_name="Подпись/название ссылки на автора",
    )
    roles = models.ManyToManyField(
        Role,
        through=BlogPerson,
        related_name="blogs",
        verbose_name="Роли",
    )
    image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        verbose_name="Заглавная картинка",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Запись блога"
        verbose_name_plural = "Блог"
        permissions = (
            ("access_level_1", "Права журналиста"),
            ("access_level_2", "Права редактора"),
            ("access_level_3", "Права главреда"),
        )

    def __str__(self):
        return f"Запись блога {self.title}"

    def get_class_name(self):
        return self.__class__.__name__


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
