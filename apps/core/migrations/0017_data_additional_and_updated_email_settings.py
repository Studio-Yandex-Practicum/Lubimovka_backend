from django.db import migrations


def add_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_volunteers_page",
        email="author@gmail.com",
        description="Почта для тех кто хочет стать волонтером",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_blog_page",
        email="author@gmail.com",
        description="Почта для тех кто хочет стать автором",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_support_page",
        email="author@gmail.com",
        description="Почта для получения отчетности об использовании пожертвований",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_add_new_emails'),
    ]

    operations = [
        migrations.RunPython(
            add_email_settings,
        ),
    ]
