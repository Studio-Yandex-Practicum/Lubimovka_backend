from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.core.models import Setting


class SettingsPlayReceptionPermission(BasePermission):
    def has_permission(self, request, view):
        if not Setting.get_setting("plays_reception_is_open").boolean:
            raise PermissionDenied("Приём пьес закрыт.")
        return True
