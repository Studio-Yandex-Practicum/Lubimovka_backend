from django.contrib import admin

from apps.library.models import (
    Author,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
    EventHeader,
    Reading,
    MasterClass,
    Program,
)


class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("author",)
    list_display = [
        "name",
        "city",
        "program",
        "festival",
        "is_draft",
    ]

    list_filter = [
        "author",
        "city",
        "program",
        "festival",
        "is_draft",
    ]
    search_fields = [
        "author_name",
        "name",
        "city",
        "program_name",
        "festival_year"
    ]


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


class EventHeaderAdmin(admin.ModelAdmin):
    pass


class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "play",
        "name",
        "director",
        "dramatist",
    )
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
        "director",
        "dramatist",
        "leading",
    )
    list_filter = [
        "director__last_name",
        "dramatist__last_name",
        "leading__last_name",
    ]
    search_fields = [
        "play__name",
        "name",
        "director__last_name",
        "dramatist__last_name",
        "leading__last_name",
    ]


class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]


admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
admin.site.register(EventHeader, EventHeaderAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(MasterClass, MasterClassAdmin)
admin.site.register(Program, ProgramAdmin)