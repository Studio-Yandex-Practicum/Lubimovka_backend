from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.content_pages.models import (
    ContentPersonRole,
    ExtendedPerson,
    ImagesBlock,
    OrderedImage,
    OrderedPerformance,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)


class ContentPersonRoleInline(admin.TabularInline):
    model = ContentPersonRole
    extra = 0


class ExtendedPersonAdmin(admin.ModelAdmin):
    list_display = (
        "block",
        "person",
    )
    list_filter = (
        ("block", admin.RelatedOnlyFieldListFilter),
        ("person", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        "block",
        "person",
    )
    inlines = (ContentPersonRoleInline,)


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


class ExtendedPersonInline(OrderedInline):
    model = ExtendedPerson


class ImagesBlockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    inlines = (OrderedImageInline,)


class PersonsBlockAdmin(admin.ModelAdmin):
    inlines = (ExtendedPersonInline,)


class PerformancesBlockAdmin(admin.ModelAdmin):
    inlines = (OrderedPerformanceInline,)


class PlaysBlockAdmin(admin.ModelAdmin):
    inlines = (OrderedPlayInline,)


class VideosBlockAdmin(admin.ModelAdmin):
    inlines = (OrderedVideoInline,)


admin.site.register(ExtendedPerson, ExtendedPersonAdmin)
admin.site.register(ImagesBlock, ImagesBlockAdmin)
admin.site.register(VideosBlock, VideosBlockAdmin)
admin.site.register(PerformancesBlock, PerformancesBlockAdmin)
admin.site.register(PlaysBlock, PlaysBlockAdmin)
admin.site.register(PersonsBlock, PersonsBlockAdmin)
