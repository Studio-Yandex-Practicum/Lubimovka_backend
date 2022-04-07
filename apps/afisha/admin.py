from datetime import datetime

import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.afisha.filters import StateOfEvent
from apps.afisha.models import Event


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "common_event__masterclass",
            "common_event__reading",
            "common_event__performance",
        ).order_by("-date_time")
        return qs

    list_display = (
        "status",
        "short_common_event",
        "type",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    fields = ("common_event", "date_time", "paid", "url", "place", "pinned_on_main")
    list_filter = (
        StateOfEvent,
        "type",
    )
    empty_value_display = "-пусто-"

    def short_common_event(self, obj):
        return str(obj.common_event)[:25] + "..."

    short_common_event.short_description = "Событие"

    def status(self, obj):
        date_now = datetime.today().replace(tzinfo=pytz.UTC).date()
        if obj.date_time.date() > date_now:
            return mark_safe('<b style="background:{};color:{};">{}</b>'.format("#008000", "#F8F8FF", "Предстоящее"))
        elif obj.date_time.date() < date_now:
            return mark_safe('<b style="background:{};color:{};">{}</b>'.format("#B22222", "#F8F8FF", "Прошедшее"))
        return mark_safe('<b style="background:{};color:{};">{}</b>'.format("#1E90FF", "#F8F8FF", "Сегодня"))

    status.short_description = "Статус"


admin.site.register(Event, EventAdmin)
