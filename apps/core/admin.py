from django.contrib import admin
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

from apps.core.mixins import AdminImagePreview
from apps.core.models import Image, Role, RoleType, Settings


class ImageAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)


class RoleAdmin(admin.ModelAdmin):
    list_dispay = (
        "name",
        "slug",
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit slug field."""
        if not request.user.is_superuser:
            return ("slug",)
        return super().get_readonly_fields(request, obj)


class RoleTypeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        """
        removes the save and add new button
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        removes the delete button
        """
        return False

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "settings_key",
        "get_value",
    )
    search_fields = (
        "field_type",
        "settings_key",
    )
    readonly_fields = (
        "field_type",
        "settings_key",
        "description",
    )

    def get_fields(self, request, obj=None):
        field_for_setting_value = Settings.TYPES_AND_FIELDS[obj.field_type]
        return (
            "description",
            "settings_key",
            "field_type",
            field_for_setting_value,
        )

    @admin.display(description="Значение")
    def get_value(self, obj: object):
        """Return value of the setting object."""
        return obj.value

    def has_add_permission(self, request, obj=None):
        """Removes the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Removes the delete button."""
        return False


admin.site.register(Image, ImageAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleType, RoleTypeAdmin)
admin.site.register(Settings, SettingsAdmin)
