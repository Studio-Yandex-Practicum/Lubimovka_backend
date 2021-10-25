from django.urls import path

from apps.core.views import get_setting

urlpatterns = [
    path("v1/setting/", get_setting, name="setting"),
]
