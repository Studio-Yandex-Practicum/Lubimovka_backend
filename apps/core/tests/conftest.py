import pytest
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def client():
    return APIClient(format="json")
