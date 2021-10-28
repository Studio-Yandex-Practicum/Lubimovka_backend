from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import ParticipationAPIView, PerformanceAPIView

router = DefaultRouter()
router.register(
    "performances",
    PerformanceAPIView,
    basename="performances",
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
