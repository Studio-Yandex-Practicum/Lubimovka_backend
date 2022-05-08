import pytest

from apps.articles.factories import ProjectFactory


@pytest.fixture
def project_published():
    return ProjectFactory(id=100, status="PUBLISHED")
