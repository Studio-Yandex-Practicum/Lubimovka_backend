from django.contrib import admin

from apps.library.models import (
    Achievement,
    Author,
    LinkOther,
    LinkSocialNetwork,
    OtherPlay,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
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
    list_display = ("id", "person", "quote", "biography")


class LinkSocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "name", "link")


class LinkOtherAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "link",
        "anchored",
        "serial_number",
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
admin.site.register(LinkSocialNetwork, LinkSocialNetworkAdmin)
admin.site.register(LinkOther, LinkOtherAdmin)
admin.site.register(OtherPlay, OtherPlayAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
