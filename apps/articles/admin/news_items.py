from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin
from apps.core.utils import create_hash


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


class NewsItemAdmin(StatusButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
        "button_preview_page",
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

    @admin.display(
        description="Предпросмотр страницы",
    )
    def button_preview_page(self, obj):
        """Set a button to view the page."""
        preview_page_hash = create_hash(obj.id)
        preview_link = reverse(
            "news-item-detail-preview",
            kwargs={
                "pk": obj.id,
                "hash": preview_page_hash,
            },
        )
        label_button = "Предпросмотр"
        if obj.status and obj.status == "PUBLISHED":
            label_button = "Просмотр"
        return mark_safe(f'<a class="button" href={preview_link}>{label_button}</a>')


admin.site.register(NewsItem, NewsItemAdmin)
