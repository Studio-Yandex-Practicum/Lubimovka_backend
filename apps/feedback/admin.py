from django.contrib import admin

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
    )
    list_filter = (
        "exported_to_google",
        "saved_to_storage",
        "festival_year",
        "sent_to_email",
    )
    search_fields = ("title", "first_name", "last_name", "city", "year")

    def has_add_permission(self, request):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_email", "question", "sent_to_email")
    list_filter = ("sent_to_email",)
    search_fields = ("author_name", "author_email", "question")
