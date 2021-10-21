from django.urls import path

from apps.main.views import main_get_settings

urlpatterns = [
    path("v1/main/", main_get_settings, name="main_get_settings"),
]
