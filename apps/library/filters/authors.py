import django_filters
from django.db.models import Q


def filter_by_name_predicate(queryset, name, value):
    return queryset.filter(Q(person__first_name__istartswith=value) | Q(person__last_name__istartswith=value))


class AuthorFilter(django_filters.FilterSet):
    """Фильтрует по начальным буквам в фамилии и имени."""

    letter = django_filters.CharFilter(method=filter_by_name_predicate)
