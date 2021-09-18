from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .mixins import AdminOnlyPermissionsMixin

User = get_user_model()


class UserAdmin(AdminOnlyPermissionsMixin, DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "is_active",
        "role",
    )
    list_filter = ["email", "username", "role"]
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ["is_superuser"]


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
