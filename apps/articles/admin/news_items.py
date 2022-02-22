from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.models import Status


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


class NewsItemAdmin(BaseContentPageAdmin):
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
                )
            },
        ),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        news = NewsItem.objects.get(pk=object_id)
        exclude_names = [news.status.name]
        if not news.status.name == "Опубликовано":
            exclude_names.append("Снято с публикации")
        statuses = Status.objects.all().exclude(name__in=exclude_names)
        extra_context = {}
        extra_context["statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(NewsItem, NewsItemAdmin)
