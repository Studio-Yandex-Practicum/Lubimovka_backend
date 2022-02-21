import pytest
from django.conf import settings
from rest_framework.test import APIClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return APIClient(format="json")


@pytest.fixture(autouse=True)
def set_media_temp_folder(tmpdir):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")
