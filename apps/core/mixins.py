from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.afisha.models.performance import Performance
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
            if self.model._meta.object_name == "Performance":
                self.prepopulated_fields = {}
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
        if self.model._meta.object_name == "Performance":
            performance = Performance.objects.get(id=object_id)
            link = f"/{string_url[self.model._meta.object_name]}/{performance.slug}"
        else:
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
