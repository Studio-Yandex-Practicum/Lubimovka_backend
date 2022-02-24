# Generated by Django 3.2.12 on 2022-02-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_data_delete_image_project_contents'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogitem',
            options={'ordering': ('-pub_date',), 'permissions': (('can_blog_publish', 'Может опубликовать блог'),), 'verbose_name': 'Запись блога', 'verbose_name_plural': 'Блог'},
        ),
        migrations.AlterModelOptions(
            name='newsitem',
            options={'ordering': ('-pub_date',), 'permissions': (('can_news_publish', 'Может опубликовать новость'),), 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-pub_date',), 'permissions': (('can_project_publish', 'Может опубликовать проект'),), 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
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
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default='IN_PROCESS', max_length=35, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='status',
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default='IN_PROCESS', max_length=35, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('IN_PROCESS', 'В работе'), ('REVIEW', 'На проверке'), ('READY_FOR_PUBLICATION', 'Готово к публикации'), ('PUBLISHED', 'Опубликовано'), ('REMOVED_FROM_PUBLICATION', 'Снято с публикации')], default='IN_PROCESS', max_length=35, verbose_name='Статус'),
        ),
    ]