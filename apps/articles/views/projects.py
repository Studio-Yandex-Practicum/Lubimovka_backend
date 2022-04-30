from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer
from apps.core.utils import create_hash


class ProjectsViewSet(ReadOnlyModelViewSet):
    """If `ingress` exist returns preview page else returns published items."""

    def get_queryset(self, **kwargs):
        object_id = self.kwargs["pk"]
        model_name = "project"
        ingress = self.request.GET.get("ingress", "")
        if ingress == create_hash(object_id, model_name):
            queryset = Project.ext_objects.current_and_published(object_id)
        else:
            queryset = Project.ext_objects.published()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    class Meta:
        model = Project
