from django.conf import settings
from django.contrib import admin, messages
from django.db import transaction
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from apps.articles.services import article_item_copy


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


class CopyActionMixin:
    """Adds copy action to the list view menu."""

    SUCCESS = "Успешно скопированы {count} {name}"
    AMOUNT_EXCEEDED = "Выберите не более {count} элементов из списка"

    @admin.action(description="Создать копию", permissions=["add"])
    def make_copy(self: admin.ModelAdmin, request, queryset):
        count = len(queryset)
        if count > settings.ARTICLES_MAX_ARTICLES_TO_COPY:
            self.message_user(
                request, self.AMOUNT_EXCEEDED.format(count=settings.ARTICLES_MAX_ARTICLES_TO_COPY), messages.WARNING
            )
            return
        for obj in queryset:
            with transaction.atomic():
                article = article_item_copy(obj, request.user)
                self.log_addition(
                    request,
                    article,
                    [
                        {
                            "added": {
                                "name": str(article._meta.verbose_name),
                                "object": str(article),
                            }
                        }
                    ],
                )

        self.message_user(request, self.SUCCESS.format(count=count, name=self.model._meta.verbose_name))
