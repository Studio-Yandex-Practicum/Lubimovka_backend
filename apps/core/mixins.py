from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.core.constants import STATUS_INFO
from apps.core.utils import get_object, get_user_perms_level


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom."""

    def has_change_permission(self, request, obj=None):
        if obj:
            user_level = get_user_perms_level(request, obj)
            right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
            if user_level < right_to_change:
                return False
        return True

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = get_object(self, object_id)
        extra_context = {}
        if self.has_change_permission(request, obj):
            extra_context["user_level"] = get_user_perms_level(request, obj)
            extra_context["current_status_level"] = STATUS_INFO[obj.status]["min_access_level"]
            possible_changes = STATUS_INFO[obj.status]["possible_changes"]
            statuses = {}
            for status in possible_changes:
                statuses[status] = STATUS_INFO[status]
            extra_context["possible_statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        for status in STATUS_INFO:
            if status in request.POST:
                obj.status = status
                obj.save()
                self.message_user(request, "Статус успешно обновлён!")
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class DeletePermissionsMixin:
    """Mixin hides button Delete.

    Button Delete removed from change_view page if
    user doesn't have perm to delete in object's status.
    """

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = get_object(self, object_id)
        user_level = get_user_perms_level(request, obj)
        right_to_delete = STATUS_INFO[obj.status]["min_level_to_delete"]
        if user_level < right_to_delete:
            extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)

    def get_actions(self, request):
        app_name = self.model._meta.app_label
        actions = super().get_actions(request)
        if "delete_selected" in actions and not request.user.has_perm(f"{app_name}.access_level_3"):
            del actions["delete_selected"]
        return actions


class AdminImagePreview:
    """Mixin makes preview for uploaded images.

    Need to add parameters in admin class
        list_display = ("image_preview_list_page",)
        readonly_fields = ("image_preview_change_page",)
    """

    @admin.display(description="Превью")
    def image_preview_change_page(self, obj):
        return format_html(
            '<img src="{}" width="600" height="300" style="object-fit: contain;" />'.format(obj.image.url)
        )

    @admin.display(description="Превью")
    def image_preview_list_page(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="50" style="object-fit: contain;" />'.format(obj.image.url)
            )


class HideOnNavPanelAdminModelMixin:
    """Mixin hides model from admin main page(nav. panel)."""

    def has_module_permission(self, request):
        return False
