from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model


def check_journalist_perms(request, obj):
    """Journalist can edit only own items."""
    creator = LogEntry.objects.filter(object_id=obj.id, content_type=get_content_type_for_model(obj)).first()
    visitor = request.user
    if creator and visitor.is_staff and visitor != creator.user:
        return 0
    return 1
