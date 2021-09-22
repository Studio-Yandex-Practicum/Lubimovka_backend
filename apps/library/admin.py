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
    pass


class PerformanceReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
