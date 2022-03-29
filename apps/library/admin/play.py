from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import re_path

from apps.library.filters.play import PlayProgramFilter
from apps.library.models import Author, Play
from apps.library.models.play import ProgramType


class AuthorInline(admin.TabularInline):
    model = Author.plays.through
    min_num = 1
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
    )
    inlines = (AuthorInline,)
    list_filter = (
        PlayProgramFilter,
        "authors",
        "city",
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
        "program",
        "name",
        "city",
        "year",
        "url_download",
        "url_reading",
        "festival",
        "published",
        "link",
    )

    def get_urls(self):
        urls = super().get_urls()
        ajax = [
            re_path(r"\S*/ajax_play_program/", self.play_program),
        ]
        return ajax + urls

    def play_program(self, request, obj_id=None):
        program_id = request.GET.get("program")
        program = get_object_or_404(ProgramType, id=program_id)
        slug = program.slug
        print(slug)
        response = {"slug": slug}
        return JsonResponse(response)

    class Media:
        js = ("admin/play.js",)
