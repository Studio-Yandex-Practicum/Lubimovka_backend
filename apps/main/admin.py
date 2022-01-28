from django.contrib import admin

from apps.core.models import Setting
from apps.main.models import Banner, SettingAfishaScreen, SettingEmail, SettingFirstScreen, SettingGeneral, SettingMain


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "url",
    )


@admin.register(SettingEmail, SettingGeneral, SettingMain, SettingFirstScreen, SettingAfishaScreen)
class SettingAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "settings_key",
        "get_value",
        "group",
        "image",
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj.settings_key in Setting.HELP_TEXT:
            field = Setting.TYPES_AND_FIELDS[obj.field_type]
            help_text = Setting.HELP_TEXT[obj.settings_key]
            form.base_fields[field].help_text = help_text
        return form

    def get_fields(self, request, obj=None):
        field_for_setting_value = Setting.TYPES_AND_FIELDS[obj.field_type]
        return (
            "description",
            "settings_key",
            "field_type",
            "group",
            field_for_setting_value,
        )

    @admin.display(description="Значение")
    def get_value(self, obj: object):
        """Return value of the setting object."""
        return obj.value

    def has_add_permission(self, request, obj=None):
        """Remove the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove the delete button."""
        return False
