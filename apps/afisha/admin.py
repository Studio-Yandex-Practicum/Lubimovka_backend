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
