from django.contrib import admin

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
        "short_common_event",
        "type",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    fields = ("common_event", "date_time", "paid", "url", "place", "pinned_on_main")
    list_filter = ("type",)
    empty_value_display = "-пусто-"

    def short_common_event(self, obj):
        return str(obj.common_event)[:25] + "..."

    short_common_event.short_description = "Событие"


admin.site.register(Event, EventAdmin)
