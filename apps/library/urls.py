from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorLettersAPIView,
    AuthorsReadViewSet,
    PerformanceMediaReviewViewSet,
    PerformancePreviewDetailAPI,
    PerformanceReviewViewSet,
    PerformanceViewSet,
    PlayFiltersAPIView,
    PlayViewSet,
    SearchResultViewSet,
)

router = DefaultRouter()
router.register(
    "performances",
    PerformanceViewSet,
    basename="performance",
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
performance_item_urls = [
    path("", include(router.urls)),
    path(
        route="performances/<int:id>/preview/",
        view=PerformancePreviewDetailAPI.as_view(),
        name="performance-detail-preview",
    ),
]

library_urls = [
    path("library/", include(performance_item_urls)),
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
