from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorLettersAPIView,
    AuthorsReadViewSet,
    ParticipationViewSet,
    PerformanceMediaReviewViewSet,
    PerformanceReviewViewSet,
    PerformanceViewSet,
    PlayFiltersAPIView,
    PlayViewSet,
    SearchResultViewSet,
)
from apps.library.views.performance import PreviewPerformanceViewSet

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

participation_url = [
    path(
        "participation/",
        ParticipationViewSet.as_view(),
        name="participation",
    ),
]
performance_urls = [
    path(
        route="performance/preview/<int:id>/<str:hash>/",
        view=PreviewPerformanceViewSet.as_view(),
        name="performance-item-detail-preview",
    ),
]

library_urls = [
    path("library/", include(router.urls)),
    path("library/", include(participation_url)),
    path("library/", include(performance_urls)),
    path(
        "library/author_letters/",
        AuthorLettersAPIView.as_view(),
        name="author_letters",
    ),
    path(
        "library/playfilters/",
        PlayFiltersAPIView.as_view(),
        name="playfilters",
    ),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
