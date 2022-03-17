from django.contrib import admin

from apps.library.models import ProgramType


@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit slug field."""
        if not request.user.is_superuser:
            return ("slug",)
        return super().get_readonly_fields(request, obj)
