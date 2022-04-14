from datetime import datetime

from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from apps.afisha.filters import StatusOfEvent
from apps.afisha.models import Event
from apps.core.widgets import FkSelect


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
        "common_event",
        "status",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    fields = ("common_event", "date_time", "paid", "url", "place", "pinned_on_main")
    date_hierarchy = "date_time"
    list_filter = (
        StatusOfEvent,
        "type",
    )
    search_fields = ("common_event",)
    empty_value_display = "-пусто-"
    formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}

    # @admin.display(
    #     description="Событие",
    # )
    # def short_common_event(self, obj):
    #     return str(obj.common_event)[:25] + "..."

    @admin.display(
        description="Состояние",
    )
    def status(self, obj):
        date_now = datetime.today().date()

        def icon(status, lable):
            return mark_safe(f"<img src='/static/admin/img/{status}.svg' title='{lable}'/>")

        if obj.date_time.date() > date_now:
            return icon("upcoming", "Предстоящее")
        elif obj.date_time.date() < date_now:
            return icon("past", "Прошедшее")
        return icon("today", "Cегодняшнее")


admin.site.register(Event, EventAdmin)
