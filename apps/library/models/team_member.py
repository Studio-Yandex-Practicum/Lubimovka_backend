from django.db import models
from django.db.models import UniqueConstraint

from apps.core.models import BaseModel, Person

from .master_class import MasterClass
from .performance import Performance
from .reading import Reading


class TeamMember(BaseModel):
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="team_members",
        verbose_name="Спектакль",
    )
    reading = models.ForeignKey(
        Reading,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="team_members",
        verbose_name="Читка",
    )
    masterclass = models.ForeignKey(
        MasterClass,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="team_members",
        verbose_name="Мастер-класс",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="team_members",
        verbose_name="Член команды",
    )
    role = models.ForeignKey(
        "core.Role",
        on_delete=models.PROTECT,
        related_name="team_members",
        verbose_name="Роль",
    )

    class Meta:
        ordering = ("role",)
        verbose_name = "Член команды"
        verbose_name_plural = "Члены команды"
        constraints = (
            UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "performance",
                ),
                name="unique_person_role_per_performance",
            ),
            UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "reading",
                ),
                name="unique_person_role_per_reading",
            ),
            UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "masterclass",
                ),
                name="unique_person_role_per_masterclass",
            ),
        )

    def __str__(self):
        return f"{self.role} - {self.person.full_name}"
