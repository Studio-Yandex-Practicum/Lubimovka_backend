from django.contrib import admin

from apps.library.models import ParticipationApplicationFestival


@admin.register(ParticipationApplicationFestival)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "first_name",
        "last_name",
        "festival_year",
        "exported_to_google",
        "saved_to_storage",
        "sent_to_email",
    )
    list_filter = (
        "exported_to_google",
        "saved_to_storage",
        "festival_year",
        "sent_to_email",
    )
    search_fields = ("title", "first_name", "last_name", "city", "year")
