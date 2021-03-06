from django.db import migrations
from django.db.models import IntegerField
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Cast


def load_creators(apps, schema_editor):
    def load_using_model_name(model_name):
        Model = apps.get_model("articles", model_name)
        contentType = ContentType.objects.get_for_model(Model)
        model_logs = LogEntry.objects\
            .annotate(object_id_as_int=Cast('object_id', IntegerField()))\
            .filter(object_id_as_int__in=Model.objects.values_list('id'))\
            .filter(content_type=contentType)\
            .filter(action_flag=ADDITION)\
            .values("object_id_as_int", "user_id")
        for log in model_logs:
            model = Model.objects.filter(id=log["object_id_as_int"])
            model.update(creator=log["user_id"])

    load_using_model_name("Project")
    load_using_model_name("BlogItem")
    load_using_model_name("NewsItem")


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_overwrite_creators_articles'),
    ]

    operations = [migrations.RunPython(load_creators)]
