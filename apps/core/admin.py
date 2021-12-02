from django.contrib import admin

from apps.core.mixins import AdminImagePreview
from apps.core.models import (
    Image,
    Role,
    Settings,
    SettingsFirstScreen,
    SettingsGeneral,
    SettingsMail,
    SettingsMain,
)


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
    list_display = (
        "description",
        "settings_key",
        "get_value",
        "settings_group",
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
            "settings_group",
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


class SettingsMailAdmin(SettingsAdmin):
    def get_queryset(self, request):
        return SettingsMail.objects.filter(settings_group="MAIL").all()


class SettingsGeneralAdmin(SettingsAdmin):
    def get_queryset(self, request):
        return SettingsGeneral.objects.filter(settings_group="GENERAL").all()


class SettingsMainAdmin(SettingsAdmin):
    def get_queryset(self, request):
        return SettingsMain.objects.filter(settings_group="MAIN").all()


class SettingsFirstScreenAdmin(SettingsAdmin):
    def get_queryset(self, request):
        return SettingsFirstScreen.objects.filter(
            settings_group="FIRST_SCREEN"
        ).all()


admin.site.register(Image, ImageAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(SettingsMail, SettingsMailAdmin)
admin.site.register(SettingsGeneral, SettingsGeneralAdmin)
admin.site.register(SettingsMain, SettingsMainAdmin)
admin.site.register(SettingsFirstScreen, SettingsFirstScreenAdmin)
