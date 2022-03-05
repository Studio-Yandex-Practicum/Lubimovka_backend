from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.core.views import error400, error404, error500

DEBUG = settings.DEBUG
MEDIA_URL = settings.MEDIA_URL
MEDIA_ROOT = settings.MEDIA_ROOT

handler400 = error400
handler404 = error404
handler500 = error500

apps_patterns = [
    path("", include("apps.content_pages.urls")),
    path("", include("apps.afisha.urls")),
    path("", include("apps.articles.urls")),
    path("", include("apps.library.urls")),
    path("", include("apps.info.urls")),
    path("", include("apps.main.urls")),
]

api_schema_patterns = [
    path(
        route="",
        view=SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        route="redoc/",
        view=SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        route="swagger-ui/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns = [
    path(
        route="api/",
        view=include(apps_patterns),
    ),
    path(
        route="api/v1/schema/",
        view=include(api_schema_patterns),
    ),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += i18n_patterns(path("admin/", admin.site.urls), prefix_default_language=False)

if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
