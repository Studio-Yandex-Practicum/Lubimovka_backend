from rest_framework.permissions import BasePermission

from apps.core.models import Setting


class SettingsPermission(BasePermission):
    message = "Приём пьес закрыт."

    def has_permission(self, request, view):
        return Setting.objects.get(settings_key="plays_reception_is_open").boolean
