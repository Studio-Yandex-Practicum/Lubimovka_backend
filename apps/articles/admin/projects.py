from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import DeletePermissionsMixin, InlineReadOnlyMixin, StatusButtonMixin


class ProjectContentInline(InlineReadOnlyMixin, BaseContentInline):
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


class ProjectAdmin(StatusButtonMixin, DeletePermissionsMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
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
    readonly_fields = (
        "status",
        "image_preview_change_page",
    )
    inlines = (ProjectContentInline,)
    other_readonly_fields = (
        "status",
        "title",
        "intro",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
    )


admin.site.register(Project, ProjectAdmin)
