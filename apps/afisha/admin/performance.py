from django.contrib import admin

from apps.afisha.models import Performance, PerformanceImage, PerformanceMediaReview, PerformanceReview
from apps.content_pages.filters import CreatorFilter
from apps.content_pages.mixins import SaveCreatorMixin
from apps.core.mixins import AdminImagePreview, InlineReadOnlyMixin, PreviewButtonMixin, StatusButtonMixin
from apps.library.admin import TeamMemberInlineCollapsible


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


@admin.register(Performance)
class PerformanceAdmin(StatusButtonMixin, PreviewButtonMixin, SaveCreatorMixin, admin.ModelAdmin):
    list_display = (
        "short_name",
        "short_description",
        "play",
        "status",
        "creator_name",
        "created",
    )
    fields = (
        "status",
        "name",
        "play",
        "main_image",
        "bottom_image",
        "video",
        "description",
        "supplemental_text",
        "text",
        "age_limit",
        "project",
        "duration",
        "block_images_description",
        "creator_name",
    )
    list_filter = (
        "age_limit",
        "status",
        CreatorFilter,
    )
    autocomplete_fields = ("play",)
    search_fields = (
        "play__name",
        "name",
        "text",
        "creator__first_name",
        "creator__last_name",
    )
    readonly_fields = ("status", "creator_name")
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
        "creator_name",
    )
    inlines = (
        ImagesInBlockInline,
        PerformanceMediaReviewInline,
        PerformanceReviewInline,
        TeamMemberInlineCollapsible,
    )
    ordering = ("-created",)

    class Media:

        js = ("admin/afisha/js/DurationValidation.js",)
