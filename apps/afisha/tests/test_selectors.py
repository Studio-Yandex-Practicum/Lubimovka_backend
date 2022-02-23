import pytest

from apps.afisha import selectors

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "field",
    (
        "festival_status",
        "description",
        "info_registration",
        "asterisk_text",
    ),
)
def test_selector_afisha_festival_status_dict_keys(field):
    """Check required attributes in dict returned by selector."""
    selector_data = selectors.afisha_festival_status()

    assert field in selector_data, f"Проверьте что атрибут `{field}` есть в ответе."
    assert len(selector_data) == 4, "Проверьте, что селектор возвращает только 4 ключа."
