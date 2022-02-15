from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .forms import GroupAdminForm, UserAdminForm
from .models import ProxyGroup

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    list_display = (
        "full_name",
        "username",
        "is_active",
        "role",
        "get_last_login",
    )
    list_filter = (
        "groups",
        "is_active",
    )

    @admin.display(description="Последний визит")
    def get_last_login(self, obj):
        return obj.last_login

    @admin.display(description="Имя и фамилия")
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit `is_superuser` field."""
        if not request.user.is_superuser:
            return ("is_superuser",)
        return super().get_readonly_fields(request, obj)

    @admin.display(description="Роль")
    def role(self, obj):
        return obj.groups.first()


class GroupAdmin(admin.ModelAdmin):

    form = GroupAdminForm
    list_display = ["name"]
    filter_horizontal = ("permissions",)


admin.site.register(ProxyGroup, GroupAdmin)
