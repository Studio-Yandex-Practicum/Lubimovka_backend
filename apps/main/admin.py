from django.contrib import admin

from apps.main.models import InfoBlock, MainSettings, Text


class BlockInline(admin.StackedInline):
    model = InfoBlock


class TextAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "text_order",
    )


class MainSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ("texts_for_page", "images_for_page")
    list_display = (
        "name",
        "type",
        "text",
    )
    search_fields = ("type", "value_type", "name")
    inlines = [
        BlockInline,
    ]

    def get_inlines(self, request, obj):
        if not obj or obj.value_type != MainSettings.BLOCKS:
            return list()
        return self.inlines

    def get_fields(self, request, obj=None):
        fields = ["type", "value_type", "name"]
        if obj is None:
            return fields
        else:
            if obj.value_type == MainSettings.EMAIL:
                return fields + ["email"]
            elif obj.value_type == MainSettings.BOOL:
                return fields + ["boolean"]
            elif obj.value_type == MainSettings.TEXT:
                return fields + ["text"]
            elif obj.value_type == MainSettings.IMAGE:
                return fields + ["image"]
            elif obj.value_type == (
                MainSettings.TITLE_DESCRIPTION_IMAGES_AND_TEXTS
            ):
                return fields + [
                    "title",
                    "description",
                    "texts_for_page",
                    "images_for_page",
                ]
        return fields


admin.site.register(MainSettings, MainSettingsAdmin)
admin.site.register(Text, TextAdmin)
