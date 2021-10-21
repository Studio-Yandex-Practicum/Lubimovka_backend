from django.contrib import admin
from django.core.exceptions import ValidationError

from apps.main.models import InfoBlock, MainSettings, SettingsImageRelation


class BlockInline(admin.StackedInline):
    model = InfoBlock
    extra = 0

    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise ValidationError("You must have at least one order")


class SettingsImageRelationInline(admin.StackedInline):
    model = SettingsImageRelation
    extra = 0


class MainSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ("images_for_page",)
    list_display = (
        "type",
        "settings_key",
        "boolean",
    )
    list_filter = ("type",)
    search_fields = ("type", "settings_key")
    inlines = [BlockInline, SettingsImageRelationInline]

    def get_inlines(self, request, obj):
        if not obj:
            return list()
        else:
            saved_obj = MainSettings.objects.get(pk=obj.pk)
            if saved_obj.settings_key not in [
                MainSettings.SettingsKey.WHAT_WE_DO_PAGE_INFO,
                MainSettings.SettingsKey.IDEOLOGY_PAGE_INFO,
                MainSettings.SettingsKey.HISTORY_PAGE_INFO,
            ]:
                return list()
            else:
                return self.inlines

    def get_fields(self, request, obj=None):
        fields = ["type", "settings_key"]
        if obj is None:
            return fields
        else:
            return fields + MainSettings.SETTINGS_FIELDS[obj.settings_key]


admin.site.register(MainSettings, MainSettingsAdmin)
