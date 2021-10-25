from django.contrib import admin

from apps.core.models import Image, Settings


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "field_type",
        "settings_key",
    )
    list_filter = ("type",)
    search_fields = ("type", "field_type", "settings_key")
    readonly_fields = ["type", "field_type", "settings_key"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return list()
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        return ["type", "field_type", "settings_key"] + [obj.field_type]


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Image)
