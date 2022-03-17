# Generated by Django 3.2.12 on 2022-02-28 17:37

from django.db import migrations, models

from apps.core.constants import Status


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_project_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogitem',
            options={'ordering': ('-pub_date',), 'permissions': (('access_level_1', 'Права журналиста'), ('access_level_2', 'Права редактора'), ('access_level_3', 'Права главреда')), 'verbose_name': 'Запись блога', 'verbose_name_plural': 'Блог'},
        ),
        migrations.AlterModelOptions(
            name='newsitem',
            options={'ordering': ('-pub_date',), 'permissions': (('access_level_1', 'Права журналиста'), ('access_level_2', 'Права редактора'), ('access_level_3', 'Права главреда')), 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-pub_date',), 'permissions': (('access_level_1', 'Права журналиста'), ('access_level_2', 'Права редактора'), ('access_level_3', 'Права главреда')), 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.RemoveField(
            model_name='blogitem',
            name='is_draft',
        ),
        migrations.RemoveField(
            model_name='newsitem',
            name='is_draft',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_draft',
        ),
        migrations.AddField(
            model_name='blogitem',
            name='status',
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default=Status.IN_PROCESS, max_length=35, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='status',
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default=Status.IN_PROCESS, max_length=35, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default=Status.IN_PROCESS, max_length=35, verbose_name='Статус'),
        ),
    ]
