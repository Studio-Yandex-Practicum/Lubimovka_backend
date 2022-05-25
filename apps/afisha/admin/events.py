from datetime import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.afisha.filters import StatusOfEvent
from apps.afisha.models.events import CommonEvent, Event
from apps.core.constants import Status
from apps.core.mixins import HideOnNavPanelAdminModelMixin


@admin.register(CommonEvent)
class CommonEventAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    search_fields = (
        "masterclass__name",
        "reading__name",
        "performance__name",
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        event_type = request.GET.get("event_type").lower()
        if event_type:
            filter = f"{event_type}__name__isnull"
            queryset = queryset.filter(**{filter: False})
            if event_type == "performance":
                queryset = queryset.filter(performance__status=Status.PUBLISHED)
        return queryset, use_distinct


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "common_event",
        "status",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("type",),
            },
        ),
        (
            None,
            {
                "fields": ("common_event",),
                "classes": ("depended_on_common_event",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "date_time",
                    "paid",
                    "url",
                    "place",
                    "pinned_on_main",
                ),
            },
        ),
    )
    date_hierarchy = "date_time"
    list_filter = (
        StatusOfEvent,
        "type",
    )
    autocomplete_fields = ("common_event",)
    search_fields = (
        "common_event__reading__name",
        "common_event__masterclass__name",
        "common_event__performance__name",
    )
    empty_value_display = "-пусто-"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "common_event__masterclass",
            "common_event__reading",
            "common_event__performance",
        ).order_by("-date_time")
        return qs

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

    class Media:

        js = ("admin/afisha/js/AfishaGetEvent.js",)
