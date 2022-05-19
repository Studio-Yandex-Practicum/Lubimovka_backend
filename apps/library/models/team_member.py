from django.db import models
from django.db.models import Q

from apps.afisha.models.masterclass import MasterClass
from apps.afisha.models.performance import Performance
from apps.afisha.models.reading import Reading
from apps.core.models import BaseModel, Person


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
            models.UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "performance",
                ),
                name="unique_person_role_per_performance",
            ),
            models.UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "reading",
                ),
                name="unique_person_role_per_reading",
            ),
            models.UniqueConstraint(
                fields=(
                    "person",
                    "role",
                    "masterclass",
                ),
                name="unique_person_role_per_masterclass",
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_only_one_of_reading_masterclass_performance",
                check=(
                    Q(
                        performance__isnull=False,
                        reading__isnull=True,
                        masterclass__isnull=True,
                    )
                    | Q(
                        performance__isnull=True,
                        reading__isnull=False,
                        masterclass__isnull=True,
                    )
                    | Q(
                        performance__isnull=True,
                        reading__isnull=True,
                        masterclass__isnull=False,
                    )
                ),
            ),
        )

    def __str__(self):
        return f"{self.role} - {self.person.full_name}"
