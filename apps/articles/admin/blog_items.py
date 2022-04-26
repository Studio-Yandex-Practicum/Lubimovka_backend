from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin
from apps.library.utilities import get_button_preview_page


class BlogPersonInline(InlineReadOnlyMixin, admin.TabularInline):
    model = BlogItem.roles.through
    extra = 0


class BlogItemContentInline(InlineReadOnlyMixin, BaseContentInline):
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


class BlogItemAdmin(StatusButtonMixin, BaseContentPageAdmin):
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
                    (
                        "author_url_title",
                        "author_url",
                    ),
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
        "author_url_title",
        "author_url",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
    )

    @admin.display(
        description="Предпросмотр страницы",
    )
    def button_preview_page(self, obj):
        return get_button_preview_page(obj)


admin.site.register(BlogItem, BlogItemAdmin)
