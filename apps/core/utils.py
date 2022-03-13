import urllib

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify
from rest_framework.response import Response

from apps.core.constants import ALPHABET


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
