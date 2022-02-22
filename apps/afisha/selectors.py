from typing import Union

from django.db.models import QuerySet
from django.utils import timezone

from apps.afisha.filters import AfishaEventsDateInFilter
from apps.afisha.models import Event
from apps.core.models import Setting


def afisha_festival_status() -> dict[str, Union[str, bool]]:
    """Return festival status and Afisha's page header data."""
    festival_status = Setting.get_setting("festival_status")
    description = Setting.get_setting("afisha_description")
    info_registration = Setting.get_setting("afisha_info_festival_text")
    asterisk_text = Setting.get_setting("afisha_asterisk_text")
    afisha_festival_status_data = {
        "festival_status": festival_status,
        "description": description,
        "info_registration": info_registration,
        "asterisk_text": asterisk_text,
    }
    return afisha_festival_status_data


def afisha_events_get(filters: dict[str, str] = None) -> QuerySet:
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
