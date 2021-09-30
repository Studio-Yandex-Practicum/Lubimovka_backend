from django.contrib import admin

from apps.library.models import (
    Author,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
)


class PlayAdmin(admin.ModelAdmin):
    pass


class PerformanceAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class PerformanceMediaReviewAdmin(admin.ModelAdmin):
    list_display = (
        "media_name",
        "performance",
        "pub_date",
    )

    list_filter = [
        "media_name",
        "performance__name",
        "pub_date",
    ]
    search_fields = [
        "media_name",
        "performance__name",
        "pub_date",
    ]


class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = [
        "reviewer_name",
        "performance",
        "pub_date",
    ]

    list_filter = [
        "reviewer_name",
        "performance__name",
        "pub_date",
    ]
    search_fields = [
        "reviewer_name",
        "performance__name",
        "pub_date",
    ]


admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
