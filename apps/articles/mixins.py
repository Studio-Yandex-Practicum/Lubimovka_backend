from django.contrib import admin
from django.urls import resolve
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from apps.articles.services import content_block_copy, copy_image

COPY_TITLE = "Копия {original_title}"


class PubDateSchemaMixin:
    """Adds examples how `PubDateFilter` (filter by month and year) works."""

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="month",
                description="Фильтрация по месяцу",
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Ноябрь",
                        description="Для фильтрации по месяцу нужно указать номер месяца от 1 до 12",
                        value="11",
                    ),
                ],
            ),
            OpenApiParameter(
                name="year",
                description="Фильтрация по году",
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Текущий год",
                        description="Для фильтрации нужно указать год",
                        value="2021",
                    ),
                ],
            ),
            OpenApiParameter(
                name="ordering",
                description="Which field to use when ordering the results.",
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Сортировка года по возрастанию",
                        description="Параметр сортирует год по возрастанию",
                        value="pub_date__year",
                    ),
                    OpenApiExample(
                        "Example 2",
                        summary="Сортировка года по убыванию",
                        description="Параметр сортирует год по убыванию",
                        value="-pub_date__year",
                    ),
                    OpenApiExample(
                        "Example 3",
                        summary="Сортировка месяца по возрастанию",
                        description="Параметр сортирует месяц по возрастанию",
                        value="pub_date__month",
                    ),
                    OpenApiExample(
                        "Example 4",
                        summary="Сортировка месяца по убыванию",
                        description="Параметр сортирует месяц по убыванию",
                        value="-pub_date__month",
                    ),
                ],
            ),
        ],
    )
    def list(self, request):
        return super().list(request)


class ArticleSaveAsMixin:
    """Align Django save as functionality with Article model."""

    def get_form(self: admin.ModelAdmin, request, obj, change, **kwargs):
        """Make image field optional field to allow for successful validation."""
        form = super().get_form(request, obj, change, **kwargs)
        if request.method == "POST" and "_saveasnew" in request.POST:
            form.base_fields["image"].required = False
        return form

    def save_model(self: admin.ModelAdmin, request, obj, form, change):
        """Copy image from old object when saving as new."""
        if "_saveasnew" in request.POST and "image" not in request.FILES:
            source_pk = resolve(request.path).kwargs["object_id"]
            source_obj = self.get_object(request, source_pk)
            copy_image(source_obj.image, obj.image)
            if obj.title == source_obj.title:
                obj.title = COPY_TITLE.format(original_title=obj.title)
        return super().save_model(request, obj, form, change)

    def save_related(self: admin.ModelAdmin, request, form, formsets, change):
        """Replace blocks with their copies when saving as new."""
        super().save_related(request, form, formsets, change)
        if "_saveasnew" in request.POST:
            obj = form.instance
            for content in obj.contents.all():
                BlockModel = content.content_type.model_class()
                block = BlockModel.objects.get(pk=content.object_id)
                content.object_id = content_block_copy(block).pk
                content.save()
