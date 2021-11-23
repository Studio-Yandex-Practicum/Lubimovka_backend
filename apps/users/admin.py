from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .forms import GroupAdminForm, UserAdminForm

User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    list_display = (
        "id",
        "username",
        "is_active",
        "role",
    )
    list_filter = (
        "email",
        "username",
    )

    def get_readonly_fields(self, request, obj=None):
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


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
