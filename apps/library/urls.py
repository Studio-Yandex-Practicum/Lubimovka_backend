from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsAPIView,
    MediaReviewsPerformanceAPIView,
    PerformancesAPIView,
    PlaysAPIView,
    ReviewsPerformanceAPIView,
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
    MediaReviewsPerformanceAPIView,
    basename="media-reviews",
)
router.register(
    "reviews",
    ReviewsPerformanceAPIView,
    basename="reviews",
)


library_urls = [
    path("library/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
