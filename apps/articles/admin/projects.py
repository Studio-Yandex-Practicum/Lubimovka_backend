from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin


class ProjectContentInline(BaseContentInline):
    model = ProjectContent

    content_type_model = (
        "image",
        "imagesblock",
        "link",
        "performancesblock",
        "personsblock",
        "playsblock",
        "text",
        "videosblock",
    )

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
                    "is_draft",
                )
            },
        ),
    )


class ProjectAdmin(BaseContentPageAdmin):
    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
