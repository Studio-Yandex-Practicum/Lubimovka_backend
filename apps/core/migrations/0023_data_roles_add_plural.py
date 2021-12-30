from django.db import migrations


def add_plural(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    roles = [
        {
            "name": "Актёр",
            "name_plural": "Актёры",
        },
        {
            "name": "Адаптация текста",
            "name_plural": "Адаптация текста",
        },
        {
            "name": "Драматург",
            "name_plural": "Драматурги",
        },
        {
            "name": "Режиссёр",
            "name_plural": "Режиссёры",
        },
        {
            "name": "Переводчик",
            "name_plural": "Переводчики",
        },
        {
            "name": "Ведущий",
            "name_plural": "Ведущие",
        },
        {
            "name": "Текст",
            "name_plural": "Текст",
        },
        {
            "name": "Иллюстрации",
            "name_plural": "Иллюстрации",
        },
        {
            "name": "Фото",
            "name_plural": "Фото",
        },
    ]
    for role in roles:
        obj = Role.objects.get(name=role["name"])
        obj.name_plural = role["name_plural"]
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_role_name_plural"),
    ]

    operations = [migrations.RunPython(add_plural)]
