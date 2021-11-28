from django.urls import path

from apps.main.views import MainView

app_name = "main"

urlpatterns = (path("v1/main/", MainView.as_view()),)
