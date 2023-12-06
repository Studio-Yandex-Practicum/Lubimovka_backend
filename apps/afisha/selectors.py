from datetime import timedelta
from typing import Any, Union

from django.conf import settings
from django.db.models import DateTimeField, ExpressionWrapper, F, Q, QuerySet
from django.db.models.functions import Now, TruncDay, TruncSecond
from django.utils import timezone

from apps.afisha.filters import AfishaEventsDateInFilter
from apps.afisha.models import Event
from apps.core.constants import Status
from apps.core.models import Setting


def afisha_info_get() -> dict[str, Union[str, Any]]:
    """Return festival status and Afisha's page header data.

    If `festival_status=False` only
    - `festival_status`
    - `afisha_description`
    - `afisha_dates`
    should be in response.
    """
    settings_keys = (
        "festival_status",
        "afisha_description",
        "afisha_info_festival_text",
        "afisha_asterisk_text",
    )
    afisha_info_data = Setting.get_settings(settings_keys)

    festival_status = afisha_info_data.get("festival_status")
    if not festival_status:
        afisha_info_data.pop("afisha_info_festival_text")
        afisha_info_data.pop("afisha_asterisk_text")

    afisha_dates = (
        Event.objects.filter(date_time__gte=timezone.now())
        .annotate(date=F("date_time__date"))
        .order_by("date")
        .values_list("date", flat=True)
        .distinct()
    )
    afisha_info_data["afisha_dates"] = afisha_dates
    return afisha_info_data


def afisha_event_list_get(filters: dict[str, str] = None) -> QuerySet:
    """Return events filtered by date future events queryset."""
    filters = filters or {}
    afisha_events = (
        Event.objects.filter(date_time__gte=timezone.now())
        .annotate(
            opening_date_time=ExpressionWrapper(
                TruncDay(
                    "date_time",
                )
                - timedelta(hours=settings.AFISHA_REGISTRATION_OPENS_HOURS_BEFORE),
                output_field=DateTimeField(),
            )
        )
        # TruncDay functions produces DateTime without timezone when wrapped with ExpressionWrapper;
        # to have Now without timezone as well, use TruncSecond here
        .annotate(now=ExpressionWrapper(TruncSecond(Now()), output_field=DateTimeField()))
        .select_related(
            "common_event__custom",
            "common_event__performance",
        )
        .filter(Q(common_event__custom__name__isnull=False) | Q(common_event__performance__status=Status.PUBLISHED))
        .order_by("date_time")
    )
    filtered_afisha_events = AfishaEventsDateInFilter(filters, afisha_events).qs
    return filtered_afisha_events
