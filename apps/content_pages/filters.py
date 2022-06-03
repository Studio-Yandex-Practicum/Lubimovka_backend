from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CreatorFilter(admin.SimpleListFilter):
    title = _("Авторство")

    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (
            ("all", _("Все записи")),
            ("me_author", _("Я автор")),
        )

    def queryset(self, request, queryset):
        if self.value() == "me_author":
            return queryset.filter(creator=request.user)
        return queryset

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": changelist.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }
