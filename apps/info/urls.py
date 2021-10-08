from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import QuestionCreate

router = DefaultRouter()
# router.register(
#     "partners",
#     PartnersAPIView,
#     basename="partners",
# )

info_urls = [
    # path("", include(router.urls)),
    path("questions/", QuestionCreate.as_view(), name="questions"),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
