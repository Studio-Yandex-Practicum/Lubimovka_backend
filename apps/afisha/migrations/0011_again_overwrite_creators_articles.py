from django.db import migrations
from django.db.models import IntegerField
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast


def load_creators(apps, schema_editor):
    Performance = apps.get_model("afisha", "Performance")
    contentType = ContentType.objects.get_for_model(Performance)
    perfomance_logs = LogEntry.objects\
        .annotate(object_id_as_int=Cast('object_id', IntegerField()))\
        .filter(object_id_as_int__in=Performance.objects.values_list('id'))\
        .filter(content_type=contentType)\
        .filter(action_flag=ADDITION)\
        .values("object_id_as_int", "user_id")
    for log in perfomance_logs:
        perfomance = Performance.objects.filter(id=log["object_id_as_int"])
        perfomance.update(creator=log["user_id"])


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0010_overwrite_creators_perfomances'),
    ]

    operations = [migrations.RunPython(load_creators)]
