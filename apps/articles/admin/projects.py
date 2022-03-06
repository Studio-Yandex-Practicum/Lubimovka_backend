from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin


class ProjectContentInline(BaseContentInline):
    model = ProjectContent

    content_type_model = (
        "eventsblock",
        "imagesblock",
        "link",
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
                    # The pub_date field is disabled until the publication delay is implemented
                    # "pub_date",
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

    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
