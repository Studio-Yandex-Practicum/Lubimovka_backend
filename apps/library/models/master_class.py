from django.db import models

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
        through="TeamMember",
        related_name="masterclasses",
        verbose_name="Члены команды",
    )
    events = models.OneToOneField(
        "afisha.CommonEvent",
        on_delete=models.PROTECT,
        related_name="masterclass",
        verbose_name="События",
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
        return self.name

    @property
    def event_team(self):
        """Return hosts related with MasterClass."""
        return get_team_roles(self, {"team_members__masterclass": self, "slug__in": ["host"]})
