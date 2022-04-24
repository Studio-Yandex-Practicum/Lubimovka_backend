from django.urls import include, path

from apps.feedback.views import ParticipationViewSet, QuestionCreateAPIView

feedback_urls = [
    path(
        "questions/",
        QuestionCreateAPIView.as_view(),
        name="questions",
    ),
]

participation_url = [
    path(
        "participation/",
        ParticipationViewSet.as_view(),
        name="participation",
    ),
]

app_prefix = [
    path(
        "feedback/",
        include(feedback_urls),
    ),
    path("feedback/", include(participation_url)),
]

urlpatterns = [
    path(
        "v1/",
        include(app_prefix),
    ),
]
