from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from gfklookupwidget.widgets import GfkLookupWidget

from apps.content_pages.models import AbstractContent


class BaseContentInline(SortableInlineAdminMixin, admin.StackedInline):
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
            "widget": GfkLookupWidget(
                content_type_field_name="content_type",
                parent_field=AbstractContent._meta.get_field("content_type"),
            )
        },
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Limits avaliable models to choose while creating ContentPage object.
        """

        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(
                model__in=self.content_type_model,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
