from django.urls import include, path

from apps.history.views import HistoryAPIView

history_urls = [
    path("history/", HistoryAPIView.as_view(), name="history_page"),
]

urlpatterns = [
    path("v1/", include(history_urls)),
]
