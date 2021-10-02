from django.contrib import admin

from apps.afisha.models import BaseEvent, Event


class BaseEventAdmin(admin.ModelAdmin):
    list_display = ("pk",)
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class EventAdmin(admin.ModelAdmin):
    list_display = ("pk", "base_event", "type", "date_time", "paid")
    list_filter = ("type",)
    empty_value_display = "-пусто-"


admin.site.register(Event, EventAdmin)
admin.site.register(BaseEvent, BaseEventAdmin)
