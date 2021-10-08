# Generated by Django 3.2.7 on 2021-10-08 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_remove_festival_programms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festival',
            name='cities_count',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество участвующих городов'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(max_length=500, verbose_name='Текст вопроса'),
        ),
    ]
