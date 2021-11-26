from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsReadViewSet,
    ParticipationViewSet,
    PerformanceViewSet,
    PlayViewSet,
    SearchResultViewSet,
    filters,
)

router = DefaultRouter()
router.register(
    "performances",
    PerformanceViewSet,
    basename="performances",
)
router.register(
    "plays",
    PlayViewSet,
    basename="plays",
)
router.register(
    "search",
    SearchResultViewSet,
    basename="search",
)
router.register(
    "authors",
    AuthorsReadViewSet,
    basename="authors",
)
router.register(
    "participation",
    ParticipationViewSet,
    basename="participation",
)

library_urls = [
    path("library/filters/", filters, name="filters"),
    path("library/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
