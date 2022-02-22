from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.models import Status


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
                )
            },
        ),
    )

    inlines = (ProjectContentInline,)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        project = Project.objects.get(pk=object_id)
        statuses = Status.objects.all().exclude(name=project.status.name)
        extra_context = {}
        extra_context["statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(Project, ProjectAdmin)
