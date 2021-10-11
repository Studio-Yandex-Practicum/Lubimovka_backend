from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import QuestionCreateAPI

router = DefaultRouter()
# router.register(
#     "partners",
#     PartnersAPIView,
#     basename="partners",
# )

info_urls = [
    # path("", include(router.urls)),
    path("questions/", QuestionCreateAPI.as_view(), name="questions"),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
