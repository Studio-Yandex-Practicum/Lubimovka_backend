from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer
from apps.library.utilities import set_next_status, set_prev_status


class ProjectsViewSet(ReadOnlyModelViewSet):
    """Returns published News items."""

    queryset = Project.ext_objects.published()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    class Meta:
        model = Project


def project_prev_status(request, object_pk):
    return set_prev_status(request=request, object_pk=object_pk, object_model=Project, view_name="articles_project")


def project_next_status(request, object_pk):
    return set_next_status(request=request, object_pk=object_pk, object_model=Project, view_name="articles_project")
