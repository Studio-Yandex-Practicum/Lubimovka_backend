from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.core.status_source import get_status_info_for_app


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom."""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = {}
        obj_class = self.model
        obj = obj_class.objects.get(pk=object_id)
        app_name = obj._meta.app_label
        status_info = get_status_info_for_app(app_name)
        extra_context["access_level"] = status_info[obj.status]["access_level"]
        possible_changes = status_info[obj.status]["possible_changes"]
        statuses = {}
        for status in possible_changes:
            statuses[status] = status_info[status]
        extra_context["possible_statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        app_name = obj._meta.app_label
        status_info = get_status_info_for_app(app_name)
        for status in status_info:
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
        status_info = get_status_info_for_app(app_name)
        access_to_delete = status_info[obj.status]["access_to_delete"]
        flag = False
        for perm in access_to_delete:
            if request.user.has_perm(perm):
                flag = True
        if not flag:
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
