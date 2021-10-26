from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import PerformanceAPIView

router = DefaultRouter()
router.register(
    "performances",
    PerformanceAPIView,
    basename="performances",
)

library_urls = [
    path("library/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
