from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsAPIView,
    PerformanceMediaReviewsAPIView,
    PerformanceReviewsAPIView,
    PerformancesAPIView,
    PlaysAPIView,
)

router = DefaultRouter()
router.register(
    "plays",
    PlaysAPIView,
    basename="plays",
)
router.register(
    "performances",
    PerformancesAPIView,
    basename="performances",
)
router.register(
    "authors",
    AuthorsAPIView,
    basename="authors",
)
router.register(
    "media-reviews",
    PerformanceMediaReviewsAPIView,
    basename="media-reviews",
)
router.register(
    "reviews",
    PerformanceReviewsAPIView,
    basename="reviews",
)


library_urls = [
    path("library/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
