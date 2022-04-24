from django.contrib import admin

from apps.feedback.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "author_email", "question", "sent")
    list_filter = ("sent",)

    def has_module_permission(self, request):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
            return super().has_module_permission(request)
        return False
