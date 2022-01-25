from django.db import models

from apps.core.models import BaseModel, Person

from .play import Play


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
    persons = models.ManyToManyField(
        Person,
        through="TeamMemberReading",
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
        return self.name
