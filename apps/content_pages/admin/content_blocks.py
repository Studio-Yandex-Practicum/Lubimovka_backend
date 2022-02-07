from django.contrib import admin

from apps.core.mixins import HideOnNavPanelAdminModelMixin

from ..admin.content_block_items import ContentBlockItemInline, ContentImagesBlockItemInline
from ..models import (
    ContentPersonRole,
    ExtendedPerson,
    ImagesBlock,
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


class OrderedVideoInline(ContentBlockItemInline):
    model = OrderedVideo


class OrderedPerformanceInline(ContentBlockItemInline):
    model = OrderedPerformance


class OrderedPlayInline(ContentBlockItemInline):
    model = OrderedPlay


class ExtendedPersonInline(ContentBlockItemInline):
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
    inlines = (ContentImagesBlockItemInline,)


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
