from django.db import migrations


def add_press_release_setting(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="pr_director_name",
        text="Имя Фамилия в дательном падеже (пример: Анне Загородниковой)",
        description="Имя PR деректора на странице для прессы (в дательном падеже)",
    )
    Setting.objects.filter(settings_key="pr_manager_name").delete()

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_delete_template_id"),
    ]

    operations = [
        migrations.RunPython(
            add_press_release_setting,
        ),
    ]
