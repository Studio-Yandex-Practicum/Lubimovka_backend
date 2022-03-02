import pytest

from apps.afisha import selectors

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "field",
    (
        "festival_status",
        "afisha_description",
        "afisha_info_festival_text",
        "afisha_asterisk_text",
        "afisha_dates",
    ),
)
def test_selector_afisha_info_is_festival_dict_keys(field, is_festival_afisha, four_events_october):
    """Check required attributes in returned dict when `festival_status=True`."""
    selector_data = selectors.afisha_info_get()

    assert field in selector_data, f"Проверьте что атрибут `{field}` есть в ответе."
    assert len(selector_data) == 5, "Проверьте, что селектор возвращает только 5 ключей."


@pytest.mark.parametrize(
    "field",
    (
        "festival_status",
        "afisha_description",
        "afisha_dates",
    ),
)
def test_selector_afisha_info_is_not_festival_dict_keys(field, is_not_festival_afisha, four_events_october):
    """Check required attributes in returned dict when `festival_status=False`."""
    selector_data = selectors.afisha_info_get()

    assert field in selector_data, f"Проверьте что атрибут `{field}` есть в ответе."
    assert len(selector_data) == 3, "Проверьте, что селектор возвращает только 3 ключа."


def test_selector_afisha_info_expected_distinct_dates(four_events_october):
    """Compare dates returned by selector with expected. Dates should be distinct and sorted."""
    unique_event_dates = {event.date_time.date() for event in four_events_october}
    expected_sorted_dates = sorted(unique_event_dates)

    selector_data = selectors.afisha_info_get()
    returned_data_list = list(selector_data.get("afisha_dates"))

    assert returned_data_list == expected_sorted_dates, "Проверьте, что даты отфильтрованы и уникальны."


def test_selector_afisha_event_list_doesnt_return_events_in_past(freezer, four_events_october):
    """Compare the count of events with expected. One event has to disappear when date moves."""
    selector_events = selectors.afisha_event_list_get()
    assert selector_events.count() == 4, "Изначально ожидается 4 события."

    freezer.move_to("2021-10-06")
    selector_events = selectors.afisha_event_list_get()
    assert selector_events.count() == 3, "Одно событие должно оказаться в прошлом и пропасть в queryset"


@pytest.mark.parametrize(
    "comma_dates, expected_count",
    (
        ("2021-10-5", 1),
        ("2021-10-11", 2),
        ("2021-10-11,2021-10-05", 3),
    ),
)
def test_test_selector_afisha_event_list_date_filter(comma_dates, expected_count, four_events_october):
    """Compare events count in selector responce with expected count."""
    filter_dict = {"dates": comma_dates}
    filtered_events = selectors.afisha_event_list_get(filter_dict)

    assert filtered_events.count() == expected_count
