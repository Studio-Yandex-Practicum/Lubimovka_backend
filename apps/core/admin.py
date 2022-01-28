from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

from apps.core.mixins import AdminImagePreview, AdminSlugFieldExcludeMixin
from apps.core.models import Image, Role, RoleType


@admin.register(Image)
class ImageAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = ("image_preview_list_page",)
    readonly_fields = ("image_preview_change_page",)


@admin.register(Role)
class RoleAdmin(AdminSlugFieldExcludeMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


@admin.register(RoleType)
class RoleTypeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        """Remove the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove the delete button."""
        return False

    def get_model_perms(self, request):
        """Return empty perms dict thus hiding the model from admin index."""
        return {}


admin.site.site_header = "Администрирование сайта"
