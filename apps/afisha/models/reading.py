from django.db import models

from apps.core.models import BaseModel, Person
from apps.library.utilities import get_team_roles


class Reading(BaseModel):
    play = models.ForeignKey(
        "library.Play",
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
    persons = models.ManyToManyField(
        Person,
        through="library.TeamMember",
        related_name="readings",
        verbose_name="Члены команды",
    )
    events = models.OneToOneField(
        "afisha.CommonEvent",
        on_delete=models.PROTECT,
        related_name="reading",
        verbose_name="События",
    )
    project = models.ForeignKey(
        "articles.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="readings",
        verbose_name="Проект",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Читка"
        verbose_name_plural = "Читки"

    def __str__(self):
        if len(self.name) >= 25:
            return self.name[:25] + "..."
        return self.name

    @property
    def event_team(self):
        """Return directors and dramatists related with Reading."""
        return get_team_roles(self, {"team_members__reading": self, "slug__in": ["director", "dramatist"]})
