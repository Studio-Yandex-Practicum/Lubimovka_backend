from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CreatorFilter(admin.SimpleListFilter):
    title = _("Авторство")

    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (("me_author", _("Я автор")),)

    def queryset(self, request, queryset):
        if self.value() == "me_author":
            return queryset.filter(creator=request.user)
        return queryset
