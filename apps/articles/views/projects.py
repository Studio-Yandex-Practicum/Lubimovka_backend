from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.models import Project
from apps.articles.serializers import ProjectListSerializer, ProjectSerializer


def project_prev_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    project = Project.objects.get(pk=object_pk)
    project.status = project.status.prev()
    project.save()
    return HttpResponseRedirect(reverse("admin:articles_project_change", args=[object_pk]))


def project_next_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    project = Project.objects.get(pk=object_pk)
    project.status = project.status.next()
    project.save()
    return HttpResponseRedirect(reverse("admin:articles_project_change", args=[object_pk]))


class ProjectsViewSet(ReadOnlyModelViewSet):
    """Returns published News items."""

    queryset = Project.ext_objects.published()

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    class Meta:
        model = Project
