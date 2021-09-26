from django.urls import path

from apps.main.views import MainApiView

urlpatterns = [
    path("v1/main/", MainApiView.as_view(), name="main_page"),
]
