from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles import selectors
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


class ProjectsPreviewDetailAPI(APIView):
    """Returns preview page `Projects`."""

    def get(self, request, id):
        hash_sum = request.GET.get("hash", None)
        project_item_detail = selectors.preview_item_detail_get(Project, id, hash_sum)
        context = {"request": request}
        serializer = ProjectSerializer(project_item_detail, context=context)
        return Response(serializer.data)
