import urllib
from functools import wraps

from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify as django_slugify
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst
from rest_framework import status
from rest_framework.response import Response

from apps.core.constants import ALPHABET, STATUS_INFO


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


def cache_user(func):
    cache_user_dict = dict()

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user.username
        if user in cache_user_dict:
            return cache_user_dict[user]

        result = func(self, request, *args, **kwargs)
        cache_user_dict[user] = result
        return result

    return wrapper


def _custom_build_app_dict(self, request, fictitious_apps=None, label=None):
    """Build the app dictionary. The optional `label` parameter filters models of a specific app."""
    app_dict = {}

    if label:
        models = {m: m_a for m, m_a in self._registry.items() if m._meta.app_label == label}
    else:
        models = self._registry

    for model, model_admin in models.items():
        fictitious = False
        if model._meta.model_name in fictitious_apps:
            fictitious = True
            app_label = fictitious_apps[model._meta.model_name]["app_label"]
        else:
            app_label = model._meta.app_label

        has_module_perms = model_admin.has_module_permission(request)
        if not has_module_perms:
            continue

        perms = model_admin.get_model_perms(request)

        # Check whether user has any perm for this module.
        # If so, add the module to the model_list.
        if True not in perms.values():
            continue

        info = (app_label, model._meta.model_name)
        model_dict = {
            "name": capfirst(model._meta.verbose_name_plural),
            "object_name": model._meta.object_name,
            "perms": perms,
        }
        if perms.get("change"):
            try:
                model_dict["admin_url"] = reverse("admin:%s_%s_changelist" % info, current_app=self.name)
            except NoReverseMatch:
                pass
        if perms.get("add"):
            try:
                model_dict["add_url"] = reverse("admin:%s_%s_add" % info, current_app=self.name)
            except NoReverseMatch:
                pass

        if app_label in app_dict:
            app_dict[app_label]["models"].append(model_dict)
        else:
            if fictitious:
                app_dict[app_label] = {
                    "name": fictitious_apps[model._meta.model_name]["verbose_name"],
                    "app_label": app_label,
                    "app_url": f"/admin/{app_label}/",
                }
            else:
                app_dict[app_label] = {
                    "name": apps.get_app_config(app_label).verbose_name,
                    "app_label": app_label,
                    "app_url": reverse(
                        "admin:app_list",
                        kwargs={"app_label": app_label},
                        current_app=self.name,
                    ),
                }
            app_dict[app_label].update(
                {
                    "has_module_perms": has_module_perms,
                    "models": [model_dict],
                }
            )

    if label:
        return app_dict.get(label)
    return app_dict


@cache_user
def get_app_list(self, request):
    admin_site_apps_order = getattr(settings, "ADMIN_SITE_APPS_ORDER", None)
    admin_site_models_order = getattr(settings, "ADMIN_SITE_MODELS_ORDER", None)
    fictitious_apps = {
        "participationapplicationfestival": {"app_label": "feedback", "verbose_name": "Фидбек"},
        "question": {"app_label": "feedback", "verbose_name": "Фидбек"},
    }

    app_dict = _custom_build_app_dict(self, request, fictitious_apps)

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


def send_email(message):
    message.send()
    if hasattr(message, "anymail_status") and message.anymail_status.esp_response.status_code == status.HTTP_200_OK:
        return True
    return False
