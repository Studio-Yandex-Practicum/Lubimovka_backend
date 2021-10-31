from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsReadViewSet,
    ParticipationAPIView,
    PerformanceAPIView,
    PlayAPIView,
    SearchResultAPIViewSet,
)

router = DefaultRouter()
router.register(
    "performances",
    PerformanceAPIView,
    basename="performances",
)
router.register(
    "plays",
    PlayAPIView,
    basename="plays",
)
router.register(
    "search-result",
    SearchResultAPIViewSet,
    basename="search-result",
)
router.register(
    "authors",
    AuthorsReadViewSet,
    basename="authors",
)


paths = [
    path(
        "participation",
        ParticipationAPIView.as_view(),
        name="participation",
    ),
]

library_urls = [
    path("library/", include(router.urls)),
    path("library/", include(paths)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
