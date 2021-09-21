from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorsAPIView,
    MediaReviewsSpectacleAPIView,
    PlaysAPIView,
    SpectaclesAPIView,
    WatcherReviewsSpectacleAPIView,
)

router = DefaultRouter()
router.register(
    "plays",
    PlaysAPIView,
    basename="plays",
)
router.register(
    "spectacles",
    SpectaclesAPIView,
    basename="spectacles",
)
router.register(
    "authors",
    AuthorsAPIView,
    basename="authors",
)
router.register(
    "media-reviews",
    MediaReviewsSpectacleAPIView,
    basename="media-reviews",
)
router.register(
    "watcher-reviews",
    WatcherReviewsSpectacleAPIView,
    basename="watcher-reviews",
)


library_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
