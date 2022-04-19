from django.contrib import admin
from django.db import models
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet

from apps.core.widgets import FkSelect
from apps.library.filters.play import PlayTypeFilter
from apps.library.models import AuthorPlay, Play


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
    model = AuthorPlay
    formset = AuthorRequiredInlineFormset
    extra = 0
    verbose_name = "Автор"
    verbose_name_plural = "Авторы"
    fields = ("author",)
    formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}


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
        PlayTypeFilter,
        "authors",
        "city",
        "festival",
        "program",
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
        "other_play",
        "name",
        "program",
        "city",
        "year",
        "url_download",
        "url_reading",
        "festival",
        "published",
    )
    formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}
