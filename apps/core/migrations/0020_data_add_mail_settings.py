from django.db import migrations


def add_settings(apps, schema_editor):

    Settings = apps.get_model("core", "Setting")

    Settings.objects.filter(settings_key="mail_send_to").delete()

    Settings.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_question_template_id",
        text="3420599",
        description="Id шаблона письма с вопросом",
    )
    Settings.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_send_from",
        text="questions@lyubimovka.ru",
        description="Почта для отправки вопроса",
    )
    Settings.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_send_to",
        text="admin@lyubimovka.ru",
        description="Почта для приёма вопроса",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_sorting_settings_by_groups"),
    ]

    operations = [migrations.RunPython(add_settings)]
