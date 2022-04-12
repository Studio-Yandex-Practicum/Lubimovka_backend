from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from apps.library.models import Play
from apps.library.models.play import ProgramType


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class PlayFilter(filters.FilterSet):
    program = NumberInFilter(
        field_name="program__pk",
        label="Программа",
        lookup_expr="in",
    )
    festival = NumberInFilter(
        field_name="festival__year",
        label="Год фестиваля",
        lookup_expr="in",
    )
    published = filters.BooleanFilter(
        field_name="published",
        label="Отображать только опубликованные пьесы?",
    )

    class Meta:
        model = Play
        fields = (
            "program",
            "festival",
        )


class PlayProgramFilter(admin.SimpleListFilter):
    title = _("Программа")
    parameter_name = "program"

    def lookups(self, request, model_admin):
        programs_list = [
            (None, _("Все программы Любимовки")),  # default lookup which is used instead of 'All ('Все')
            ("all", _("Показать все пьесы")),  # add lookup to see all Lubimovka programs
        ]
        queryset = ProgramType.objects.all()
        for program_type in queryset:
            programs_list.append((str(program_type.id), program_type.name))  # all others possible lookups
        return programs_list

    def queryset(self, request, queryset):
        if self.value() is None:  # get qs for new default lookup
            return Play.objects.exclude(program__slug="other_plays")
        if self.value() != "all":
            return Play.objects.filter(program__id=self.value())

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": changelist.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }
