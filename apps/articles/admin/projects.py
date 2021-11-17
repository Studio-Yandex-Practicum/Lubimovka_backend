from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline
from apps.core.utilities.mixins import AdminImagePreview


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


class ProjectAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)
    inlines = (ProjectContentInline,)


admin.site.register(Project, ProjectAdmin)
