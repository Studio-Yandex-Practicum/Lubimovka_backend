from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin


class BlogPersonInline(admin.TabularInline):
    model = BlogItem.roles.through
    extra = 0


class BlogItemContentInline(BaseContentInline):
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


class BlogItemAdmin(BaseContentPageAdmin):
    inlines = (
        BlogPersonInline,
        BlogItemContentInline,
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
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

    def change_view(self, request, object_id, form_url="", extra_context=None):
        blog = BlogItem.objects.get(pk=object_id)
        statuses = dict(blog.STATUS_INFO)
        statuses.pop(blog.status, None)
        if not blog.status == "PUBLISHED":
            statuses.pop("REMOVED_FROM_PUBLICATION", None)
        extra_context = {}
        extra_context["statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(BlogItem, BlogItemAdmin)
