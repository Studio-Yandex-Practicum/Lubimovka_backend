from django.contrib import admin

from apps.library.models import PerformanceReview


class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    search_fields = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)


admin.site.register(PerformanceReview, PerformanceReviewAdmin)
