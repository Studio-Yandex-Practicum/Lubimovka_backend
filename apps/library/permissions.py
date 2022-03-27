from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.core.models import Setting


class SettingsPlayReceptionPermission(BasePermission):
    def has_permission(self, request, view):
        if not Setting.get_setting("plays_reception_is_open"):
            raise PermissionDenied("Приём пьес закрыт.")
        return True


class AuthorWithoutQueryPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.query_params.get("letter"):
            raise PermissionDenied("Укажите параметр - letter.")
        return True
