from django.db import migrations


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(
        name="journalist",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_auto_20220226_0242"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
    ]
