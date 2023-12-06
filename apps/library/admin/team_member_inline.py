from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.afisha.models import Performance, Reading
from apps.core.mixins import InlineReadOnlyMixin
from apps.core.models import Role
from apps.library.models import Play, TeamMember


class TeamMemberInline(SortableInlineAdminMixin, InlineReadOnlyMixin, admin.TabularInline):
    model = TeamMember
    fields = (
        "person",
        "role",
    )
    autocomplete_fields = ("person",)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("role", "order")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Restricts role types for the model where inline is used."""
        LIMIT_ROLES = {
            Performance: "performanse_role",
            Play: "play_role",
            Reading: "reading_role",
        }
        if db_field.name == "role":
            if self.parent_model in LIMIT_ROLES.keys():
                kwargs["queryset"] = Role.objects.filter(types__role_type=LIMIT_ROLES[self.parent_model])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TeamMemberInlineCollapsible(TeamMemberInline):
    classes = ("collapsible",)
