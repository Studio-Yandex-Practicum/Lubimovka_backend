from typing import Any, Union

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from apps.postfix.models import Recipient, Virtual


class RecipientsInline(admin.TabularInline):
    model = Recipient
    extra = 0

    def get_readonly_fields(self, request: HttpRequest, obj: Union[Virtual, None]) -> tuple[Any, ...]:
        fields = super().get_readonly_fields(request, obj)
        return tuple(fields) + (("email",) if obj and obj.author else ())


@admin.register(Virtual)
class VirtualAdmin(admin.ModelAdmin):
    list_display = ("enabled", "mailbox", "author", "list_recipients")
    list_display_links = ("mailbox",)
    list_editable = ("enabled",)
    inlines = (RecipientsInline,)

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
