from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string

from apps.users.forms import GroupAdminForm, UserAdminCreationForm, UserAdminForm
from apps.users.models import ProxyGroup
from apps.users.utils import send_reset_password_email

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    list_display = ("full_name", "username", "email", "is_active", "role", "last_login")
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
    readonly_fields = (
        "date_joined",
        "last_login",
    )

    @admin.display(description="Имя и фамилия")
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description="Роль")
    def role(self, obj):
        return obj.groups.all()[:1]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("groups")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            template_id = settings.MAILJET_TEMPLATE_ID_REGISTRATION_USER
            send_reset_password_email(request, obj, template_id)

    def response_change(self, request, obj):
        if "reset_password" in request.POST:
            obj.set_password(get_random_string(length=8))
            obj.save()
            template_id = settings.MAILJET_TEMPLATE_ID_RESET_PASSWORD_USER
            send_reset_password_email(request, obj, template_id)
            self.message_user(request, "Пароль был сброшен. Пользователю отправлена ссылка для смены пароля.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class HiddenAdmin(DjangoGroupAdmin):
    """Удаление модели из панели администратора.

    Необходимость регистрации модели в панели администратора
    вызвана применением пакета django-filer
    """

    def has_module_permission(self, request):
        return False


admin.site.unregister(Group)
admin.site.register(Group, HiddenAdmin)


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ["name"]
    filter_horizontal = ("permissions",)


admin.site.register(ProxyGroup, GroupAdmin)


def permissions_new_unicode(self):
    # Translate default permissions
    class_name = str(self.content_type)
    permissions_name = str(self.name)

    if "Can delete" in permissions_name:
        permissions_name = "разрешено удалять"
    elif "Can add" in permissions_name:
        permissions_name = "разрешено добавлять"
    elif "Can change" in permissions_name:
        permissions_name = "разрешено изменять"
    elif "Can view" in permissions_name:
        permissions_name = "разрешено просматривать"

    return "%s - %s" % (class_name.title(), permissions_name)


Permission.__str__ = permissions_new_unicode
