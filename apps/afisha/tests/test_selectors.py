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
    ),
)
def test_selector_afisha_info_is_festival_dict_keys(field, is_festival_afisha):
    """Check required attributes in returned dict when `festival_status=True`."""
    selector_data = selectors.afisha_info_get()

    assert field in selector_data, f"Проверьте что атрибут `{field}` есть в ответе."
    assert len(selector_data) == 4, "Проверьте, что селектор возвращает только 4 ключа."


@pytest.mark.parametrize(
    "field",
    (
        "festival_status",
        "afisha_description",
    ),
)
def test_selector_afisha_info_is_not_festival_dict_keys(field, is_not_festival_afisha):
    """Check required attributes in returned dict when `festival_status=False`."""
    selector_data = selectors.afisha_info_get()

    assert field in selector_data, f"Проверьте что атрибут `{field}` есть в ответе."
    assert len(selector_data) == 2, "Проверьте, что селектор возвращает только 2 ключа."
