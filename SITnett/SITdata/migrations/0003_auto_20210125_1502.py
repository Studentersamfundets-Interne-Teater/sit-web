# Generated by Django 3.0.8 on 2021-01-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0002_auto_20210117_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produksjon',
            name='lokale',
        ),
        migrations.AddField(
            model_name='produksjon',
            name='lokale',
            field=models.ManyToManyField(related_name='produksjoner', to='SITdata.Lokale'),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='ptags',
            field=models.ManyToManyField(blank=True, related_name='produksjonstags', to='SITdata.pTag'),
        ),
    ]