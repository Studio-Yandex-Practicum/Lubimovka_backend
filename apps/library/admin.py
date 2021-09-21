from django.contrib import admin

from apps.library.models import (
    Author,
    DraftPlay,
    MediaReviewSpectacle,
    Play,
    Spectacle,
    WatcherReviewSpectacle,
)


class PlayAdmin(admin.ModelAdmin):
    pass


class DraftPlayAdmin(admin.ModelAdmin):
    pass


class SpectacleAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class MediaReviewSpectacleAdmin(admin.ModelAdmin):
    pass


class WatcherReviewSpectacleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Play, PlayAdmin)
admin.site.register(DraftPlay, DraftPlayAdmin)
admin.site.register(Spectacle, SpectacleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(MediaReviewSpectacle, MediaReviewSpectacleAdmin)
admin.site.register(WatcherReviewSpectacle, WatcherReviewSpectacleAdmin)
