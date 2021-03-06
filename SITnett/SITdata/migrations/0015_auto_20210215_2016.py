# Generated by Django 3.0.8 on 2021-02-15 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0014_auto_20210215_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produksjon',
            options={'ordering': ['-premieredato', 'tittel'], 'verbose_name_plural': 'produksjoner'},
        ),
        migrations.AddField(
            model_name='ar',
            name='gjengfoto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ar', to='SITdata.Foto'),
        ),
        migrations.AlterField(
            model_name='ar',
            name='forsidebilde',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='brukere', to='SITdata.Foto'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='fototype',
            field=models.IntegerField(choices=[(1, 'scene'), (2, 'kostyme'), (3, 'kulisse'), (4, 'arbeid'), (5, 'dalje'), (6, 'arrangement'), (7, 'gruppe'), (8, 'sosialt')]),
        ),
        migrations.AddField(
            model_name='foto',
            name='fotograf',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
