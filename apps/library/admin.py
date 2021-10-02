from django.contrib import admin

from apps.library.models import (
    Achievement,
    Author,
    OtherLink,
    OtherPlay,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
    SocialNetworkLink,
)


class PlayAdmin(admin.ModelAdmin):
    pass


class PerformanceAdmin(admin.ModelAdmin):
    pass


class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "quote",
        "biography",
    )


class SocialNetworkLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "link",
    )


class OtherLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "link",
        "is_pinned",
        "order_number",
    )


class OtherPlayAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "link",
    )


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
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(SocialNetworkLink, SocialNetworkLinkAdmin)
admin.site.register(OtherLink, OtherLinkAdmin)
admin.site.register(OtherPlay, OtherPlayAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
