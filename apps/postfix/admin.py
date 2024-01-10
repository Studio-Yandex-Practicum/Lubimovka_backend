from typing import Any, Union

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from apps.postfix.models import Recipient, Virtual

ENABLE_SUMMARY = "Включена переадресация для {count} адресов"
DISABLE_SUMMARY = "Отключена переадресация для {count} адресов"


class RecipientsInline(admin.TabularInline):
    model = Recipient
    extra = 0

    def get_readonly_fields(self, request: HttpRequest, obj: Union[Virtual, None]) -> tuple[Any, ...]:
        fields = super().get_readonly_fields(request, obj)
        return tuple(fields) + (("email",) if obj and obj.author else ())

    def has_add_permission(self, request: HttpRequest, obj: Virtual) -> bool:
        return False if obj.author else super().has_add_permission(request, obj)

    def has_delete_permission(self, request: HttpRequest, obj: Virtual) -> bool:
        return False if obj.author else super().has_add_permission(request, obj)


@admin.register(Virtual)
class VirtualAdmin(admin.ModelAdmin):
    list_display = ("enabled", "mailbox", "author", "list_recipients")
    list_display_links = ("mailbox",)
    list_editable = ("enabled",)
    inlines = (RecipientsInline,)
    actions = ("enable_selected", "disable_selected")

    search_fields = ("author__person__first_name", "author__person__last_name", "mailbox", "recipients__email")
    readonly_fields = ("author",)

    @admin.display(description="получатели")
    def list_recipients(self, obj: Virtual):
        return ", ".join(recipient.email for recipient in obj.recipients.all())

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related("recipients").select_related("author")

    def get_readonly_fields(self, request: HttpRequest, obj: Union[Virtual, None]) -> tuple[Any, ...]:
        fields = super().get_readonly_fields(request, obj)
        return tuple(fields) + (("mailbox",) if obj and obj.author else ())

    @admin.action(description="Включить переадресацию электронной почты")
    def enable_selected(modeladmin, request, queryset):
        queryset.update(enabled=True)
        modeladmin.message_user(request, ENABLE_SUMMARY.format(count=len(queryset)))

    @admin.action(description="Отключить переадресацию электронной почты")
    def disable_selected(modeladmin, request, queryset):
        queryset.update(enabled=False)
        modeladmin.message_user(request, DISABLE_SUMMARY.format(count=len(queryset)))
