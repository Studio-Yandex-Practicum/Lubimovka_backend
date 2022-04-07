from datetime import datetime, timedelta

import django_filters
import pytz
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DateInFilter(django_filters.BaseInFilter, django_filters.DateFilter):
    pass


class AfishaEventsDateInFilter(django_filters.FilterSet):
    dates = DateInFilter(field_name="date_time", lookup_expr="date__in")


class StateOfEvent(admin.SimpleListFilter):
    title = _("Состояние события")

    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (
            ("all", _("Все")),
            (None, _("Предстоящие")),
            ("today", _("Сегодня")),
            ("past", _("Прошедшие")),
        )

    def queryset(self, request, queryset):
        date_now = datetime.today().replace(tzinfo=pytz.UTC).date()
        date_tomorrow = date_now + timedelta(days=1)
        if self.value() is None or self.value() == "upcoming":
            queryset = queryset.filter(date_time__gt=date_now).exclude(date_time__range=[date_now, date_tomorrow])
            return queryset
        if self.value() == "all":
            return queryset
        if self.value() == "past":
            queryset = queryset.filter(date_time__lt=date_now)
            return queryset
        if self.value() == "today":
            queryset = queryset.filter(date_time__range=[date_now, date_tomorrow])
            return queryset

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
