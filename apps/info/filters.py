from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, filters


class YearFestivalFilterSet(FilterSet):
    year = filters.NumberFilter(field_name="festival__year")


class HasReviewFilter(admin.SimpleListFilter):
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
