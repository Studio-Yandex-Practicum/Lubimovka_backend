from django.contrib import admin

from apps.articles.models import (
    BlockText,
    BlockTitle,
    BlogItem,
    Content,
    NewsItem,
    Project,
)


class NewsItemAdmin(admin.ModelAdmin):
    pass


class BlogItemAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(BlockText)
class BlockTextAdmin(admin.ModelAdmin):
    list_display = ["text"]


@admin.register(BlockTitle)
class BlockTitleAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(BlogItem, BlogItemAdmin)
admin.site.register(Project, ProjectAdmin)
