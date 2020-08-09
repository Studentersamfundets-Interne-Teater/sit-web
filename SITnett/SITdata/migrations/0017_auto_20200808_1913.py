# Generated by Django 3.0.8 on 2020-08-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0016_auto_20200808_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produksjon',
            options={'ordering': ['ptype', 'premiere'], 'verbose_name_plural': 'produksjoner'},
        ),
        migrations.RemoveField(
            model_name='produksjon',
            name='ar',
        ),
        migrations.RemoveField(
            model_name='produksjon',
            name='semester',
        ),
        migrations.AddField(
            model_name='produksjon',
            name='premiere',
            field=models.DateField(default='2020-01-01'),
            preserve_default=False,
        ),
    ]
