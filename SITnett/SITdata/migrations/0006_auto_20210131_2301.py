# Generated by Django 3.0.8 on 2021-01-31 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0005_auto_20210131_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anmeldelse',
            name='forfatter',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='anmeldelse',
            name='medium',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='varighet',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='dokument',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='erfaring',
            name='navn',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='erfaring',
            name='rolle',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='erfaring',
            name='tittel',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='hendelse',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='lokale',
            name='navn',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='etternavn',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='fornavn',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='jobb',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='kallenavn',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='mellomnavn',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='medlem',
            name='studium',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='nummer',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='varighet',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='sitat',
            name='kontekst',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sitat',
            name='tekst',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='uttrykk',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='verv',
            name='tittel',
            field=models.CharField(max_length=60),
        ),
    ]
