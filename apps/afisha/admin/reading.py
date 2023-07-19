from django.contrib import admin

from apps.afisha.models import Reading
from apps.library.admin import TeamMemberInline


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "play",
    )
    exclude = ("events",)
    search_fields = (
        "name",
        "play__name",
    )
    autocomplete_fields = ("play",)
    inlines = (TeamMemberInline,)
