import django_filters
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.info.models import Festival, Partner


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class YearFestivalFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="festival__year")


class PartnerFilterSet(django_filters.FilterSet):
    types = CharInFilter(field_name="type", lookup_expr="in")

    class Meta:
        model = Partner
        fields = (
            "types",
            "in_footer_partner",
        )


class HasReviewAdminFilter(admin.SimpleListFilter):
    title = _("Есть отзыв?")
    parameter_name = "volunteer"

    def lookups(self, request, model_admin):
        return (
            ("True", _("Да")),
            ("False", _("Нет")),
        )

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(~Q(review_text__exact=""))
        if self.value() == "False":
            return queryset.filter(review_text__exact="")


class PartnerTypeFilter(admin.SimpleListFilter):
    title = _("Тип партнера")
    parameter_name = "type"

    def lookups(self, request, model_admin):
        partner_types_list = [
            (None, _("Партнер фестиваля")),  # default lookup which is used instead of 'All' ('Все')
            (Partner.PartnerType.GENERAL_PARTNER, _("Генеральный партнер")),
            (Partner.PartnerType.INFO_PARTNER, _("Информационный партнер")),
        ]
        return partner_types_list

    def queryset(self, request, queryset):
        if self.value() is None:  # get qs for new default lookup
            return Partner.objects.filter(type=Partner.PartnerType.FESTIVAL_PARTNER)
        if self.value() == Partner.PartnerType.GENERAL_PARTNER:
            return Partner.objects.filter(type=Partner.PartnerType.GENERAL_PARTNER)
        if self.value() == Partner.PartnerType.INFO_PARTNER:
            return Partner.objects.filter(type=Partner.PartnerType.INFO_PARTNER)

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


class FestivalYearFilter(admin.SimpleListFilter):
    title = "Год фестиваля"
    parameter_name = "festival__year"

    def lookups(self, request, model_admin):
        list_of_years = []
        years = Festival.objects.order_by("-year").values_list("year", flat=True)
        for year in years:
            if len(list_of_years) == 0:
                list_of_years.append((None, f"Фестиваль {year} года"))
            else:
                list_of_years.append((str(year), f"Фестиваль {year} года"))
        return list_of_years

    def queryset(self, request, queryset):
        latest_festival_year = Festival.objects.latest("year").year
        if self.value():
            return queryset.filter(festival__year=self.value())
        else:
            return queryset.filter(festival__year=latest_festival_year)

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
