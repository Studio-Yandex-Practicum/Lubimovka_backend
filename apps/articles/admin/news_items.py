from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline
from apps.core.utilities.mixins import AdminImagePreview


class NewsItemContentInline(BaseContentInline):
    model = NewsItemContent

    content_type_model = (
        "imagesblock",
        "link",
        "personsblock",
        "playsblock",
        "quote",
        "text",
        "title",
    )


class NewsItemAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)
    inlines = (NewsItemContentInline,)


admin.site.register(NewsItem, NewsItemAdmin)
