from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget

from apps.static_pages.models import StaticPagesModel


class StaticPagesModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }
    exclude = ("title", "static_page_url")

    def has_add_permission(self, request, obj=None):
        """Remove the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove the delete button."""
        return False


admin.site.register(StaticPagesModel, StaticPagesModelAdmin)
