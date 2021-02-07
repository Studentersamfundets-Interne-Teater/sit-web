# Generated by Django 3.0.8 on 2021-02-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0009_auto_20210206_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dokument',
            name='dtags',
            field=models.ManyToManyField(blank=True, to='SITdata.dTag', verbose_name='dokumenttags'),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='ptags',
            field=models.ManyToManyField(blank=True, to='SITdata.pTag', verbose_name='produksjonstags'),
        ),
        migrations.AlterField(
            model_name='verv',
            name='vtags',
            field=models.ManyToManyField(blank=True, to='SITdata.vTag', verbose_name='vervtags'),
        ),
    ]