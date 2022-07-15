from django.db import models

from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.models import BaseModel, Person
from apps.library.utilities import get_team_roles


class MasterClass(BaseModel):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
    )
    persons = models.ManyToManyField(
        Person,
        through="library.TeamMember",
        related_name="masterclasses",
        verbose_name="Члены команды",
    )
    events = models.OneToOneField(
        "afisha.CommonEvent",
        on_delete=models.PROTECT,
        related_name="masterclass",
        verbose_name="События",
    )
    main_image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        blank=True,
        null=True,
        verbose_name="Главное изображение",
    )
    project = models.ForeignKey(
        "articles.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="masterclasses",
        verbose_name="Проект",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Мастер-класс"
        verbose_name_plural = "Мастер-классы"

    def __str__(self):
        if len(self.name) >= 25:
            return self.name[:25] + "..."
        return self.name

    @property
    def event_team(self):
        """Return hosts related with MasterClass."""
        return get_team_roles(self, {"team_members__masterclass": self, "slug__in": ["host"]})
