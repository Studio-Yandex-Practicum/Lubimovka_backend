from django.contrib import admin

from apps.core.mixins import AdminImagePreview, InlineReadOnlyMixin, StatusButtonMixin
from apps.core.models import Role
from apps.library.models import (
    MasterClass,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
    Reading,
    TeamMember,
)


class ImagesInBlockInline(InlineReadOnlyMixin, admin.TabularInline, AdminImagePreview):
    model = Performance.images_in_block.through
    verbose_name = "Изображение в блоке изображений"
    verbose_name_plural = "Изображения в блоке изображений"
    autocomplete_fields = ("image",)
    extra = 0
    max_num = 8
    classes = ["collapse"]
    model.__str__ = lambda self: ""


class PerformanceMediaReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceMediaReview
    extra = 0
    max_num = 8
    classes = ["collapse"]


class PerformanceReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceReview
    extra = 0
    max_num = 8
    classes = ["collapse"]


class TeamMemberInline(InlineReadOnlyMixin, admin.TabularInline):
    model = TeamMember
    fields = (
        "person",
        "role",
    )
    autocomplete_fields = (
        "person",
        "role",
    )
    extra = 0
    classes = ["collapse"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Restricts role types for the model where inline is used."""
        LIMIT_ROLES = {
            Performance: "performanse_role",
            Play: "play_role",
            MasterClass: "master_class_role",
            Reading: "reading_role",
        }
        if db_field.name == "role":
            if self.parent_model in LIMIT_ROLES.keys():
                kwargs["queryset"] = Role.objects.filter(types__role_type=LIMIT_ROLES[self.parent_model])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("events",)
    search_fields = (
        "project",
        "play__name",
        "name",
    )
    inlines = (TeamMemberInline,)


@admin.register(Performance)
class PerformanceAdmin(StatusButtonMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "play",
        "status",
    )
    fields = (
        "status",
        "name",
        "play",
        "main_image",
        "bottom_image",
        "video",
        "description",
        "text",
        "age_limit",
        "project",
        "duration",
    )
    list_filter = (
        "age_limit",
        "status",
    )
    search_fields = (
        "play__name",
        "name",
        "text",
    )
    readonly_fields = ("status",)
    other_readonly_fields = (
        "status",
        "name",
        "play",
        "main_image",
        "bottom_image",
        "video",
        "description",
        "text",
        "age_limit",
        "project",
        "duration",
    )
    inlines = (
        ImagesInBlockInline,
        PerformanceMediaReviewInline,
        PerformanceReviewInline,
        TeamMemberInline,
    )


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "play",
        "name",
    )
    exclude = ("events",)
    search_fields = (
        "play__name",
        "name",
    )
    inlines = (TeamMemberInline,)
