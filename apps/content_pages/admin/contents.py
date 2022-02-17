from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.content_pages.admin.widgets import GfkHiddenInput, GfkSelect
from apps.content_pages.models import AbstractContent
from apps.core.mixins import AdminImagePreview


class BaseContentInline(SortableInlineAdminMixin, admin.TabularInline):
    """Extends StackedInline for a bit more convenient work in the admin panel.

    It do 4 things:
    1. Set custom widget to `object_id` field. It's original HiddenInput widget
    with custom class `content-pages-object-id`.
    2. Add `content_type` to `raw_id_fields`. It;s required to turn off
    wrapprig the field with `RelatedFieldWidgetWrapper` (it's common behavior
    for ModelAdmin or InlineAdmin forms).
    2. Set custom widget to `content_type` field. The widget do:
        - add class `content-pages-content-type` to the field.
        - add `genericForeignKeyAddChange.js`. It's responsible to disable
        choose options and create links to add or change objects.
    3. Limit 'content_type' models to choose from in admin.
    4. Adds sortable abilities with 'SortableInlineAdminMixin'
    """

    model = AbstractContent
    extra = 0
    raw_id_fields = ("content_type",)
    content_type_model = tuple()
    formfield_overrides = {
        models.PositiveIntegerField: {"widget": GfkHiddenInput},
        models.ForeignKey: {"widget": GfkSelect},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limits avaliable models to choose while creating ContentPage object."""
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(
                model__in=self.content_type_model,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BaseContentPageAdmin(AdminImagePreview, admin.ModelAdmin):
    """Base admin class for ContentPage objects."""

    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
    )
    list_filter = ("status",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "pub_date",
                    "description",
                    (
                        "image_preview_change_page",
                        "image",
                    ),
                    "status",
                )
            },
        ),
    )
    readonly_fields = ("image_preview_change_page",)
