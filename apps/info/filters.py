from django_filters import FilterSet, filters


class YearVolunteerFilterSet(FilterSet):
    year = filters.NumberFilter(field_name="festival__year")

    class Meta:
        fields = ("year",)
