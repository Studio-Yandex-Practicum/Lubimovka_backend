from django.contrib import admin
from django.http import HttpResponseRedirect

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

    def response_change(self, request, obj):
        for status in obj.STATUS_INFO:
            if status in request.POST:
                obj.status = status
                obj.save()
                self.message_user(request, "Статус успешно обновлён!")
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Project, ProjectAdmin)
