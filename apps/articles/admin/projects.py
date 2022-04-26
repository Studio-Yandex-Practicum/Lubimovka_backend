from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin
from apps.library.utilities import get_button_preview_page


class ProjectContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = ProjectContent

    content_type_model = (
        "contentunitrichtext",
        "eventsblock",
        "imagesblock",
        "link",
        "personsblock",
        "playsblock",
        "text",
        "videosblock",
    )


@admin.register(Project)
class ProjectAdmin(StatusButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
        "button_preview_page",
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

    @admin.display(
        description="Предпросмотр страницы",
    )
    def button_preview_page(self, obj):
        return get_button_preview_page(obj)
