from django.contrib import admin

from apps.articles.models import ArticleBlog, NewsItem, Project


class NewsItemAdmin(admin.ModelAdmin):
    pass


class ArticleBlogAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(ArticleBlog, ArticleBlogAdmin)
admin.site.register(Project, ProjectAdmin)
