from django.contrib import admin

from apps.library.models import PerformanceMediaReview


class PerformanceMediaReviewAdmin(admin.ModelAdmin):
    list_display = (
        "media_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    search_fields = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)


admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
