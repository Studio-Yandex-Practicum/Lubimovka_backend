from django.db import migrations


def add_press_release_setting(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="pr_manager_name",
        text="Имя Фамилия в дателльном падеже (пример: Анне Загородниковой)",
        description="Данные о PR-менеджере на странице для прессы",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_settings_change_data"),
    ]

    operations = [
        migrations.RunPython(
            add_press_release_setting,
        ),
    ]
