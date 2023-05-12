from django.db import models

from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.mixins import ImageCleanUpMixin
from apps.core.models import CORE_ROLES, BaseModel, Person
from apps.library.utilities import get_team_roles


class Reading(ImageCleanUpMixin, BaseModel):
    cleanup_fields = ("main_image",)
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
    main_image = models.ImageField(
        upload_to=path_by_app_label_and_class_name,
        blank=True,
        null=True,
        verbose_name="Главное изображение",
    )
    intro = models.TextField(
        max_length=500,
        verbose_name="Дополнительное описание",
        blank=True,
        help_text="Описание, расположенное под изображением",
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
        """Return team members filtered by roles specified in this method."""
        return get_team_roles(self, {"team_members__reading": self, "slug__in": CORE_ROLES})
