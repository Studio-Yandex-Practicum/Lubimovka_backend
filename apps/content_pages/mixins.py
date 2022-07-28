from django.contrib import admin


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
        super().save_model(request, obj, form, change)
