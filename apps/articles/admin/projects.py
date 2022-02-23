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
                )
            },
        ),
    )

    inlines = (ProjectContentInline,)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        project = Project.objects.get(pk=object_id)
        statuses = dict(project.STATUS_INFO)
        statuses.pop(project.status, None)
        if not project.status == "PUBLISHED":
            statuses.pop("REMOVED_FROM_PUBLICATION", None)
        extra_context = {}
        extra_context["statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(Project, ProjectAdmin)
