from typing import Any, Union

from django.db.models import QuerySet
from django.utils import timezone

from apps.afisha.filters import AfishaEventsDateInFilter
from apps.afisha.models import Event
from apps.core.models import Setting


def afisha_info_get() -> dict[str, Union[str, Any]]:
    """Return festival status and Afisha's page header data.

    If `festival_status=False` only `festival_status` and `afisha_description`
    should be in response.
    """
    settings_keys = (
        "festival_status",
        "afisha_description",
        "afisha_info_festival_text",
        "afisha_asterisk_text",
    )
    afisha_festival_status_data = Setting.get_settings(settings_keys)

    festival_status = afisha_festival_status_data.get("festival_status")
    if not festival_status:
        afisha_festival_status_data.pop("afisha_info_festival_text")
        afisha_festival_status_data.pop("afisha_asterisk_text")

    return afisha_festival_status_data


def afisha_event_list_get(filters: dict[str, str] = None) -> QuerySet:
    """Return events filtered by date future events queryset."""
    filters = filters or {}
    afisha_events = (
        Event.objects.filter(date_time__gte=timezone.now())
        .select_related(
            "common_event__masterclass",
            "common_event__reading",
            "common_event__performance",
        )
        .order_by("date_time")
    )
    filtered_afisha_events = AfishaEventsDateInFilter(filters, afisha_events).qs
    return filtered_afisha_events
