from django.contrib import admin

from apps.core.models import Image, Settings
from apps.core.utilities.mixins import AdminImagePreview


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "settings_key",
        "field_type",
    )
    search_fields = ("field_type", "settings_key")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return "field_type", "settings_key"

    def get_fields(self, request, obj=None):
        field_for_setting_value = Settings.TYPES_AND_FIELDS[obj.field_type]
        return "field_type", "settings_key", field_for_setting_value


class ImageAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Image, ImageAdmin)
