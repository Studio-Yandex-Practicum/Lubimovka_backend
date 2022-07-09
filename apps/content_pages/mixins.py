from django.contrib import admin
from rest_framework.exceptions import PermissionDenied

from apps.articles.utils import journalist_has_not_perms


class SaveCreatorMixin:
    """Поле 'creator_name' для админ-классов унаследованных от BaseContentPageAdmin и PerformanceAdmin."""

    @admin.display(
        description="Создатель",
    )
    def creator_name(self, obj):
        return f"{obj.creator.first_name} {obj.creator.last_name}"

    def save_model(self, request, obj, form, change):
        """При создании записи сохраняем ее создателя.

        Журналист может редактировать только свои записи.
        """
        if not change:
            creator = request.user
            obj.creator = creator
        if journalist_has_not_perms(request, obj):
            raise PermissionDenied()
        super().save_model(request, obj, form, change)
