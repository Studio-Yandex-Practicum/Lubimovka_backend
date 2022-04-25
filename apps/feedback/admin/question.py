from django.contrib import admin

from apps.feedback.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "author_email", "question", "sent")
    list_filter = ("sent",)
