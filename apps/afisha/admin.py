from django.contrib import admin

from apps.afisha.models import BaseEvent, Event


class BaseEventAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(BaseEvent, BaseEventAdmin)
