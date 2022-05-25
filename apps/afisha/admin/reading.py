from django.contrib import admin

from apps.afisha.models import Reading
from apps.library.admin import TeamMemberInline
from apps.library.models import Play


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "play",
        "name",
    )
    exclude = ("events",)
    search_fields = (
        "name",
        "play__name",
    )
    autocomplete_fields = ("play",)
    inlines = (TeamMemberInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["play"].queryset = Play.objects.filter(other_play=False)
        return form
