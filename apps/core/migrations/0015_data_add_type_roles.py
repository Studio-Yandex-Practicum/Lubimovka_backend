from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    roles = [
        {
            "name": "Актёр",
            "slug": "actor",
            "type_roles": "performanse_roles",
        },
        {
            "name": "Адаптация текста",
            "slug": "text_adaptation",
            "type_roles": "blog_persons_roles",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "type_roles": "play_roles",
        },
        {
            "name": "Режиссёр",
            "slug": "director",
            "type_roles": "performanse_roles",
        },
        {
            "name": "Переводчик",
            "slug": "translator",
            "type_roles": "blog_persons_roles",
        },
        {
            "name": "Ведущий",
            "slug": "host",
            "type_roles": "play_roles",
        },
        {
            "name": "Текст",
            "slug": "text",
            "type_roles": "blog_persons_roles",
        },
        {
            "name": "Иллюстрации",
            "slug": "illustrations",
            "type_roles": "blog_persons_roles",
        },
        {
            "name": "Фото",
            "slug": "photo",
            "type_roles": "blog_persons_roles",
        },
    ]
    for role in roles:
        role_obj = Role.objects.get(name=role["name"])
        role_obj.type_roles = role["type_roles"]
        role_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_auto_20211130_2202"),
    ]

    operations = [migrations.RunPython(create_roles)]
