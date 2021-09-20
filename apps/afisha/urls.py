from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.afisha.views import AfishaAPIView

router = DefaultRouter()
router.register(
    "afisha",
    AfishaAPIView,
    basename="afisha",
)


afisha_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/afisha/", include(afisha_urls)),
]
