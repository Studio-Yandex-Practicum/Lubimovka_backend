from collections.abc import Iterable

from django.contrib import admin, messages
from django.core import checks
from django.db.models import FileField
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.core.constants import STATUS_INFO, Status
from apps.core.utils import get_domain, get_object, get_user_change_perms_for_status, get_user_perms_level


class StatusButtonMixin:
    """Mixin to add status-change buttons on page bottom.

    Prevent deleting selected objects on list page if user is not admin or superuser.
    Make all fields readonly and hide buttons Save if user has no permission to change
    according to object's status.
    Hide button Delete if user has no permission according to object's status.
    """

    def get_actions(self, request):
        app_name = self.model._meta.app_label
        actions = super().get_actions(request)
        if "delete_selected" in actions and not request.user.has_perm(f"{app_name}.access_level_3"):
            del actions["delete_selected"]
        return actions

    def get_readonly_fields(self, request, obj=None):
        if not get_user_change_perms_for_status(request, obj):
            return self.other_readonly_fields
        return super().get_readonly_fields(request, obj=obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = get_object(self, object_id)
        if not hasattr(obj, "status"):
            return super().change_view(request, object_id, form_url, extra_context)
        user_level = get_user_perms_level(request, obj)

        # making Status buttons context for template
        possible_changes = STATUS_INFO[obj.status]["possible_changes"]
        statuses = {}
        for status in possible_changes:
            statuses[status] = STATUS_INFO[status]
        extra_context = {}
        extra_context["user_level"] = user_level
        extra_context["level_to_change"] = STATUS_INFO[obj.status]["min_level_to_change"]
        extra_context["possible_statuses"] = statuses

        # hide buttons SAVE if user doesn't have permission to change in current status
        right_to_change = STATUS_INFO[obj.status]["min_level_to_change"]
        if user_level < right_to_change:
            extra_context["show_save"] = False
            extra_context["show_save_and_continue"] = False
            extra_context["show_save_and_add_another"] = False

        # hide button DELETE if user doesn't have permission to delete in current status
        right_to_delete = STATUS_INFO[obj.status]["min_level_to_delete"]
        if user_level < right_to_delete:
            extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        user_level = get_user_perms_level(request, obj)
        if user_level >= STATUS_INFO[obj.status]["min_level_to_change"]:
            for status in STATUS_INFO:
                if status in request.POST:
                    if (
                        obj._meta.model_name == "performance"
                        and not obj.play.published
                        and status == Status.PUBLISHED.value
                    ):
                        self.message_user(
                            request, "Статус спектакля не обновлён. Пьеса должна быть опубликована!", messages.ERROR
                        )
                        return HttpResponseRedirect(".")
                    obj.status = status
                    obj.save()
                    self.message_user(request, "Статус успешно обновлён!")
                    return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class PreviewButtonMixin:
    """Mixin to add preview buttons on change page.

    Pass hash and name of url to context.
    """

    def change_view(self, request, object_id, form_url="", extra_context=None):
        string_url = {
            "BlogItem": "blog",
            "NewsItem": "news",
            "Project": "projects",
            "Performance": "performances",
        }
        link = f"/{string_url[self.model._meta.object_name]}/{object_id}"
        # add hash for unpublished pages and change button name
        preview_button_context = {}
        if self.model.objects.is_published(object_id):
            preview_button_context["button_name"] = "Просмотр страницы"
            preview_button_context["link"] = link
        # FIXME: Ждем когда функционал для предпросмотра будет готов на фронтенде
        # ДОБАВИТЬ ИМПОРТ calculate_hash из apps.core.utils
        # else:
        #     preview_button_context["button_name"] = "Предпросмотр страницы"
        #     preview_button_context["link"] = f"{link}?hash={calculate_hash(object_id)}"
        extra_context["preview_button_context"] = preview_button_context
        extra_context.update(preview_button_context)
        return super().change_view(request, object_id, form_url, extra_context)


class InlineReadOnlyMixin:
    """Makes Inlines read-only depends on status and user's permissions."""

    def has_add_permission(self, request, obj=None):
        return get_user_change_perms_for_status(request, obj)

    def has_change_permission(self, request, obj=None):
        return get_user_change_perms_for_status(request, obj)

    def has_delete_permission(self, request, obj=None):
        return get_user_change_perms_for_status(request, obj)


class AdminImagePreview:
    """Mixin makes preview for uploaded images.

    Need to add parameters in admin class
        list_display = ("image_preview_list_page",)
        or readonly_fields = ("image_preview_change_page",)
        or readonly_fields = ("inline_image_preview",)
    """

    @admin.display(description="Превью")
    def image_preview_change_page(self, obj):
        return format_html('<img src="{}" height="300" style="object-fit: contain;" />'.format(obj.image.url))

    @admin.display(description="Превью")
    def inline_image_preview(self, obj):
        return format_html('<img src="{}" height="150" style="object-fit: contain;" />'.format(obj.image.image.url))

    @admin.display(description="Превью")
    def image_preview_list_page(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" style="object-fit: contain;" />'.format(obj.image.url))


class HideOnNavPanelAdminModelMixin:
    """Mixin hides model from admin main page(nav. panel)."""

    def has_module_permission(self, request):
        return False


class GetDomainMixin:
    """Serializer mixin to generate URLs with domain."""

    def prepend_domain(self, url):
        return get_domain(self.context["request"]) + str(url)


class FileCleanUpMixin:
    """Delete old image/file file when image/file is changed or deleted.

    Add the mixin to the model class parents and setup the
    `cleanup_fields` tuple as the model's attribute, containing a sequence of
    the model's ImageField field names, for which you want to delete the
    file after the field is altered.
    """

    @classmethod
    def _check_field_tuple(cls):
        fields = getattr(cls, "cleanup_fields", None)
        if not fields:
            return [
                checks.Error(
                    "cleanup_fields attribute is missing",
                    hint="Add the cleanup_fields attribute to the model class or remove ImageCleanUpMixin",
                    obj=cls,
                )
            ]
        if isinstance(fields, str):
            return [
                checks.Error(
                    "cleanup_fields attribute must not be a str instance",
                    hint="It is recommended to assign cleanup_fields a tuple of field names",
                    obj=cls,
                )
            ]
        if not issubclass(type(fields), Iterable):
            return [
                checks.Error(
                    "cleanup_fields attribute must be iterable",
                    hint="It is recommended to assign cleanup_fields a tuple of field names",
                    obj=cls,
                )
            ]
        errors = []
        for field in fields:
            if not hasattr(cls, field):
                errors.append(
                    checks.Error(
                        f"{field} is listed in the cleanup_fields, but not found in the model",
                        hint="Check the field exists in the model",
                        obj=cls,
                    )
                )
                continue
            if not issubclass(type(cls._meta.get_field(field)), FileField):
                errors.append(
                    checks.Error(
                        f"{field} is not a FileField or an ImageField",
                        hint="Remove the field from the cleanup_fields attribute",
                        obj=cls,
                    )
                )
        return errors

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_field_tuple())
        return errors

    def save(self, *args, **kwargs):
        this = type(self).objects.filter(id=self.id).first()
        if this:
            for field in self.cleanup_fields:
                attr = getattr(this, field)
                if attr != getattr(self, field):
                    attr.delete(save=False)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for attr in (getattr(self, field) for field in self.cleanup_fields):
            storage, path = attr.storage, attr.path
            super().delete(*args, **kwargs)
            storage.delete(path)
