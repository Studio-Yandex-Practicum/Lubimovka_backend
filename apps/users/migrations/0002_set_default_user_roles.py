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
    Permission = apps.get_model("auth", "Permission")
    permissions = Permission.objects.filter(
        Q(codename__endswith="event")
        | Q(codename__endswith="blogitem")
        | Q(codename__endswith="newsitem")
        | Q(codename__endswith="project")
        | Q(codename__endswith="image")
        | Q(codename__endswith="performance")
        | Q(codename__endswith="play")
    ).exclude(name__contains="delete")

    admin = Group.objects.get(name="admin")
    admin.permissions.add(*Permission.objects.all())
    editor = Group.objects.get(name="editor")
    editor.permissions.add(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
    ]
