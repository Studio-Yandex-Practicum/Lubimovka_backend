from django.db import migrations


def add_to_model(apps, schema_editor):
    static_pages_model = apps.get_model("static_pages", "StaticPagesModel")
    what_we_do = static_pages_model.objects.create(
        title='Страница "Что мы делаем"',
        static_page_url="what-we-do",
        data="# markdown text",
    )
    ideology = static_pages_model.objects.create(
        title='Страница "Страница "Идеология"',
        static_page_url="ideology",
        data="# markdown text",
    )
    history = static_pages_model.objects.create(
        title='Страница "История"',
        static_page_url="history",
        data="# markdown text",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("static_pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            add_to_model, reverse_code=migrations.RunPython.noop
        ),
    ]
