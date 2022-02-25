from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import StatusButtonMixin


class ProjectContentInline(BaseContentInline):
    model = ProjectContent

    content_type_model = (
        "imagesblock",
        "link",
        "performancesblock",
        "personsblock",
        "playsblock",
        "text",
        "videosblock",
    )


class ProjectAdmin(StatusButtonMixin, BaseContentPageAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "intro",
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

    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
