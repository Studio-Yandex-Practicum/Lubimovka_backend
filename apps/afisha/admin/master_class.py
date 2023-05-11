from django.contrib import admin

from apps.afisha.models import MasterClass
from apps.library.admin import TeamMemberInline


@admin.register(MasterClass)
class MasterClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("events",)
    search_fields = ("name",)
    inlines = (TeamMemberInline,)
