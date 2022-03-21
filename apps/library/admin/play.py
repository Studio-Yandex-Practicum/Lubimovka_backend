from django.contrib import admin

from apps.library.filters.play import PlayTypeFilter
from apps.library.models import Author, Play


class AuthorInline(admin.TabularInline):
    model = Author.plays.through
    extra = 1
    verbose_name = "Автор"
    verbose_name_plural = "Авторы"
    classes = ["collapse"]


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("authors",)
    list_display = (
        "name",
        "city",
        "program",
        "festival",
        "published",
        "play_type",
    )
    inlines = (AuthorInline,)
    list_filter = (
        PlayTypeFilter,
        "authors",
        "city",
        "program",
        "festival",
        "published",
    )
    search_fields = (
        "authors__person__first_name",
        "authors__person__last_name",
        "name",
        "city",
        "program__name",
        "festival__year",
    )
    fields = (
        "name",
        "play_type",
        "city",
        "year",
        "url_download",
        "url_reading",
        "program",
        "festival",
        "published",
        "link",
    )

    class Media:
        js = ("admin/play.js",)
