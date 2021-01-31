# Generated by Django 3.0.8 on 2021-01-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='erfaring',
            options={'ordering': ['produksjon__premieredato', 'ar', 'verv__vtype', 'verv__erfaringsoverforing', 'verv__tittel', 'tittel', 'medlem__etternavn', 'navn'], 'verbose_name_plural': 'erfaringer'},
        ),
        migrations.AlterModelOptions(
            name='verv',
            options={'ordering': ['vtype', 'erfaringsoverforing', 'tittel'], 'verbose_name_plural': 'verv'},
        ),
        migrations.RemoveField(
            model_name='verv',
            name='erfaringsoverføring',
        ),
        migrations.AddField(
            model_name='verv',
            name='erfaringsoverforing',
            field=models.BooleanField(default=True, verbose_name='erfaringsoverføring'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anmeldelse',
            name='utdrag',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='arrangører',
            field=models.ManyToManyField(blank=True, to='SITdata.Verv'),
        ),
        migrations.AlterField(
            model_name='dokument',
            name='dtags',
            field=models.ManyToManyField(blank=True, related_name='dokumenttags', to='SITdata.dTag'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='medlemmer',
            field=models.ManyToManyField(blank=True, to='SITdata.Medlem'),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='opphavsar',
            field=models.IntegerField(blank=True, null=True, verbose_name='opphavsår'),
        ),
        migrations.AlterField(
            model_name='produksjon',
            name='ptags',
            field=models.ManyToManyField(related_name='produksjonstags', to='SITdata.pTag'),
        ),
        migrations.AlterField(
            model_name='verv',
            name='vtags',
            field=models.ManyToManyField(blank=True, related_name='vervtags', to='SITdata.vTag'),
        ),
    ]
