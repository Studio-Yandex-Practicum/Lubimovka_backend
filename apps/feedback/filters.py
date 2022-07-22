import datetime

from django.contrib import admin
from django.utils import timezone


class LookBackDateListFilter(admin.SimpleListFilter):
    """Ретроспективный фильтр по датам."""

    title = "Дата создания"
    parameter_name = "created_since"

    def lookups(self, request, model_admin):
        return (
            ("today", "Сегодня"),
            ("seven_days", "Последние 7 дней"),
            ("this_month", "Этот месяц"),
            ("this_year", "Этот год"),
        )

    def queryset(self, request, queryset):
        today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
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
