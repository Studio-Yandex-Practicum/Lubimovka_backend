from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    RoleType = apps.get_model("core", "RoleType")
    roles = [
        {
            "name": "Драматург",
            "slug": "dramatist",
            "types": "performanse_role",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "types": "reading_role",
        },
        {
            "name": "Режиссёр",
            "slug": "director",
            "types": "reading_role",
        },
        {
            "name": "Ведущий",
            "slug": "host",
            "types": "master_class_role",
        },
    ]
    for role in roles:
        role_obj = Role.objects.get(name=role["name"])
        type_of_role = RoleType.objects.get(role_type=role["types"])
        role_obj.types.add(type_of_role)
        role_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_data_roles_add_plural"),
    ]

    operations = [migrations.RunPython(create_roles)]
