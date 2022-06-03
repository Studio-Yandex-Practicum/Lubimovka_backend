from django.contrib import admin
from django.utils import formats

from apps.feedback.models import ParticipationApplicationFestival, Question


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
        "created_datetime",
    )
    list_filter = (
        "exported_to_google",
        "saved_to_storage",
        "festival_year",
        "sent_to_email",
        "created",
    )

    readonly_fields = ("created",)
    search_fields = ("title", "first_name", "last_name", "city", "year")

    @admin.display(description="Создана")
    def created_datetime(self, obj):
        return formats.localize(obj.created)

    def has_add_permission(self, request):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_email", "question", "sent_to_email")
    list_filter = ("sent_to_email",)
    search_fields = ("author_name", "author_email", "question")
