from django.urls import path

from apps.core.views import MainView

app_name = "main"

urlpatterns = (path("main/", MainView.as_view()),)
