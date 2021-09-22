from django.contrib import admin

from apps.library.models import (
    Author,
    MediaReviewPerformance,
    Performance,
    Play,
    PlayDraft,
    ReviewPerformance,
)


class PlayAdmin(admin.ModelAdmin):
    pass


class PlayDraftAdmin(admin.ModelAdmin):
    pass


class PerformanceAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class MediaReviewPerformanceAdmin(admin.ModelAdmin):
    pass


class ReviewPerformanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Play, PlayAdmin)
admin.site.register(PlayDraft, PlayDraftAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(MediaReviewPerformance, MediaReviewPerformanceAdmin)
admin.site.register(ReviewPerformance, ReviewPerformanceAdmin)
