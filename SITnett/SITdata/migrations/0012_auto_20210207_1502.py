# Generated by Django 3.0.8 on 2021-02-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0011_auto_20210206_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrangement',
            name='arrangører',
        ),
        migrations.AddField(
            model_name='arrangement',
            name='arrangorer',
            field=models.ManyToManyField(blank=True, to='SITdata.Verv', verbose_name='arrangører'),
        ),
    ]
