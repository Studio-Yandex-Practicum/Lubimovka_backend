from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet

from apps.library.filters.play import PlayProgramFilter
from apps.library.forms.admin.play import PlayForm
from apps.library.models import AuthorPlays, Play


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
    model = AuthorPlays
    formset = AuthorRequiredInlineFormset
    extra = 1
    verbose_name = "Автор"
    verbose_name_plural = "Авторы"
    classes = ["collapse"]
    fields = ("author",)


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    form = PlayForm
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

    class Media:
        js = ("admin/play.js",)
