from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from apps.articles.models import OrderedProjectContent, Project, ProjectContent
from apps.content_pages.admin import BaseContentAdmin


class ProjectContentAdmin(BaseContentAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
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


class OrderedProjectContentInline(
    SortableInlineAdminMixin,
    admin.StackedInline,
):
    model = OrderedProjectContent
    extra = 0
    show_change_link = True


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]
    inlines = [OrderedProjectContentInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectContent, ProjectContentAdmin)
