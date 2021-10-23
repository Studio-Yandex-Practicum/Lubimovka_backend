from django.contrib import admin

from apps.main.models import InfoBlock, MainSettings, SettingsImageRelation


class BlockInline(admin.StackedInline):
    model = InfoBlock
    extra = 0


class SettingsImageRelationInline(admin.StackedInline):
    model = SettingsImageRelation
    extra = 0


class MainSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ("images_for_page",)
    list_display = (
        "type",
        "field_type",
        "settings_key",
    )
    list_filter = ("type",)
    search_fields = ("type", "field_type", "settings_key")
    inlines = [BlockInline, SettingsImageRelationInline]
    readonly_fields = ["type", "field_type", "settings_key"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return list()
        return self.readonly_fields

    def get_inlines(self, request, obj):
        if not obj:
            return list()
        else:
            saved_obj = MainSettings.objects.get(pk=obj.pk)
            if saved_obj.field_type != MainSettings.SettingFieldType.BLOCK:
                return list()
            else:
                return self.inlines

    def get_fields(self, request, obj=None):
        fields = ["type", "field_type", "settings_key"]
        if (
            obj is None
            or obj.field_type == MainSettings.SettingFieldType.BLOCK
        ):
            return fields
        return fields + MainSettings.SETTINGS_FIELDS[obj.field_type]


admin.site.register(MainSettings, MainSettingsAdmin)
