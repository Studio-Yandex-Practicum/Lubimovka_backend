from django.db import migrations


def change_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.filter(
        settings_key="email_subject_for_question",
    ).delete()

    Setting.objects.get_or_create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_to_send_participations",
        text="lubimovka-2021@yandex.ru",
        description="Почта для приёма заявок на участие.",
    )

    values_for_update_email_send_from = {"description": "Почта для отправки писем."}
    Setting.objects.update_or_create(
        settings_key="email_send_from",
        defaults=values_for_update_email_send_from,
    )

    values_for_update_email_to_send_questions = {
        "settings_key": "email_to_send_questions",
        "description": "Почта для приёма вопросов.",
    }
    Setting.objects.update_or_create(
        settings_key="email_send_to",
        defaults=values_for_update_email_to_send_questions,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_add_press_realease_data"),
    ]

    operations = [
        migrations.RunPython(
            change_email_settings,
        ),
    ]
