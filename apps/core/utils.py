import logging
import urllib

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify
from rest_framework.response import Response

from apps.core.constants import ALPHABET, STATUS_INFO
from apps.core.decorators.cache import cache_user

logger = logging.getLogger("django")


def slugify(name):
    """Return "slug" formated string. It's an ordinary `django_slugify` with cyrillic support."""
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def get_picsum_image(width: int = 1024, height: int = 768) -> ContentFile:
    """Return real image from picsum.photos. Supports width and height arguments."""
    image = urllib.request.urlopen(f"https://picsum.photos/{width}/{height}").read()
    return ContentFile(image)


def get_paginated_response(pagination_class, serializer_class, queryset, request, view):
    """Return paginated response. Use it with `list` views based on APIView."""
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)
    context = {"request": request}

    if page is not None:
        serializer = serializer_class(page, context=context, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, context=context, many=True)
    return Response(data=serializer.data)


def get_object(admin_object, object_id):
    obj_class = admin_object.model
    obj = obj_class.objects.get(pk=object_id)
    return obj


def get_user_perms_level(request, obj):
    """Return user's access level for using in StatusButtonMixin."""
    app_name = obj._meta.app_label
    perms = request.user.get_all_permissions()
    if f"{app_name}.access_level_3" in perms:
        return 3
    if f"{app_name}.access_level_2" in perms:
        return 2
    if f"{app_name}.access_level_1" in perms:
        return 1
    return 0


def get_user_change_perms_for_status(request, obj):
    """Return user can change object."""
    if obj and hasattr(obj, "status"):
        user_level = get_user_perms_level(request, obj)
        right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
        if user_level < right_to_change:
            return False
    return True


def manual_order_app_list(app_dict, admin_site_apps_order):
    app_list = []
    apps = list(app_dict.values())
    for app_name in admin_site_apps_order:
        index = next((index for index, app in enumerate(apps) if app["name"] == app_name), None)
        if index is not None:
            app_list.append(apps.pop(index))

    app_list.extend(apps)
    return app_list


def manual_order_model_list(app, admin_site_models_order):
    app_name = app["name"]
    if app_name in admin_site_models_order:
        ordered_models = []
        models = app["models"]
        for model_name in admin_site_models_order[app_name]:
            index = next((index for index, model in enumerate(models) if model["name"] == model_name), None)
            if index is not None:
                ordered_models.append(models.pop(index))

        ordered_models.extend(models)
        return ordered_models

    app["models"].sort(key=lambda x: x["name"])
    return app["models"]


@cache_user(timelimit=300)
def get_app_list(self, request):
    admin_site_apps_order = getattr(settings, "ADMIN_SITE_APPS_ORDER", None)
    admin_site_models_order = getattr(settings, "ADMIN_SITE_MODELS_ORDER", None)

    app_dict = self._build_app_dict(request)

    if admin_site_apps_order:
        app_list = manual_order_app_list(app_dict, admin_site_apps_order)
    else:
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    for app in app_list:
        if admin_site_models_order:
            app["models"] = manual_order_model_list(app, admin_site_models_order)
        else:
            app["models"].sort(key=lambda x: x["name"])

    return app_list


def get_domain(request):
    server_protocol = request.META["SERVER_PROTOCOL"].split("/1.1")[0].lower()
    domain = server_protocol + "://" + request.META["HTTP_HOST"]
    return domain
