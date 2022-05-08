import django_filters
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.info.models import Partner


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
