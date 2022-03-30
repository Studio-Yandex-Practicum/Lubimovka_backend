from django.contrib import admin

from apps.library.models import ParticipationApplicationFestival


@admin.register(ParticipationApplicationFestival)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "first_name",
        "last_name",
        "exported_to_google",
        "saved_to_storage",
    )
    list_filter = (
        "exported_to_google",
        "saved_to_storage",
    )
    search_fields = (
        "title",
        "first_name",
        "last_name",
        "city",
        "year",
    )
