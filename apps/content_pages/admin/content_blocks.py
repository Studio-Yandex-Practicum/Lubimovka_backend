from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.afisha.models import Event
from apps.content_pages.models import (
    ContentPersonRole,
    EventsBlock,
    ExtendedPerson,
    ImagesBlock,
    OrderedEvent,
    OrderedImage,
    OrderedPlay,
    OrderedVideo,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)
from apps.core.mixins import AdminImagePreview, HideOnNavPanelAdminModelMixin
from apps.library.models import Play


class ContentPersonRoleInline(admin.TabularInline):
    model = ContentPersonRole
    extra = 0


class OrderedInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0


class OrderedEventInline(OrderedInline):
    model = OrderedEvent
    max_num = 3

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Event.objects.filter(common_event__performance__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderedImageInline(AdminImagePreview, OrderedInline):
    readonly_fields = ("image_preview_change_page",)
    model = OrderedImage
    max_num = 8


class OrderedVideoInline(OrderedInline):
    model = OrderedVideo


class OrderedPlayInline(OrderedInline):
    model = OrderedPlay
    autocomplete_fields = ("item",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.filter(other_play=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExtendedPersonInline(OrderedInline):
    model = ExtendedPerson
    show_change_link = True
    readonly_fields = ("person_roles",)
    autocomplete_fields = ("person",)


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


@admin.register(EventsBlock)
class EventsBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    list_display = ("title",)
    inlines = (OrderedEventInline,)


@admin.register(PersonsBlock)
class PersonsBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (ExtendedPersonInline,)


@admin.register(PlaysBlock)
class PlaysBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedPlayInline,)


@admin.register(VideosBlock)
class VideosBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedVideoInline,)
