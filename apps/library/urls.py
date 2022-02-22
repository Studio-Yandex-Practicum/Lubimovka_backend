from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsReadViewSet,
    ParticipationViewSet,
    PerformanceMediaReviewViewSet,
    PerformanceReviewViewSet,
    PerformanceViewSet,
    PlayFiltersAPIView,
    PlayViewSet,
    SearchResultViewSet,
)
from apps.library.views.play import play_status

router = DefaultRouter()
router.register(
    "performances",
    PerformanceViewSet,
    basename="performances",
)
router.register(
    r"performances/(?P<performance_id>\d+)/media-reviews",
    PerformanceMediaReviewViewSet,
    basename="performance-media-reviews",
)
router.register(
    r"performances/(?P<performance_id>\d+)/reviews",
    PerformanceReviewViewSet,
    basename="performance-reviews",
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
    path("library/", include(router.urls)),
    path(
        "library/playfilters/",
        PlayFiltersAPIView.as_view(),
        name="playfilters",
    ),
]

urlpatterns = [
    path("v1/", include(library_urls)),
    re_path(r"^play_status/(?P<object_pk>\d+)/(?P<status_pk>\d+)$", play_status, name="play_status"),
]
