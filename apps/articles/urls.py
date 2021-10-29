from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import ProjectsViewSet

router = DefaultRouter()
router.register(
    "projects",
    ProjectsViewSet,
    basename="projects",
)


articles_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
