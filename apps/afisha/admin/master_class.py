from django.contrib import admin

from apps.afisha.admin.performance import TeamMemberInline
from apps.afisha.models.master_class import MasterClass


@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("events",)
    search_fields = (
        "project",
        "play__name",
        "name",
    )
    inlines = (TeamMemberInline,)
