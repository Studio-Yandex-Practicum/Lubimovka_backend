from django.db import migrations


def rename_email_settings(apps, schema_editor):
    Setting = apps.get_model("core", "Setting")

    Setting.objects.filter(settings_key="email_send_from").update(
        description="Email адрес для исходящей почты и рассылок",
    )
    Setting.objects.filter(settings_key="email_to_send_questions").update(
        description="Email для вопросов и пожеланий (форма на странице 'Контакты')",
    )
    Setting.objects.filter(settings_key="submit_play_email").update(
        description="Email для формы подачи пьес (страница 'Подать пьесу')",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0032_add_default_roles"),
    ]

    operations = [
        migrations.RunPython(
            rename_email_settings, migrations.RunPython.noop
        ),
    ]
