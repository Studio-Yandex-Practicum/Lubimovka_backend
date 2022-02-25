from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom."""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj_class = self.model
        obj = obj_class.objects.get(pk=object_id)
        statuses = dict(obj.STATUS_INFO)
        statuses.pop(obj.status, None)
        if not obj.status == "PUBLISHED":
            statuses.pop("REMOVED_FROM_PUBLICATION", None)
        extra_context = {}
        extra_context["statuses"] = statuses
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        for status in obj.STATUS_INFO:
            if status in request.POST:
                obj.status = status
                obj.save()
                self.message_user(request, "Статус успешно обновлён!")
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)


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
