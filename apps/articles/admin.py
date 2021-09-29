from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.articles.models import BlogItem, Content, Module, NewsItem, Project


class NewsItemAdmin(admin.ModelAdmin):
    pass


class BlogItemAdmin(admin.ModelAdmin):
    pass


class ContentInline(GenericTabularInline):
    model = Content


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [
        ContentInline,
    ]


class ModuleInline(admin.StackedInline):
    model = Module


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    inlines = [ModuleInline]


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(BlogItem, BlogItemAdmin)
admin.site.register(Project, ProjectAdmin)
