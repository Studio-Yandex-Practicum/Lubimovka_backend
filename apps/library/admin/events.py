from django.contrib import admin
from django.db import models

from apps.core.mixins import AdminImagePreview, InlineReadOnlyMixin, StatusButtonMixin
from apps.core.models import Role
from apps.core.utils import get_user_change_perms_for_status
from apps.core.widgets import AutocompleteSelectWithRestriction, FkSelect
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
    extra = 0
    max_num = 8
    classes = ("collapsible",)
    model.__str__ = lambda self: ""


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
    # formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}

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
    # formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}


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
    # formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}
    limited_fk_fields = ("play",)

    def formfield_for_dbfield(self, db_field: models.Field, request, **kwargs):
        db = kwargs.get("using")
        if db_field.name in self.autocomplete_fields and db_field.name in self.limited_fk_fields:
            kwargs["widget"] = AutocompleteSelectWithRestriction(db_field, self.admin_site, using=db)
        elif db_field.name in self.limited_fk_fields:
            kwargs["widget"] = FkSelect
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        change_permission = get_user_change_perms_for_status(request, obj)
        if change_permission:
            form.base_fields["play"].queryset = Play.objects.filter(other_play=False)
        return form


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "play",
        "name",
    )
    exclude = ("events",)
    search_fields = (
        "name",
        "play__name",
    )
    autocomplete_fields = ("play",)
    inlines = (TeamMemberInline,)
    # formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["play"].queryset = Play.objects.filter(other_play=False)
        return form
