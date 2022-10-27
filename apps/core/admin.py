from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

from apps.core.mixins import AdminImagePreview, HideOnNavPanelAdminModelMixin
from apps.core.models import CORE_ROLES, Image, Role, RoleType
from apps.core.utils import get_app_list

admin.AdminSite.get_app_list = get_app_list


@admin.register(Image)
class ImageAdmin(HideOnNavPanelAdminModelMixin, AdminImagePreview, admin.ModelAdmin):
    list_display = ("image_preview_list_page",)
    search_fields = ("image",)
    readonly_fields = ("image_preview_change_page",)


@admin.register(Role)
class RoleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("order", "name", "slug")
    list_display_links = ("name",)
    sortable_by = []
    search_fields = ("role",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("types",)
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit slug field."""
        if not request.user.is_superuser:
            self.prepopulated_fields = {}
            return ("slug",)
        return super().get_readonly_fields(request, obj)

    def delete_queryset(self, request, queryset):
        for object in queryset:
            if object.slug in CORE_ROLES:
                raise PermissionDenied(f'Удаление роли "{object.name}" невозможно.')
        return super().delete_queryset(request, queryset)


@admin.register(RoleType)
class RoleTypeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        """Remove the save and add new button."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Remove the delete button."""
        return False

    def get_model_perms(self, request):
        """Return empty perms dict thus hiding the model from admin index."""
        return {}


admin.site.site_header = "Администрирование сайта"
admin.site.unregister(Group)
