import pytest
from django.http import HttpRequest
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core.factories import ImageFactory
from apps.core.models import Image
from apps.core.serializers import ImageSerializer
from apps.core.utils import get_paginated_response

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def images():
    return ImageFactory.create_batch(5)


def test_get_paginated_response_absolute_url(images):
    """Get paginated response of images and check that media URL is absolute."""
    http_request = HttpRequest()
    request = Request(http_request)
    request._request._current_scheme_host = "http://lubimovka-test.ru"
    queryset = Image.objects.all()

    paginated_response = get_paginated_response(
        pagination_class=LimitOffsetPagination,
        serializer_class=ImageSerializer,
        queryset=queryset,
        request=request,
        view=APIView,
    )

    results = paginated_response.data.get("results")
    image_object_in_result = results[0]
    assert "http://lubimovka-test.ru" in image_object_in_result.get(
        "image"
    ), "Убедитесь, что для картинки отдается абсолютный url."
