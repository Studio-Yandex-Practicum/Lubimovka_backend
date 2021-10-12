from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from apps.articles.models import Project, ProjectContentPage
from apps.content_pages.admin import BaseContentInline


class ProjectContentInline(BaseContentInline):
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


class ProjectContentPageAdmin(admin.ModelAdmin):
    inlines = [ProjectContentInline]


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectContentPage, ProjectContentPageAdmin)
