import pytest

from apps.afisha import selectors

pytestmark = [pytest.mark.django_db]


def test_selector_afisha_festival_status_dict_len():
    """Get data returned by selector and check len. We expect len = 4."""
    selector_data = selectors.afisha_festival_status()
    assert len(selector_data) == 4, "Проверьте, что селектор возвращает только 4 ключа."


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
