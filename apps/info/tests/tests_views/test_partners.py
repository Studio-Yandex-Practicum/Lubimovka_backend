import pytest
from django.urls import reverse
from rest_framework import status

from apps.info.factories import PartnerFactory

pytestmark = [pytest.mark.django_db]

PARTNERS_URL = reverse("partners")


@pytest.fixture
def in_footer_general_partner():
    return PartnerFactory(is_general=True, type="festival", in_footer_partner=True)


@pytest.fixture
def general_partner():
    return PartnerFactory(is_general=True, type="festival")


@pytest.fixture()
def info_partner():
    return PartnerFactory(type="info")


@pytest.fixture()
def festival_partner():
    return PartnerFactory(type="festival")


@pytest.fixture()
def partners(in_footer_general_partner, general_partner, info_partner, festival_partner):
    return in_footer_general_partner, general_partner, info_partner, festival_partner


def test_partner_list_count_in_response_matches_count_in_db(client, partners):
    """Checks that amount objects in response matches expected count."""
    response_data = client.get(PARTNERS_URL).data
    assert len(response_data) == 4


@pytest.mark.parametrize(
    "expected_attribute",
    ("id", "name", "type", "description", "url", "image"),
)
def test_partner_list_fields(client, general_partner, expected_attribute):
    """Check whether expected attribute found in returned object."""
    response_data = client.get(PARTNERS_URL).data
    partner_data = response_data[0]
    assert expected_attribute in partner_data


@pytest.mark.parametrize(
    "types_param, expected_count",
    (
        ("info", 1),
        ("festival", 3),
        ("info,festival", 4),
    ),
)
def test_partner_list_in_types_filter(client, types_param, expected_count, partners):
    """Compare amount of objects in response with expected when `types` filter applied."""
    query_params = {"types": types_param}

    response_data = client.get(PARTNERS_URL, query_params).data
    assert len(response_data) == expected_count


def test_partner_list_in_types_filter_incorrect_value(client, partners):
    """Pass incorrect value to `types` filter and check for the error."""
    query_params = {"types": "SOME_INCORRECT_VALUE"}

    response = client.get(PARTNERS_URL, query_params)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, "На недопустимое значение должны вернуть ошибку 400"
    assert "types" in response.data, "Проверьте, что в списке ошибок есть ключ `types`."
