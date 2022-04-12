from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin


class NewsItemContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = NewsItemContent

    content_type_model = (
        "imagesblock",
        "personsblock",
        "playsblock",
        "preamble",
        "quote",
        "text",
        "title",
    )
    classes = ["collapsible"]


class NewsItemAdmin(StatusButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
    )
    readonly_fields = (
        "status",
        "image_preview_change_page",
    )
    inlines = (NewsItemContentInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "title",
                    "pub_date",
                    "description",
                    (
                        "image_preview_change_page",
                        "image",
                    ),
                )
            },
        ),
    )
    other_readonly_fields = (
        "status",
        "title",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
    )


admin.site.register(NewsItem, NewsItemAdmin)
