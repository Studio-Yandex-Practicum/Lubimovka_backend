from django.db import models

from apps.content_pages.utilities import path_by_app_label_and_class_name
from apps.core.mixins import FileCleanUpMixin
from apps.core.models import CORE_ROLES, BaseModel, Person
from apps.library.utilities import get_team_roles


class Reading(FileCleanUpMixin, BaseModel):
    cleanup_fields = ("main_image",)
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    custom_type = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Описание вида события",
    )
    play = models.ForeignKey(
        "library.Play",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="readings",
        verbose_name="Пьеса",
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
        related_name="custom",
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
        verbose_name = "специальное событие"
        verbose_name_plural = "специальные события"

    def __str__(self):
        if len(self.name) >= 25:
            return self.name[:25] + "..."
        return self.name

    @property
    def event_team(self):
        """Return team members filtered by roles specified in this method."""
        return get_team_roles(self, {"team_members__reading": self, "slug__in": CORE_ROLES})
