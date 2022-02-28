from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.core.constants import STATUS_INFO
from apps.core.utils import get_user_perms_level


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom."""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = {}
        obj_class = self.model
        obj = obj_class.objects.get(pk=object_id)
        app_name = obj._meta.app_label
        extra_context["user_level"] = get_user_perms_level(request, app_name)
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
        obj_class = self.model
        obj = obj_class.objects.get(pk=object_id)
        app_name = obj._meta.app_label
        access_to_delete = STATUS_INFO[obj.status]["min_access_to_delete"]
        user_level = get_user_perms_level(request, app_name)
        if user_level < access_to_delete:
            extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)


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
