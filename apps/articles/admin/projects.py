from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin


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


class ProjectAdmin(BaseContentPageAdmin):
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
                    "status",
                )
            },
        ),
    )

    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
