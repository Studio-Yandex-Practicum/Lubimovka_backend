from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db import models
from gfklookupwidget.widgets import GfkLookupWidget

from apps.content_pages.models import (
    Content,
    Image,
    ImagesBlock,
    Link,
    OrderedImage,
    OrderedPerformance,
    OrderedPerson,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PersonsBlock,
    PlaysBlock,
    Video,
    VideosBlock,
)
from apps.content_pages.models.content import ContentPage


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
    inlines = [OrderedImageInline]


class VideosBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedVideoInline]


class PerformancesBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPerformanceInline]


class PlaysBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPlayInline]


class PersonsBlockAdmin(admin.ModelAdmin):
    inlines = [OrderedPersonInline]


class BaseContentInline(SortableInlineAdminMixin, admin.StackedInline):
    formfield_overrides = {
        models.PositiveIntegerField: {
            "widget": GfkLookupWidget(
                content_type_field_name="content_type",
                parent_field=Content._meta.get_field("content_type"),
            )
        },
    }
    model = Content
    extra = 0


class BaseContentPageAdmin(admin.ModelAdmin):
    inlines = [BaseContentInline]


admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Link)
admin.site.register(ImagesBlock, ImagesBlockAdmin)
admin.site.register(VideosBlock, VideosBlockAdmin)
admin.site.register(PerformancesBlock, PerformancesBlockAdmin)
admin.site.register(PlaysBlock, PlaysBlockAdmin)
admin.site.register(PersonsBlock, PersonsBlockAdmin)
admin.site.register(ContentPage, BaseContentPageAdmin)
