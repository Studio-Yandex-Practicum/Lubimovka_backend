# Generated by Django 3.2.12 on 2022-02-22 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20220221_1205'),
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
    ]