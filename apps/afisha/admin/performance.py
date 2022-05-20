from django.contrib import admin

from apps.afisha.models.masterclass import MasterClass
from apps.afisha.models.performance import Performance
from apps.afisha.models.performance_media_review import PerformanceImage, PerformanceMediaReview, PerformanceReview
from apps.afisha.models.reading import Reading
from apps.core.mixins import AdminImagePreview, InlineReadOnlyMixin, PreviewButtonMixin, StatusButtonMixin
from apps.core.models import Role
from apps.core.utils import get_user_change_perms_for_status
from apps.library.models import Play, TeamMember


class ImagesInBlockInline(InlineReadOnlyMixin, admin.TabularInline, AdminImagePreview):
    model = PerformanceImage
    verbose_name = "Изображение в блоке изображений"
    verbose_name_plural = "Изображения в блоке изображений"
    extra = 0
    max_num = 8
    classes = ("collapsible",)
    model.__str__ = lambda self: ""
    readonly_fields = ("image_preview_list_page",)


class PerformanceMediaReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceMediaReview
    extra = 0
    max_num = 8
    classes = ("collapsible",)


class PerformanceReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceReview
    extra = 0
    max_num = 8
    classes = ("collapsible",)


class TeamMemberInline(InlineReadOnlyMixin, admin.TabularInline):
    model = TeamMember
    fields = (
        "person",
        "role",
    )
    autocomplete_fields = ("person",)
    extra = 0

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


class TeamMemberInlineCollapsible(TeamMemberInline):
    classes = ("collapsible",)


@admin.register(Performance)
class PerformanceAdmin(StatusButtonMixin, PreviewButtonMixin, admin.ModelAdmin):
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
    autocomplete_fields = ("play",)
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
        TeamMemberInlineCollapsible,
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        change_permission = get_user_change_perms_for_status(request, obj)
        if change_permission:
            form.base_fields["play"].queryset = Play.objects.filter(other_play=False)
        return form
