from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import DeletePermissionsMixin, StatusButtonMixin


class NewsItemContentInline(BaseContentInline):
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


class NewsItemAdmin(StatusButtonMixin, DeletePermissionsMixin, BaseContentPageAdmin):
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
                    "title",
                    "pub_date",
                    "description",
                    (
                        "image_preview_change_page",
                        "image",
                    ),
                    "status",
                )
            },
        ),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions and not request.user.has_perm("articles.access_level_3"):
            del actions["delete_selected"]
        return actions


admin.site.register(NewsItem, NewsItemAdmin)
