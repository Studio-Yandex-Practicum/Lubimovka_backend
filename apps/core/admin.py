from django.contrib import admin

from apps.core.mixins import AdminImagePreview
from apps.core.models import Image, Role, Settings


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

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit slug field."""
        if not request.user.is_superuser:
            return ("slug",)
        return super().get_readonly_fields(request, obj)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ("description", "settings_key", "value_field_type")
    search_fields = ("field_type", "settings_key")
    readonly_fields = ("field_type", "settings_key", "description")

    def get_fields(self, request, obj=None):
        field_for_setting_value = Settings.TYPES_AND_FIELDS[obj.field_type]
        return (
            "description",
            "settings_key",
            "field_type",
            field_for_setting_value,
        )

    def value_field_type(self, obj):
        """
        return value of the field type
        """
        return obj.value

    value_field_type.short_description = "Значение"

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


admin.site.register(Image, ImageAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Settings, SettingsAdmin)
