from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline


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


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
