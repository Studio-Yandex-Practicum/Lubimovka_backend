from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import PartnersAPIView, QuestionsAPIView

router = DefaultRouter()
router.register(
    "partners",
    PartnersAPIView,
    basename="partners",
)
router.register(
    "questions",
    QuestionsAPIView,
    basename="questions",
)


info_urls = [
    path("info/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
