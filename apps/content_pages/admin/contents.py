from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.content_pages.models import AbstractContent
from apps.content_pages.widgets import GfkPopupWidget
from apps.core.mixins import AdminImagePreview


class BaseContentInline(SortableInlineAdminMixin, admin.TabularInline):
    """Extends StackedInline for a bit more convenient work in the admin panel.

    It do 3 things:
    1. Sets custom widget to GenericForeginKey field. It adds magnifier icon
    next to Generic Foreign Key and helps to choose item.
    2. Limit 'content_type' models to choose from in admin.
    3. Adds sortable abilities with 'SortableInlineAdminMixin'
    """

    extra = 0
    content_type_model = tuple()
    formfield_overrides = {
        models.PositiveIntegerField: {
            "widget": GfkPopupWidget(
                content_type_field_name="content_type",
                parent_field=AbstractContent._meta.get_field("content_type"),
            )
        },
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
    list_filter = ("is_draft",)
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
                    "is_draft",
                )
            },
        ),
    )
    readonly_fields = ("image_preview_change_page",)
