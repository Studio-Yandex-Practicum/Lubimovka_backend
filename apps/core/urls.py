from django.urls import path

from apps.core.views import get_settings

urlpatterns = [
    path("v1/get_settings/", get_settings, name="get_settings"),
]
