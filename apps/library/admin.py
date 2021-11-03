from django.contrib import admin

from apps.library.forms import PerformanceAdminForm
from apps.library.models import (
    Achievement,
    Author,
    MasterClass,
    OtherLink,
    OtherPlay,
    ParticipationApplicationFestival,
    Performance,
    PerformanceMediaReview,
    PerformancePerson,
    PerformanceReview,
    Play,
    ProgramType,
    Reading,
    SocialNetworkLink,
)


class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("authors",)
    list_display = [
        "name",
        "city",
        "program",
        "festival",
        "is_draft",
    ]

    list_filter = [
        "authors",
        "city",
        "program",
        "festival",
        "is_draft",
    ]
    search_fields = [
        "authors_name",
        "name",
        "city",
        "program_name",
        "festival_year",
    ]


class AchievementAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "tag",
    ]


class AchievementInline(admin.TabularInline):
    model = Author.achievements.through
    extra = 1
    verbose_name = "Достижение"
    verbose_name_plural = "Достижения"


class PlayInline(admin.TabularInline):
    model = Author.plays.through
    extra = 1
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"


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
    list_display = [
        "id",
        "person",
        "quote",
        "biography",
    ]
    inlines = [
        AchievementInline,
        PlayInline,
        SocialNetworkLinkInline,
        OtherLinkInline,
        OtherPlayInline,
    ]
    exclude = [
        "achievements",
        "plays",
        "social_network_links",
        "other_links",
        "other_plays_links",
    ]
    empty_value_display = "-пусто-"


class PerformanceMediaReviewAdmin(admin.ModelAdmin):
    list_display = [
        "media_name",
        "performance",
        "pub_date",
    ]

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


class ReadingAdmin(admin.ModelAdmin):
    list_display = [
        "play",
        "name",
        "director",
        "dramatist",
    ]
    list_filter = [
        "director__last_name",
        "dramatist__last_name",
    ]
    search_fields = [
        "play__name",
        "name",
        "director__last_name",
        "dramatist__last_name",
    ]


class MasterClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "host",
    )
    list_filter = [
        "host__last_name",
    ]
    search_fields = [
        "play__name",
        "name",
        "host__last_name",
    ]


class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


class PerformanceReviewInline(admin.TabularInline):
    model = PerformanceReview
    extra = 1
    max_num = 8


class PerformanceMediaReviewInline(admin.TabularInline):
    model = PerformanceMediaReview
    extra = 1
    max_num = 8


class PerformanceTeamInline(admin.TabularInline):
    model = PerformancePerson
    extra = 1


class PerformanceAdmin(admin.ModelAdmin):
    filter_horizontal = [
        "images_in_block",
        "persons",
    ]
    list_filter = [
        "age_limit",
    ]
    search_fields = [
        "play__name",
        "name",
        "text",
    ]
    form = PerformanceAdminForm
    inlines = [
        PerformanceReviewInline,
        PerformanceMediaReviewInline,
        PerformanceTeamInline,
    ]


class ParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "verified",
        "title",
        "first_name",
        "last_name",
        "city",
        "year",
        "created",
        "file",
    )
    list_filter = [
        "year",
        "verified",
        "city",
    ]
    search_fields = [
        "title",
        "first_name",
        "last_name",
        "city",
        "year",
    ]


admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
admin.site.register(ParticipationApplicationFestival, ParticipationAdmin)

admin.site.register(SocialNetworkLink)
admin.site.register(OtherPlay)
admin.site.register(OtherLink)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(MasterClass, MasterClassAdmin)
admin.site.register(ProgramType, ProgramTypeAdmin)
