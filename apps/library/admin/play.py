from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet

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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if (
            "autocomplete" in request.path
            and request.GET.get("field_name") == "play"
            and (request.GET.get("model_name") == "reading" or request.GET.get("model_name") == "performance")
        ):
            queryset = queryset.filter(other_play=False)
        return queryset, use_distinct
