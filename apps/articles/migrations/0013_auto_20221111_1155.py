# Generated by Django 3.2.15 on 2022-11-11 08:55

from django.db import migrations, models


def reorder(apps, schema_editor):
    MyModel = apps.get_model("articles", "Project")
    for order, item in enumerate(MyModel.objects.all(), 1):
        item.order = order
        item.save(update_fields=['order'])


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_alter_project_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='order',
            field=models.PositiveSmallIntegerField(db_index=True, default=0, verbose_name='Порядок'),
        ),
        migrations.RunPython(reorder, reverse_code=migrations.RunPython.noop),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('order',), 'permissions': (('access_level_1', 'Права журналиста'), ('access_level_2', 'Права редактора'), ('access_level_3', 'Права главреда')), 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
    ]
