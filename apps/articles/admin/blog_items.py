from django.contrib import admin
from django.http import HttpResponseRedirect

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

    def response_change(self, request, obj):
        for status in obj.STATUS_INFO:
            if status in request.POST:
                obj.status = status
                obj.save()
                self.message_user(request, "Статус успешно обновлён!")
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(BlogItem, BlogItemAdmin)
