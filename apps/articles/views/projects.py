from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer


class ProjectsViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    class Meta:
        model = Project
