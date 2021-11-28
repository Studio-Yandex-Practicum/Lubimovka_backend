from django.db import models
from django.db.models.constraints import UniqueConstraint

from apps.content_pages.models import AbstractContent, AbstractContentPage
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

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Блог"
        ordering = ("-pub_date",)

    def __str__(self):
        return f"Запись блога {self.title}"


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
