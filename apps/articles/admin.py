from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.articles.models import Project
from apps.articles.models.project import ProjectContent
from apps.content_pages.admin import BaseContentInlineMixin


class ProjectContentInline(
    BaseContentInlineMixin,
    SortableInlineAdminMixin,
    admin.StackedInline,
):
    model = ProjectContent


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
    ]
    inlines = [ProjectContentInline]


admin.site.register(Project, ProjectAdmin)
