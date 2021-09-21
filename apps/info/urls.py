from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import PartnersAPIView

router = DefaultRouter()
router.register(
    "partners",
    PartnersAPIView,
    basename="partners",
)


info_urls = [
    path("info/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
