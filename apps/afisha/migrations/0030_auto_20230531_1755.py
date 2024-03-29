# Generated by Django 3.2.18 on 2023-05-31 14:55

from django.db import migrations, models
import django.db.models.deletion


def reading_to_custom(apps, schema_editor):
    Event = apps.get_model("afisha", "Event")
    Event.objects.filter(type="READING").update(type="CUSTOM")


def custom_to_reading(apps, schema_editor):
    Event = apps.get_model("afisha", "Event")
    Event.objects.filter(type="CUSTOM").update(type="READING")
    Event.objects.filter(location__isnull=True).update(location="")


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0029_delete_masterclass'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-date_time',), 'verbose_name': 'афиша', 'verbose_name_plural': 'афиша'},
        ),
        migrations.AlterModelOptions(
            name='reading',
            options={'ordering': ('-created',), 'verbose_name': 'специальное событие', 'verbose_name_plural': 'специальные события'},
        ),
        migrations.AddField(
            model_name='reading',
            name='custom_type',
            field=models.CharField(blank=False, max_length=200, null=False, verbose_name='Описание вида события', default="Читка"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='common_event',
            field=models.ForeignKey(help_text='Создайте спектакль или другое событие чтобы получить возможность создать соответствующее название', on_delete=django.db.models.deletion.CASCADE, related_name='body', to='afisha.commonevent', verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('PERFORMANCE', 'Спектакль'), ('CUSTOM', 'Специальное событие')], help_text='Выберите тип пункта афиши', max_length=50, verbose_name='Тип '),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='reading',
            name='events',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='custom', to='afisha.commonevent', verbose_name='События'),
        ),
        migrations.RunPython(reading_to_custom, custom_to_reading),
    ]
