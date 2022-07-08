from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, PreviewButtonMixin, StatusButtonMixin


class BlogPersonInline(InlineReadOnlyMixin, admin.TabularInline):
    model = BlogItem.roles.through
    autocomplete_fields = ("person",)
    extra = 0


class BlogItemContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = BlogItemContent


@admin.register(BlogItem)
class BlogItemAdmin(StatusButtonMixin, PreviewButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
        "creator_name",
    )
    readonly_fields = (
        "status",
        "image_preview_change_page",
        "creator_name",
    )
    inlines = (
        BlogPersonInline,
        BlogItemContentInline,
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "title",
                    ("author_url_title", "author_url"),
                    "pub_date",
                    "description",
                    ("image_preview_change_page", "image"),
                    "creator_name",
                )
            },
        ),
    )
    other_readonly_fields = (
        "status",
        "title",
        "author_url_title",
        "author_url",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
        "creator_name",
    )
