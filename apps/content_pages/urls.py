from django.urls import include, path

from apps.content_pages.views import GetContentTypeLink

content_type_urls = [
    path(
        route="content-pages/get-content-type-link/",
        view=GetContentTypeLink.as_view(),
        name="content-pages-models-links",
    ),
]

urlpatterns = [
    path("v1/", include(content_type_urls)),
]
