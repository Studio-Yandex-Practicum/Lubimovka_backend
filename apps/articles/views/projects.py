from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.articles import selectors
from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer
from apps.core.utils import get_paginated_response


class ProjectListAPI(APIView):
    """Returns published Project items."""

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request):
        return get_paginated_response(
            pagination_class=self.pagination_class,
            serializer_class=ProjectListSerializer,
            queryset=Project.objects.published(),
            request=request,
            view=self,
        )


class ProjectDetailAPI(APIView):
    """Returns object `Project`."""

    def get(self, request, id):
        news_items = Project.objects.published()
        news_item_detail = get_object_or_404(news_items, id=id)
        context = {"request": request}
        serializer = ProjectSerializer(news_item_detail, context=context)
        return Response(serializer.data)


class ProjectsPreviewDetailAPI(APIView):
    """Returns preview page `Projects`."""

    def get(self, request, id):
        hash_sum = request.GET.get("hash", None)
        project_item_detail = selectors.preview_item_detail_get(Project, id, hash_sum)
        context = {"request": request}
        serializer = ProjectSerializer(project_item_detail, context=context)
        return Response(serializer.data)
