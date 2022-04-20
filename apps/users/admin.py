from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Permission

from apps.core.models import Setting
from apps.core.utils import get_domain

from .forms import GroupAdminForm, UserAdminCreationForm, UserAdminForm, UserAdminPasswordResetForm
from .models import ProxyGroup

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    list_display = (
        "full_name",
        "username",
        "email",
        "is_active",
        "role",
        "get_last_login",
    )
    list_filter = (
        "groups",
        "is_active",
    )
    add_form = UserAdminCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "username",
        "full_name",
    )

    @admin.display(description="Дата последней авторизации")
    def get_last_login(self, obj):
        return obj.last_login

    @admin.display(description="Имя и фамилия")
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit `is_superuser` field."""
        if not request.user.is_superuser:
            return ("is_superuser", "date_joined", "last_login")
        return ("date_joined", "last_login")

    @admin.display(description="Роль")
    def role(self, obj):
        return obj.groups.first()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        reset_form = UserAdminPasswordResetForm({"email": obj.email})
        domain = get_domain(request)
        if reset_form.is_valid():
            reset_form.send_email_to_user(
                from_email=Setting.get_setting("email_send_from"),
                template_id=settings.MAILJET_TEMPLATE_ID_CHANGE_PASSWORD_USER,
                domain=domain,
            )


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ["name"]
    filter_horizontal = ("permissions",)


admin.site.register(ProxyGroup, GroupAdmin)


def permissions_new_unicode(self):
    # Translate default permissions
    class_name = str(self.content_type)
    permissions_name = str(self.name)
    if "Can delete log entry" in permissions_name:
        permissions_name = permissions_name.replace("Can delete log entry", "Может удалить запись в журнале")
    elif "Can change log entry" in permissions_name:
        permissions_name = permissions_name.replace("Can change log entry", "Может изменять запись в журнале")
    elif "Can add log entry" in permissions_name:
        permissions_name = permissions_name.replace("Can add log entry", "Может добавлять запись в журнале")
    elif "Can view log entry" in permissions_name:
        permissions_name = permissions_name.replace("Can view log entry", "Может просматривать запись в журнале")
    elif "Can delete" in permissions_name:
        permissions_name = permissions_name.replace("Can delete", "Может удалять")
    elif "Can add" in permissions_name:
        permissions_name = permissions_name.replace("Can add", "Может добавлять")
    elif "Can change" in permissions_name:
        permissions_name = permissions_name.replace("Can change", "Может изменять")
    elif "Can view" in permissions_name:
        permissions_name = permissions_name.replace("Can view", "Может просматривать")

    return "%s - %s" % (class_name.title(), permissions_name)


Permission.__str__ = permissions_new_unicode
