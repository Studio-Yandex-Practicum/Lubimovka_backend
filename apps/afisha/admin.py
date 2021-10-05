from django.contrib import admin

from apps.afisha.models import BaseEvent, Event


class BaseEventAdmin(admin.ModelAdmin):
    list_display = ("pk", "target_model")
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        qs = qs.select_related(
            "base_event__masterclasses",
            "base_event__readings",
            # "base_event__performances"  # связь еще не создана
        )
        return qs

    list_display = ("pk", "base_event", "type", "date_time", "paid")
    list_filter = ("type",)
    empty_value_display = "-пусто-"


admin.site.register(Event, EventAdmin)
admin.site.register(BaseEvent, BaseEventAdmin)
