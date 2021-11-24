from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.content_pages.models import (
    ImagesBlock,
    OrderedImage,
    OrderedPerformance,
    OrderedPerson,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)


class OrderedInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0


class OrderedImageInline(OrderedInline):
    model = OrderedImage


class OrderedVideoInline(OrderedInline):
    model = OrderedVideo


class OrderedPerformanceInline(OrderedInline):
    model = OrderedPerformance


class OrderedPlayInline(OrderedInline):
    model = OrderedPlay


class OrderedPersonInline(OrderedInline):
    model = OrderedPerson


class ImagesBlockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    inlines = [OrderedImageInline]


class VideosBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedVideoInline]


class PerformancesBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPerformanceInline]


class PlaysBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPlayInline]


class PersonsBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPersonInline]


admin.site.register(ImagesBlock, ImagesBlockAdmin)
admin.site.register(VideosBlock, VideosBlockAdmin)
admin.site.register(PerformancesBlock, PerformancesBlockAdmin)
admin.site.register(PlaysBlock, PlaysBlockAdmin)
admin.site.register(PersonsBlock, PersonsBlockAdmin)
