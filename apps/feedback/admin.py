from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils import formats

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

    def has_add_permission(self, _):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_email", "short_question_text", "sent_to_email", "created_display")
    list_filter = ("sent_to_email", LookBackDateListFilter)
    search_fields = ("author_name", "author_email", "question")
    readonly_fields = ("question", "author_name", "author_email", "sent_to_email", "created_display")

    @admin.display(
        description="Дата создания",
    )
    def created_display(self, obj):
        """Возвращает дату создания объекта."""
        return formats.date_format(obj.created, format="DATETIME_FORMAT", use_l10n=True)

    @admin.display(
        description="Текст вопроса",
    )
    def short_question_text(self, obj):
        """Возвращает текст вопроса, обрезанный до 70 знаков."""
        return truncatechars(obj.question, 70)

    def has_add_permission(self, _):
        return False
