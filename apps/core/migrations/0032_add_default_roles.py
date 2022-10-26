from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    roles = [
        {
            "name": "Драматургиня",
            "name_plural": "Драматургини",
            "slug": "dramatess",
        },
        {
            "name": "Режиссёрка",
            "name_plural": "Режиссёрки",
            "slug": "directress",
        }
    ]
    for role in roles:
        role_obj, _ = Role.objects.get_or_create(**role)
        role_obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0031_merge_20220905_1615'),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
