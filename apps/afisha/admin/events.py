from datetime import datetime

from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse_lazy
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from apps.afisha.filters import StatusOfEvent
from apps.afisha.models import CommonEvent, Event
from apps.core.constants import Status
from apps.core.mixins import HideOnNavPanelAdminModelMixin


@admin.register(CommonEvent)
class CommonEventAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    search_fields = (
        "masterclass__name",
        "reading__name",
        "performance__name",
    )

    def get_urls(self):
        urls = super().get_urls()
        redirect_urls = [path("<path:object_id>/change/", self.redirect_to_base_event)]
        return redirect_urls + urls

    def redirect_to_base_event(self, request, object_id=None):
        commonevent = get_object_or_404(CommonEvent, id=object_id)
        event_type = type(commonevent.target_model)._meta.model_name
        if not event_type:
            raise Exception("Неподдерживаемый тип базового события!")
        event_id = getattr(commonevent, event_type).id
        url = reverse_lazy(f"admin:afisha_{event_type}_change", kwargs={"object_id": event_id})
        query_string = {"_to_field": "id", "_popup": "1"}
        return redirect(to=f"{url}?{urlencode(query_string)}")

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
        "is_archived",
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
                    ("is_archived", "paid"),
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

        if obj.date_time:
            if obj.is_archived:
                return icon("past", "Прошедшее")
            if obj.date_time.date() > date_now:
                return icon("upcoming", "Предстоящее")
            elif obj.date_time.date() < date_now:
                return icon("past", "Прошедшее")
            return icon("today", "Cегодняшнее")
        return icon("past", "Прошедшее")

    class Media:

        js = ("admin/afisha/js/AfishaGetEvent.js",)
