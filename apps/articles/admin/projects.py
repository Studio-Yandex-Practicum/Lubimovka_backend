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
        "video",
        "videosblock",
    )


class ProjectAdmin(BaseContentPageAdmin):
    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
