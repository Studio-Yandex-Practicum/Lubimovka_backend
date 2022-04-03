from django.contrib import admin
from django.http import JsonResponse
from django.urls import re_path

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

    def get_urls(self):
        urls = super().get_urls()
        ajax_urls = [
            re_path(r"\S*/get-common-events-admin/", self.get_common_event),
        ]
        return ajax_urls + urls

    def get_common_event(self, request, obj_id=None):
        common_event_type = request.GET.get("type")
        common_events = {}
        if common_event_type:
            common_events_queryset = Event.objects.filter(type=common_event_type)
            common_events = {
                event.common_event.target_model.name: event.common_event.target_model.id
                for event in common_events_queryset
            }
        return JsonResponse(common_events)

    list_display = (
        "common_event",
        "type",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    list_filter = ("type",)
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
    empty_value_display = "-пусто-"

    class Media:

        js = ("admin/afisha/js/AfishaGetEvent.js",)


admin.site.register(Event, EventAdmin)
