from django.urls import include, path

from apps.info.views import PlaceAPIView  # , QuestionsAPIView, PartnersAPIView

# from rest_framework.routers import DefaultRouter


#
# router = DefaultRouter()
# router.register(
#     "partners",
#     PartnersAPIView,
#     basename="partners",
# )
# router.register(
#     "questions",
#     QuestionsAPIView,
#     basename="questions",
# )

info_urls = [
    path("places/", PlaceAPIView.as_view(), name="places"),
]

urlpatterns = [
    path("v1/info/", include(info_urls)),
]
