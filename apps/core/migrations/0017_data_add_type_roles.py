from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    RoleType = apps.get_model("core", "RoleType")
    roles = [
        {
            "name": "Актёр",
            "slug": "actor",
            "type_roles": "performanse_role",
        },
        {
            "name": "Адаптация текста",
            "slug": "text_adaptation",
            "type_roles": "blog_persons_role",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "type_roles": "play_role",
        },
        {
            "name": "Режиссёр",
            "slug": "director",
            "type_roles": "performanse_role",
        },
        {
            "name": "Переводчик",
            "slug": "translator",
            "type_roles": "blog_persons_role",
        },
        {
            "name": "Ведущий",
            "slug": "host",
            "type_roles": "play_role",
        },
        {
            "name": "Текст",
            "slug": "text",
            "type_roles": "blog_persons_role",
        },
        {
            "name": "Иллюстрации",
            "slug": "illustrations",
            "type_roles": "blog_persons_role",
        },
        {
            "name": "Фото",
            "slug": "photo",
            "type_roles": "blog_persons_role",
        },
    ]
    for role in roles:
        role_obj = Role.objects.get(name=role["name"])
        role_obj.type_roles.add(
            RoleType.objects.get(role_type=role["type_roles"])
        )
        role_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_data_role_types"),
    ]

    operations = [migrations.RunPython(create_roles)]
