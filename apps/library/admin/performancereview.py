from django.contrib import admin
from django.db import models

from apps.core.widgets import FkSelect
from apps.library.models import PerformanceReview


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer_name",
        "performance",
        "pub_date",
    )
    list_filter = ("pub_date",)
    search_fields = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)
    formfield_overrides = {models.ForeignKey: {"widget": FkSelect}}
