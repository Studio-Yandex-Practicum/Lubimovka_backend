from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import QuestionCreateAPI

router = DefaultRouter()

info_urls = [
    path("questions/", QuestionCreateAPI.as_view(), name="questions"),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
