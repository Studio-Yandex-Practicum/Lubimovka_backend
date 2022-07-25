# Generated by Django 3.2.13 on 2022-07-14 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0014_merge_20220713_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='supplemental_text',
            field=models.TextField(blank=True, help_text='Описание, расположенное под изображением', max_length=500, verbose_name='Дополнительное описание'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='description',
            field=models.TextField(blank=True, max_length=500, verbose_name='Краткое описание'),
        ),
    ]