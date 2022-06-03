import datetime

from django.contrib import admin
from django.utils import formats

from apps.feedback.models import ParticipationApplicationFestival, Question


class LookBackDateListFilter(admin.SimpleListFilter):
    """Ретроспективный фильтр по датам."""

    title = "Дата создания"
    parameter_name = "created"

    def lookups(self, request, model_admin):
        return (
            ("today", "Сегодня"),
            ("seven_days", "Последние 7 дней"),
            ("this_month", "Этот месяц"),
            ("this_year", "Этот год"),
        )

    def queryset(self, request, queryset):
        today = datetime.datetime.now().date()
        date_ranges = {
            "today": today,
            "seven_days": today - datetime.timedelta(days=7),
            "this_month": today.replace(day=1),
            "this_year": today.replace(day=1, month=1),
        }
        since_date = date_ranges.get(self.value())
        if not since_date:
            return queryset
        return queryset.filter(created__gte=since_date)


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
        LookBackDateListFilter,
    )

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
