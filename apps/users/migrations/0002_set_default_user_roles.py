from django.db import migrations
from django.db.models import Q


def set_default_groups(apps, schema_editor):

    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create(
        [
            Group(name="admin"),
            Group(name="editor"),
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
    ]
