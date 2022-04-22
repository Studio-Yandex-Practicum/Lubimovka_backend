from django.urls import include, path

from apps.feedback.views import QuestionCreateAPIView

feedback_urls = [
    path(
        "questions/",
        QuestionCreateAPIView.as_view(),
        name="questions",
    ),
]

app_prefix = [
    path(
        "feedback/",
        include(feedback_urls),
    )
]

urlpatterns = [
    path(
        "v1/",
        include(app_prefix),
    ),
]
