from django.contrib import admin

from apps.core.models import Image, Settings
from apps.core.utilities.mixins import AdminImagePreview


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


class ImageAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Image, ImageAdmin)
