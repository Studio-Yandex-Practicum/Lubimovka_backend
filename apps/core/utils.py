import logging
import urllib

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify
from rest_framework.response import Response

from apps.core.constants import ALPHABET, STATUS_INFO
from config.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


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


def get_app_list(self, request):
    admin_site_order = settings.ADMIN_SITE_ORDER
    app_dict = self._build_app_dict(request)

    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    for app in app_list:
        app_name = app["name"]
        if app_name in admin_site_order:
            ordered_models = []
            models = app["models"]
            for model_name in admin_site_order[app_name]:
                index = next((index for index, model in enumerate(models) if model["name"] == model_name), None)
                if index is not None:
                    ordered_models.append(models.pop(index))
                else:
                    logger.critical(
                        f"Ошибка в описании порядка моделей в админке. {model_name} не найдено в {app_name}"
                    )
            ordered_models.extend(models)
            app["models"] = ordered_models
            continue

        app["models"].sort(key=lambda x: x["name"])

    return app_list
