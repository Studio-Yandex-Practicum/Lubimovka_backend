from django.contrib import admin

from apps.main.models import MainSettings


class MainSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "festival",
    )
    filter_horizontal = ("persons_how_get_questions",)
    empty_value_display = "-пусто-"

    def has_add_permission(self, request):
        if MainSettings.objects.first():
            return False
        return True


admin.site.register(MainSettings, MainSettingsAdmin)
