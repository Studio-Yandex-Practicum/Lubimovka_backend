from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline
from apps.core.mixins import AdminImagePreview


class BlogItemContentInline(BaseContentInline):
    model = BlogItemContent

    content_type_model = (
        "imagesblock",
        "link",
        "personsblock",
        "playsblock",
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

    inlines = (BlogItemContentInline,)


admin.site.register(BlogItem, BlogItemAdmin)
