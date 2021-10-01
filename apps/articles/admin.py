from django.contrib import admin

from apps.articles.models import BlogItem, NewsItem, Project


class NewsItemAdmin(admin.ModelAdmin):
    pass


class BlogItemAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(BlogItem, BlogItemAdmin)
admin.site.register(Project, ProjectAdmin)
