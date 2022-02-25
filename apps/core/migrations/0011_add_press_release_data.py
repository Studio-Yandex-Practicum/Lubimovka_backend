from django.db import migrations


def add_press_release_setting(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="pr_manager_name",
        text="Имя Фамилия в дателльном падеже (пример: Анне Загородниковой)",
        description="Имя PR менеджера на странице для прессы (в дательном падеже)",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_setting_group"),
    ]

    operations = [
        migrations.RunPython(
            add_press_release_setting,
        ),
    ]
