from apps.articles.models import Project
from apps.content_pages.serializers import ModelWithContentPageSerializer


class ProjectSerializer(ModelWithContentPageSerializer):
    class Meta(ModelWithContentPageSerializer.Meta):
        model = Project
