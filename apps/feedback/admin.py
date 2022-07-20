from django.contrib import admin

from apps.feedback.filters import LookBackDateListFilter
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
        "created",
    )
    list_filter = (
        "exported_to_google",
        "saved_to_storage",
        "sent_to_email",
        "festival_year",
        LookBackDateListFilter,
    )

    readonly_fields = ("created",)
    search_fields = ("title", "first_name", "last_name", "city", "year")

    def has_add_permission(self, request):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_email", "question", "sent_to_email")
    list_filter = ("sent_to_email",)
    search_fields = ("author_name", "author_email", "question")

    def has_add_permission(self, request):
        return False
