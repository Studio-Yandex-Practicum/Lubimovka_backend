from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.content_pages.models import (
    Content,
    ContentPage,
    Image,
    ImagesBlock,
    OrderedImage,
    Text,
)


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0


class GenericContentInline(GenericTabularInline):
    model = Content
    extra = 0


class ContentPageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "overview",
    ]
    inlines = [ContentInline]


class ItemAdmin(admin.ModelAdmin):
    inlines = [GenericContentInline]


class OrderedImageInline(admin.TabularInline):
    model = OrderedImage
    min_num = 1
    extra = 0


class ImagesBlockAdmin(admin.ModelAdmin):
    inlines = [GenericContentInline, OrderedImageInline]


admin.site.register(ContentPage, ContentPageAdmin)
admin.site.register(Text, ItemAdmin)
admin.site.register(Image, ItemAdmin)
admin.site.register(ImagesBlock, ImagesBlockAdmin)
