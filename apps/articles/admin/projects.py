from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from apps.articles.models import Project, ProjectContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, PreviewButtonMixin, StatusButtonMixin


class ProjectContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = ProjectContent


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, StatusButtonMixin, PreviewButtonMixin, BaseContentPageAdmin):
    list_display = (
        "order",
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
        "creator_name",
    )
    list_display_links = ("title",)
    sortable_by = []
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
                    ("image_preview_change_page", "image"),
                    "creator_name",
                ),
            },
        ),
    )
    readonly_fields = (
        "status",
        "image_preview_change_page",
        "creator_name",
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
        "creator_name",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("creator")
