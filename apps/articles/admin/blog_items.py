from django.contrib import admin
from apps.articles.mixins import CopyActionMixin

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
class BlogItemAdmin(CopyActionMixin, StatusButtonMixin, PreviewButtonMixin, BaseContentPageAdmin):
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
    actions = ("make_copy",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("creator")

    def has_change_permission(self, request, obj=None):
        if obj and obj.creator == request.user:
            return True
        return super().has_change_permission(request, obj=None)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.creator == request.user:
            return True
        return super().has_delete_permission(request, obj=None)
