from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from apps.postfix.models import Recipient, Virtual, VirtualAuthor


class RecipientsInline(admin.TabularInline):
    model = Recipient


@admin.register(Virtual)
class VirtualAdmin(admin.ModelAdmin):
    list_display = ("enabled", "email", "list_recipients")
    list_display_links = ("email",)
    list_editable = ("enabled",)
    inlines = (RecipientsInline,)

    search_fields = ("email", "recipients__email")

    @admin.display(description="получатели")
    def list_recipients(self, obj: Virtual):
        return ", ".join(recipient.email for recipient in obj.recipients.all())

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(author__isnull=True).prefetch_related("recipients")


@admin.register(VirtualAuthor)
class VirtualAuthorAdmin(admin.ModelAdmin):
    list_display = ("enabled", "author", "email", "recipient")
    list_display_links = ("author",)
    list_editable = ("enabled", "email")

    search_fields = ("author__person__first_name", "author__person__last_name", "email", "author__person__email")
    readonly_fields = ["slug"]

    @admin.display(description="получатель")
    def recipient(self, obj: VirtualAuthor):
        return obj.author.person.email

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related("author__person")
