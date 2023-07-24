import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


AFISHA_EVENTS_URL = reverse("afisha-event-list")


@pytest.mark.parametrize("paginator_field", ("count", "next", "previous", "results"))
def test_afisha_event_list_is_paginated(client, paginator_field, four_events_october):
    """Look for specific fields for paginated response."""
    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data

    assert paginator_field in response_data


def test_afisha_event_list_doesnt_return_events_in_past(client, freezer, four_events_october):
    """Get events in response, move date to the future and check that event in past wasn't returned."""
    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data
    assert response_data.get("count") == 4, "В октябре должно быть 4 события"

    freezer.move_to("2021-10-06")
    response = client.get(AFISHA_EVENTS_URL)
    response_data = response.data
    assert response_data.get("count") == 3, "Одно событие должно оказаться в прошлом и пропасть в ответе."


@pytest.mark.parametrize(
    "dates_query_param, expected_count",
    (
        ("2021-10-5", 1),
        ("2021-10-11", 2),
        ("2021-10-11,2021-10-05", 3),
    ),
)
def test_afisha_event_list_date_filter(client, dates_query_param, expected_count, four_events_october):
    """Compare events amount in responce with expected."""
    query_params = {"dates": dates_query_param}

    response = client.get(AFISHA_EVENTS_URL, query_params)
    response_data = response.data
    assert response_data.get("count") == expected_count


@pytest.mark.parametrize(
    "expected_field",
    (
        "id",
        "date_time",
        "action_url",
        "action_text",
        "type",
        "title",
        "description",
        "team",
        "location",
        "opening_date_time",
    ),
)
def test_afisha_event_list_results_level_expected_fields(client, expected_field, four_events_october):
    """Check all expected fields persists in `results`."""
    response_data = client.get(AFISHA_EVENTS_URL).data
    first_event = response_data.get("results")[0]

    assert expected_field in first_event
