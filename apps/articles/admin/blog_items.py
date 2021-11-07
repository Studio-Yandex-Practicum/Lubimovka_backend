from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline


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


class BlogItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "author_url_title",
    )
    inlines = (BlogItemContentInline,)


admin.site.register(BlogItem, BlogItemAdmin)
