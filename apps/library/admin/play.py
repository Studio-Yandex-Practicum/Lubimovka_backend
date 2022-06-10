from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet

from apps.library.filters import PlayTypeFilter
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

    def get_search_fields(self, request):
        # if request is for autocomplete, search only in names
        if "autocomplete" in request.path:
            return ("name",)
        return super().get_search_fields(request)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # custom queryset for autocomplete requests
        if "autocomplete" in request.path and request.GET.get("field_name") == "play":
            # queryset with only main Plays for request autocomplete from reading, performance and
            # author's inline Plays
            if (
                request.GET.get("model_name") == "reading"
                or request.GET.get("model_name") == "performance"
                or (request.GET.get("model_name") == "authorplay" and request.GET.get("play_type") == "main")
            ):
                queryset = queryset.filter(published=True, other_play=False)
            # queryset with only Other Plays for request autocomplete from author's inline Other Plays
            elif request.GET.get("model_name") == "authorplay" and request.GET.get("play_type") == "other":
                queryset = queryset.filter(published=True, other_play=True)
        return queryset, use_distinct

    class Media:
        js = ("admin/play_admin.js",)
