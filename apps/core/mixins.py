from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.core.constants import STATUS_INFO
from apps.core.utils import get_object, get_user_perms_level


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom.

    Prevent changing and saving page if user do not have permission
    to change object in current Status.
    """

    def get_readonly_fields(self, request, obj=None):
        if obj:
            user_level = get_user_perms_level(request, obj)
            right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
            if user_level < right_to_change:
                return self.other_readonly_fields
        return super().get_readonly_fields(request, obj=obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = get_object(self, object_id)
        user_level = get_user_perms_level(request, obj)
        extra_context = {}
        extra_context["user_level"] = user_level
        extra_context["current_status_level"] = STATUS_INFO[obj.status]["min_access_level"]
        possible_changes = STATUS_INFO[obj.status]["possible_changes"]
        statuses = {}
        for status in possible_changes:
            statuses[status] = STATUS_INFO[status]

        # hide buttons SAVE if user doesnt have permissions to change in current status
        # used to prevent inlines changing
        extra_context["possible_statuses"] = statuses
        right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
        if user_level < right_to_change:
            extra_context["show_save"] = False
            extra_context["show_save_and_continue"] = False
            extra_context["show_save_and_add_another"] = False
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
    Also it restricts delete_selected for users which don't have
    highest level permissions.
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


class InlineReadOnlyMixin:
    """Makes Inlines read-only depends on status and user's permissions."""

    def has_add_permission(self, request, obj=None):
        if obj:
            user_level = get_user_perms_level(request, obj)
            right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
            if user_level < right_to_change:
                return False
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            user_level = get_user_perms_level(request, obj)
            right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
            if user_level < right_to_change:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            user_level = get_user_perms_level(request, obj)
            right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
            if user_level < right_to_change:
                return False
        return True


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
