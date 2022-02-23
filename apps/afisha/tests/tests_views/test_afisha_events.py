from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.urls import reverse

from apps.afisha.factories import EventFactory

pytestmark = [pytest.mark.django_db]


AFISHA_EVENTS_URL = reverse("afisha-events")


@pytest.fixture
def four_events_october(masterclasses, readings, performances):
    event_1 = EventFactory(date_time=datetime(2021, 10, 5, 17, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    event_2 = EventFactory(date_time=datetime(2021, 10, 11, 18, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    event_3 = EventFactory(date_time=datetime(2021, 10, 11, 18, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    event_4 = EventFactory(date_time=datetime(2021, 10, 17, 23, 43, tzinfo=ZoneInfo("Europe/Moscow")))
    return event_1, event_2, event_3, event_4


@pytest.mark.parametrize("paginator_field", ("count", "next", "previous", "results"))
def test_afisha_events_is_paginated(client, paginator_field, random_events):
    """Look for specific fields for paginated response."""
    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data

    assert paginator_field in response_data


def test_afisha_events_doesnt_return_events_in_past(client, freezer, four_events_october):
    """Get events in response, move date to the future and check that event in past wasn't returned."""
    freezer.move_to("2021-09-01")

    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data
    assert response_data.get("count") == 4, "В октябре должно быть 4 события"

    freezer.move_to("2021-10-06")
    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data
    assert response_data.get("count") == 3, "Одно событие должно оказаться в прошлом и пропасть в ответе."


@pytest.mark.freeze_time("2021-09-01")
@pytest.mark.parametrize(
    "dates_query_param, expected_count",
    (
        ("2021-10-5", 1),
        ("2021-10-11", 2),
        ("2021-10-11,2021-10-05", 3),
    ),
)
def test_afisha_events_date_filter(client, freezer, dates_query_param, expected_count, four_events_october):
    """Compare events amount in responce with expected. Only one event has to be found."""
    query_params = {"dates": dates_query_param}

    response = client.get(AFISHA_EVENTS_URL, query_params)
    response_data = response.data
    assert response_data.get("count") == expected_count


@pytest.mark.freeze_time("2021-09-01")
@pytest.mark.parametrize("expected_field", ("id", "type", "event_body", "date_time", "paid", "url", "place"))
def test_afisha_events_results_level_expected_fields(client, expected_field, four_events_october):
    """Check all expected fields persists in `results`."""
    response_data = client.get(AFISHA_EVENTS_URL).data
    first_event = response_data.get("results")[0]

    assert expected_field in first_event
