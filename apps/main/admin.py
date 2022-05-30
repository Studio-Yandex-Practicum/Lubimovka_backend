from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.utils.html import format_html

from apps.core.models import Setting
from apps.main.models import (
    Banner,
    SettingAfishaScreen,
    SettingEmail,
    SettingFirstScreen,
    SettingGeneral,
    SettingMain,
    SettingPlaySupply,
)


@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "title",
        "description",
        "url",
    )
    list_display_links = ("title",)


@admin.register(SettingEmail, SettingGeneral, SettingMain, SettingFirstScreen, SettingAfishaScreen, SettingPlaySupply)
class SettingAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "get_value",
    )
    search_fields = ("field_type", "settings_key", "text")
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
            field_for_setting_value,
        )

    @admin.display(description="Значение")
    def get_value(self, obj: object):
        """Return value of the setting object."""
        if isinstance(obj.value, bool):
            return _boolean_icon(obj.value)
        if obj.field_type == "IMAGE":
            if not obj.value:
                return None
            return format_html('<a href="{}">{}</a>'.format(obj.image.url, obj.value))
        if obj.field_type == "URL":
            return format_html('<a href="{}">{}</a>'.format(obj.url, obj.value))
        return obj.value

    def has_add_permission(self, request, obj=None):
        """Remove the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove the delete button."""
        return False
