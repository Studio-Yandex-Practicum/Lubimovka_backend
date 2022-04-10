from django.contrib import admin
from django.db import models

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
        "type",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    fields = ("common_event", "date_time", "paid", "url", "place", "pinned_on_main")
    list_filter = ("type",)
    search_fields = ("common_event",)
    empty_value_display = "-пусто-"
    formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}


admin.site.register(Event, EventAdmin)
