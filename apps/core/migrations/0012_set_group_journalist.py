from django.db import migrations


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(
        name="journalist",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_add_press_release_data"),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
    ]
