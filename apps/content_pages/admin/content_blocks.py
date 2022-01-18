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
from apps.core.mixins import ModelAdminToHide


class ContentPersonRoleInline(admin.TabularInline):
    model = ContentPersonRole
    extra = 0


class OrderedInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0


class OrderedImageInline(OrderedInline):
    model = OrderedImage
    max_num = 8


class OrderedVideoInline(OrderedInline):
    model = OrderedVideo


class OrderedPerformanceInline(OrderedInline):
    model = OrderedPerformance


class OrderedPlayInline(OrderedInline):
    model = OrderedPlay


class ExtendedPersonInline(OrderedInline):
    model = ExtendedPerson
    show_change_link = True
    readonly_fields = ("person_roles",)


@admin.register(ExtendedPerson)
class ExtendedPersonAdmin(ModelAdminToHide):
    list_display = (
        "person",
        "block",
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


@admin.register(ImagesBlock)
class ImagesBlockAdmin(ModelAdminToHide):
    list_display = (
        "id",
        "title",
    )
    inlines = (OrderedImageInline,)


@admin.register(PersonsBlock)
class PersonsBlockAdmin(ModelAdminToHide):
    inlines = (ExtendedPersonInline,)


@admin.register(PerformancesBlock)
class PerformancesBlockAdmin(ModelAdminToHide):
    inlines = (OrderedPerformanceInline,)


@admin.register(PlaysBlock)
class PlaysBlockAdmin(ModelAdminToHide):
    inlines = (OrderedPlayInline,)


@admin.register(VideosBlock)
class VideosBlockAdmin(ModelAdminToHide):
    inlines = (OrderedVideoInline,)
