from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline


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


class NewsItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
    )
    inlines = (NewsItemContentInline,)


admin.site.register(NewsItem, NewsItemAdmin)
