from datetime import datetime

from django.contrib import admin
from django.http import JsonResponse
from django.urls import re_path
from django.utils.safestring import mark_safe

from apps.afisha.filters import StatusOfEvent
from apps.afisha.models import CommonEvent, Event
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
        common_event_type = request.GET.get("type_name").lower()
        if common_event_type:
            filter = common_event_type + "__" + "name" + "__" + "isnull"
            queryset = queryset.filter(**{filter: False})
        return queryset, use_distinct


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

    def get_urls(self):
        urls = super().get_urls()
        ajax_urls = [
            re_path(r"\S*/get-common-events-admin/", self.get_common_event),
        ]
        return ajax_urls + urls

    def get_common_event(self, request, obj_id=None):
        common_event_type = request.GET.get("type").lower()
        common_events = {}
        if common_event_type:
            common_events_queryset = getattr(CommonEvent, common_event_type).get_queryset().order_by("-created")
            common_events = {event.name: event.id for event in common_events_queryset}
        return JsonResponse(common_events)

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


admin.site.register(Event, EventAdmin)
