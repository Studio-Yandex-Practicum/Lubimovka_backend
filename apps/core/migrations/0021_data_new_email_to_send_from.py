from django.db import migrations


def change_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    values_for_update_email_send_from = {
        "text": "admin@lubimovka.ru",
        "description": "Почта для отправки писем с сайта"
    }
    Setting.objects.update_or_create(
        settings_key="email_send_from",
        defaults=values_for_update_email_send_from,
    )

    values_for_update_email_to_send_questions = {"description": "Почта для приёма вопросов"}
    Setting.objects.update_or_create(
        settings_key="email_to_send_questions",
        defaults=values_for_update_email_to_send_questions,
    )

    values_for_update_email_to_send_participations = {"description": "Почта для приёма заявок на участие"}
    Setting.objects.update_or_create(
        settings_key="email_to_send_participations",
        defaults=values_for_update_email_to_send_participations,
    )

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_alter_person_email"),
    ]

    operations = [
        migrations.RunPython(
            change_email_settings,
        ),
    ]
