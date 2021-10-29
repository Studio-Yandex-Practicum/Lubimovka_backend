from django.contrib import admin

from apps.articles.models import Project
from apps.articles.models.project import ProjectContent
from apps.content_pages.admin import BaseContentInline


class ProjectContentInline(BaseContentInline):
    model = ProjectContent

    content_type_model = (
        "video",
        "videosblock",
        "imagesblock",
        "performancesblock",
        "playsblock",
        "image",
        "personsblock",
        "link",
    )


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
