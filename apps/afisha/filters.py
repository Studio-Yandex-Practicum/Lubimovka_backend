import django_filters


class DateInFilter(django_filters.BaseInFilter, django_filters.DateFilter):
    pass


class AfishaEventsDateInFilter(django_filters.FilterSet):
    dates = DateInFilter(field_name="date_time", lookup_expr="date__in")
