from django.contrib import admin
from django.core.exceptions import ValidationError


class SaveCreatorMixin:
    """Поле 'creator_name' для админ-классов унаследованных от BaseContentPageAdmin и PerformanceAdmin."""

    @admin.display(
        description="Создатель",
    )
    def creator_name(self, obj):
        if obj.creator:
            return f"{obj.creator.first_name} {obj.creator.last_name}"
        else:
            return "-"

    def save_model(self, request, obj, form, change):
        """При создании записи сохраняем ее создателя."""
        if form.is_valid():
            creator = request.user
            obj.creator = creator
            obj = form.save()
        else:
            raise ValidationError("Заполните поля корректно")
