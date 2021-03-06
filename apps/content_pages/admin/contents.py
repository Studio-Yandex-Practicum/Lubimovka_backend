from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db import models

from apps.content_pages.admin.widgets import GfkHiddenInput, GfkSelect
from apps.content_pages.filters import CreatorFilter
from apps.content_pages.mixins import SaveCreatorMixin
from apps.content_pages.models import AbstractContent
from apps.core.mixins import AdminImagePreview


class BaseContentInline(SortableInlineAdminMixin, admin.TabularInline):
    """Extends StackedInline for a bit more convenient work in the admin panel.

    It do 4 things:
    1. Set custom widget to `object_id` field. It's original HiddenInput widget
    with custom class `content-pages-object-id`.
    2. Add `content_type` to `raw_id_fields`. It's required to turn off
    wrapprig the field with `RelatedFieldWidgetWrapper` (it's common behavior
    for ModelAdmin or InlineAdmin forms).
    2. Set custom widget to `content_type` field. The widget do:
        - add class `content-pages-content-type` to the field.
        - add `genericForeignKeyAddChange.js`. It's responsible to disable
        choose options and create links to add or change objects.
    3. Adds sortable abilities with 'SortableInlineAdminMixin'
    """

    model = AbstractContent
    extra = 0
    raw_id_fields = ("content_type",)
    formfield_overrides = {
        models.PositiveIntegerField: {"widget": GfkHiddenInput},
        models.ForeignKey: {"widget": GfkSelect},
    }


class BaseContentPageAdmin(AdminImagePreview, SaveCreatorMixin, admin.ModelAdmin):
    """Base admin class for ContentPage objects."""

    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
    )
    list_filter = ("status", CreatorFilter)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "pub_date",
                    "description",
                    ("image_preview_change_page", "image"),
                    "status",
                )
            },
        ),
    )
    search_fields = (
        "title",
        "description",
        "creator__first_name",
        "creator__last_name",
    )
    readonly_fields = ("image_preview_change_page", "pub_date")
