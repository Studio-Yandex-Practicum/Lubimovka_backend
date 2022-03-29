from django.contrib import admin
from django.db import models
from django_select2 import forms as s2forms

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
    formfield_overrides = {
        models.ForeignKey: {
            "widget": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите событие",
                    "data-allow-clear": "true",
                }
            )
        }
    }


admin.site.register(Event, EventAdmin)
