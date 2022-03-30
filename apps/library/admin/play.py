from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import re_path

from apps.library.filters.play import PlayProgramFilter
from apps.library.models import Author, Play
from apps.library.models.play import ProgramType


class AuthorRequiredInlineFormset(BaseInlineFormSet):
    def clean(self):
        super(AuthorRequiredInlineFormset, self).clean()
        authors_count = 0
        deleting_count = 0
        for form in self.forms:
            if form.cleaned_data:
                authors_count += 1
                data = form.cleaned_data
                if data.get("DELETE"):
                    deleting_count += 1
        if deleting_count == authors_count or authors_count == 0:
            raise ValidationError("У пьесы должен быть автор")


class AuthorInline(admin.TabularInline):
    model = Author.plays.through
    formset = AuthorRequiredInlineFormset
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
        response = {"slug": slug}
        return JsonResponse(response)

    class Media:
        js = ("admin/play.js",)
