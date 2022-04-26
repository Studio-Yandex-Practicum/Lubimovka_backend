from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer


class ProjectsViewSet(ReadOnlyModelViewSet):
    """Returns published Project items."""

    queryset = Project.ext_objects.published()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    class Meta:
        model = Project


class PreviewProjectsDetailAPI(APIView):
    """Returns preview page of `Project` object."""

    def get(self, request, id, **kwargs):
        project_item_detail = get_object_or_404(Project, id=id)
        context = {"request": request}
        serializer = ProjectSerializer(project_item_detail, context=context)
        return Response(serializer.data)
