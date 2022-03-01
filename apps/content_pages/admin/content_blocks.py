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
from apps.core.mixins import AdminImagePreview, HideOnNavPanelAdminModelMixin


class ContentPersonRoleInline(admin.TabularInline):
    model = ContentPersonRole
    extra = 0
    classes = ["collapse"]


class OrderedInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0
    classes = ["collapse"]


class OrderedImageInline(AdminImagePreview, OrderedInline):
    readonly_fields = ("image_preview_change_page",)
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
class ExtendedPersonAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
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
class ImagesBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    list_display = ("title",)
    inlines = (OrderedImageInline,)


@admin.register(PersonsBlock)
class PersonsBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (ExtendedPersonInline,)


@admin.register(PerformancesBlock)
class PerformancesBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedPerformanceInline,)


@admin.register(PlaysBlock)
class PlaysBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedPlayInline,)


@admin.register(VideosBlock)
class VideosBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedVideoInline,)
