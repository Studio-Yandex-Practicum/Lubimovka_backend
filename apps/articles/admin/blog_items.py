from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline
from apps.core.mixins import AdminImagePreview


class BlogPersonInline(admin.TabularInline):
    model = BlogItem.persons.through
    extra = 0


class BlogItemContentInline(BaseContentInline):
    model = BlogItemContent
    content_type_model = (
        "imagesblock",
        "personsblock",
        "playsblock",
        "preamble",
        "quote",
        "text",
        "title",
    )


class BlogItemAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "author_url_title",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)
    inlines = (
        BlogPersonInline,
        BlogItemContentInline,
    )


admin.site.register(BlogItem, BlogItemAdmin)
