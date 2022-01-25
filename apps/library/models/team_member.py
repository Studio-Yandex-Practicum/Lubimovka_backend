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
                    "masterclass",
                ),
                name="unique_person_role_per_masterclass",
            ),
        )

    def __str__(self):
        return f"{self.role} - {self.person.full_name}"


class TeamMemberReading(BaseModel):
    reading = models.ForeignKey(
        Reading,
        on_delete=models.CASCADE,
        related_name="team_members",
        verbose_name="Читка",
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="team_members_reading",
        verbose_name="Член команды",
    )
    role = models.ManyToManyField(
        "core.Role",
        limit_choices_to={"types__role_type": "reading_role"},
        related_name="team_members_reading",
        verbose_name="Роль",
    )

    class Meta:
        ordering = ("person",)
        verbose_name = "Член команды читки"
        verbose_name_plural = "Члены команды читки"
        constraints = (
            UniqueConstraint(
                fields=(
                    "person",
                    "reading",
                ),
                name="unique_person_with_roles_per_reading",
            ),
        )

    def __str__(self):
        return self.person.full_name
