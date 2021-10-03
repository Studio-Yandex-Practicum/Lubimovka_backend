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


class SocialNetworkLinkInline(admin.TabularInline):
    model = SocialNetworkLink
    extra = 1


class OtherLinkInline(admin.TabularInline):
    model = OtherLink
    extra = 1


class OtherPlayInline(admin.StackedInline):
    model = OtherPlay
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "quote",
        "biography",
    )
    inlines = (
        SocialNetworkLinkInline,
        OtherLinkInline,
        OtherPlayInline,
    )
    exclude = (
        "social_network_links",
        "other_links",
        "other_plays_links",
    )
    empty_value_display = "-пусто-"


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
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)

admin.site.register(SocialNetworkLink)
admin.site.register(OtherPlay)
admin.site.register(OtherLink)
