from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.history.views import HistoryAPIView, HistoryQuestionsAPIView

router = DefaultRouter()
router.register(
    "questions",
    HistoryQuestionsAPIView,
    basename="history-questions",
)


history_urls = [
    path("history/", include(router.urls)),
    path("history/", HistoryAPIView.as_view(), name="history_page"),
]

urlpatterns = [
    path("v1/", include(history_urls)),
]
