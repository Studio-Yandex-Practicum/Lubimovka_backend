from django.contrib import admin

from apps.afisha.models import CommonEvent, Event


class CommonEventAdmin(admin.ModelAdmin):
    list_display = ("pk", "target_model")
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        qs = qs.select_related(
            "common_event__masterclasses",
            "common_event__readings",
            # "common_event__performances"  # связь еще не создана
        )
        return qs

    list_display = ("pk", "common_event", "type", "date_time", "paid")
    list_filter = ("type",)
    empty_value_display = "-пусто-"


admin.site.register(Event, EventAdmin)
admin.site.register(CommonEvent, CommonEventAdmin)
