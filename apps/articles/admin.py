from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from apps.articles.models import Project
from apps.articles.models.project import ProjectContent
from apps.content_pages.admin import BaseContentInlineMixin


class ProjectContentInline(
    BaseContentInlineMixin,
    SortableInlineAdminMixin,
    admin.StackedInline,
):
    model = ProjectContent

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Could be a service or some type of mixin.
        Limits avaliable models to choose while creating ContentPage object.
        """

        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(
                app_label="content_pages",
                model__in=(
                    "video",
                    "videosblock",
                    "imagesblock",
                    "performancesblock",
                    "playsblock",
                    "personsblock",
                    "link",
                ),
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
    ]
    inlines = [ProjectContentInline]


admin.site.register(Project, ProjectAdmin)
