# Generated by Django 3.0.8 on 2020-12-29 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrangement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atype', models.IntegerField(choices=[(1, 'internt'), (2, 'eksternt')], verbose_name='arrangementtype')),
                ('tittel', models.CharField(max_length=50)),
                ('tidspunkt', models.DateTimeField()),
                ('varighet', models.CharField(blank=True, max_length=22)),
                ('banner', models.ImageField(default='default/katter.png', upload_to='bannere/')),
                ('info', models.TextField(blank=True, verbose_name='beskrivelse (for eksterne)')),
                ('memo', models.TextField(blank=True, verbose_name='ytterligere anekdoter (for interne)')),
                ('blurb', models.TextField(blank=True, verbose_name='blurb (til forsida)')),
                ('blestestart', models.DateField(blank=True, null=True, verbose_name='blæstestart (på forsida)')),
                ('FBlink', models.CharField(blank=True, max_length=100, verbose_name='Facebook-link')),
            ],
            options={
                'verbose_name_plural': 'arrangementer',
                'ordering': ['tidspunkt', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='dTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'dTag',
                'verbose_name_plural': 'dTags',
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='Hendelse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittel', models.CharField(max_length=50)),
                ('dato', models.DateField()),
                ('beskrivelse', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'hendelser',
                'ordering': ['dato', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='Lokale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'lokaler',
                'ordering': ['navn'],
            },
        ),
        migrations.CreateModel(
            name='Medlem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.IntegerField(choices=[(1, 'SIT'), (2, 'Regi'), (3, 'FK'), (4, 'VK'), (5, 'SO'), (6, 'TSS'), (7, 'TKS'), (8, 'SPO'), (9, 'UKA'), (10, 'ISFiT'), (11, 'MG'), (12, 'ITK'), (13, 'ARK'), (14, 'FG'), (15, 'KSG'), (16, 'KU'), (17, 'KLST'), (18, 'LØK'), (19, 'DG'), (20, 'Profil'), (21, 'ekstern')], default=1, verbose_name='medlemstype')),
                ('fornavn', models.CharField(max_length=30)),
                ('mellomnavn', models.CharField(blank=True, max_length=30)),
                ('etternavn', models.CharField(max_length=30)),
                ('fodselsdato', models.DateField(blank=True, null=True, verbose_name='fødselsdato')),
                ('opptaksar', models.IntegerField(blank=True, null=True, verbose_name='opptaksår')),
                ('undergjeng', models.IntegerField(blank=True, choices=[(1, 'Kostyme'), (2, 'Kulisse'), (3, 'Skuespill')], null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'aktiv'), (2, 'veteran'), (3, 'pangsionist'), (4, 'inaktiv')], null=True)),
                ('portrett', models.ImageField(default='/default/katt.png', upload_to='portretter/')),
                ('kallenavn', models.CharField(blank=True, max_length=30)),
                ('telefon', models.CharField(blank=True, max_length=8, verbose_name='telefonnummer')),
                ('epost', models.EmailField(blank=True, max_length=60, verbose_name='e-postadresse')),
                ('studium', models.CharField(blank=True, max_length=30)),
                ('jobb', models.CharField(blank=True, max_length=30)),
                ('brukerkonto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'medlemmer',
                'ordering': ['mtype', 'opptaksar', 'undergjeng', 'etternavn', 'fornavn'],
            },
        ),
        migrations.CreateModel(
            name='pTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'pTag',
                'verbose_name_plural': 'pTags',
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='Uttrykk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittel', models.CharField(max_length=50)),
                ('beskrivelse', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'uttrykk',
                'ordering': ['tittel'],
            },
        ),
        migrations.CreateModel(
            name='vTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'vTag',
                'verbose_name_plural': 'vTags',
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='Verv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vtype', models.IntegerField(choices=[(1, 'styre'), (2, 'gjeng'), (3, 'produksjon')], verbose_name='vervtype')),
                ('tittel', models.CharField(max_length=50)),
                ('erfaringsoverføring', models.BooleanField()),
                ('instruks', models.TextField(blank=True)),
                ('beskrivelse', models.TextField(blank=True)),
                ('vtags', models.ManyToManyField(to='SITdata.vTag')),
            ],
            options={
                'verbose_name_plural': 'verv',
                'ordering': ['vtype', 'erfaringsoverføring', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='Utmerkelse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittel', models.IntegerField(choices=[(1, 'ridder'), (2, 'kommandør'), (3, 'storkors')])),
                ('orden', models.IntegerField(choices=[(1, 'Den Gyldne Kat'), (2, 'De Sorte Faars Ridderskab'), (3, 'Den Træge Patron'), (4, 'Polyhymnia'), (5, 'Vrangstrupen'), (6, 'Minerva Polyhymnia')], default=1)),
                ('ar', models.IntegerField(verbose_name='år')),
                ('medlem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utmerkelser', to='SITdata.Medlem')),
            ],
            options={
                'verbose_name_plural': 'utmerkelser',
                'ordering': ['ar', 'orden', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='Sitat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.TextField(max_length=100)),
                ('kontekst', models.CharField(max_length=50)),
                ('medlem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitater', to='SITdata.Medlem')),
            ],
            options={
                'verbose_name_plural': 'sitater',
            },
        ),
        migrations.CreateModel(
            name='Produksjon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptype', models.IntegerField(choices=[(1, 'SIT'), (2, 'KUP'), (3, 'AFEI'), (4, 'UKA')], default=1, verbose_name='produksjonstype')),
                ('tittel', models.CharField(max_length=50)),
                ('forfatter', models.CharField(max_length=100)),
                ('opphavsar', models.IntegerField(verbose_name='opphavsår')),
                ('premieredato', models.DateField()),
                ('varighet', models.CharField(blank=True, max_length=22)),
                ('banner', models.ImageField(default='/default/katter.png', upload_to='bannere/')),
                ('plakat', models.ImageField(blank=True, upload_to='plakater/')),
                ('opptak', models.FileField(blank=True, upload_to='opptak/')),
                ('program', models.FileField(blank=True, upload_to='programmer/')),
                ('manus', models.FileField(blank=True, upload_to='manus/')),
                ('partitur', models.FileField(blank=True, upload_to='partitur/')),
                ('visehefte', models.FileField(blank=True, upload_to='visehefter/')),
                ('info', models.TextField(blank=True, verbose_name='beskrivelse (for eksterne)')),
                ('memo', models.TextField(blank=True, verbose_name='ytterligere anekdoter (for interne)')),
                ('blurb', models.TextField(blank=True, verbose_name='blurb (til forsida)')),
                ('pris', models.IntegerField(blank=True, null=True, verbose_name='billettpris (for ikke-medlemmer)')),
                ('medlemspris', models.IntegerField(blank=True, null=True, verbose_name='billettpris (for medlemmer)')),
                ('billettlink', models.CharField(blank=True, max_length=100)),
                ('blestestart', models.DateField(blank=True, null=True, verbose_name='blæstestart (på forsida)')),
                ('FBlink', models.CharField(blank=True, max_length=100, verbose_name='Facebook-link')),
                ('lokale', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='produksjoner', to='SITdata.Lokale')),
                ('ptags', models.ManyToManyField(to='SITdata.pTag')),
            ],
            options={
                'verbose_name_plural': 'produksjoner',
                'ordering': ['premieredato', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='Nummer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittel', models.CharField(max_length=50)),
                ('opptak', models.FileField(blank=True, upload_to='opptak/')),
                ('tekst', models.TextField()),
                ('noter', models.FileField(blank=True, upload_to='noter/')),
                ('info', models.TextField(blank=True, verbose_name='beskrivelse (for eksterne)')),
                ('memo', models.TextField(blank=True, verbose_name='ytterligere anekdoter (for interne)')),
                ('produksjon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numre', to='SITdata.Produksjon')),
            ],
            options={
                'verbose_name_plural': 'numre',
                'ordering': ['produksjon__premieredato', 'tittel'],
            },
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ftype', models.IntegerField(choices=[(1, 'scene'), (2, 'kostyme'), (3, 'kulisse'), (4, 'arbeid'), (5, 'gruppe'), (6, 'arrangement'), (7, 'sosialt')], verbose_name='fototype')),
                ('dato', models.DateField(blank=True, null=True)),
                ('FGlink', models.CharField(blank=True, max_length=100, verbose_name='FG-link')),
                ('fil', models.ImageField(blank=True, upload_to='bilder/')),
                ('kontekst', models.TextField()),
                ('arrangement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bilder', to='SITdata.Arrangement')),
                ('medlemmer', models.ManyToManyField(to='SITdata.Medlem')),
                ('produksjon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bilder', to='SITdata.Produksjon')),
            ],
            options={
                'verbose_name_plural': 'fotoer',
                'ordering': ['ftype', 'produksjon__premieredato', 'arrangement__tidspunkt', 'dato'],
            },
        ),
        migrations.CreateModel(
            name='Forestilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tidspunkt', models.DateTimeField()),
                ('produksjon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forestillinger', to='SITdata.Produksjon')),
            ],
            options={
                'verbose_name_plural': 'forestillinger',
                'ordering': ['tidspunkt'],
            },
        ),
        migrations.CreateModel(
            name='Erfaring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(blank=True, max_length=50)),
                ('tittel', models.CharField(blank=True, max_length=50)),
                ('ar', models.IntegerField(blank=True, null=True, verbose_name='år')),
                ('rolle', models.CharField(blank=True, max_length=30)),
                ('skriv', models.FileField(blank=True, upload_to='erfaringsskriv/', verbose_name='erfaringsskriv')),
                ('medlem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='erfaringer', to='SITdata.Medlem')),
                ('produksjon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='erfaringer', to='SITdata.Produksjon')),
                ('verv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='erfaringer', to='SITdata.Verv')),
            ],
            options={
                'verbose_name_plural': 'erfaringer',
                'ordering': ['produksjon__premieredato', 'ar', 'verv__vtype', 'verv__erfaringsoverføring', 'verv__tittel', 'tittel', 'medlem__etternavn', 'navn'],
            },
        ),
        migrations.CreateModel(
            name='Dokument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittel', models.CharField(max_length=50)),
                ('dato', models.DateField()),
                ('fil', models.FileField(upload_to='dokumenter/')),
                ('dtags', models.ManyToManyField(to='SITdata.dTag')),
            ],
            options={
                'verbose_name_plural': 'dokumenter',
                'ordering': ['dato', 'tittel'],
            },
        ),
        migrations.AddField(
            model_name='arrangement',
            name='arrangører',
            field=models.ManyToManyField(to='SITdata.Verv'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='lokale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrangementer', to='SITdata.Lokale'),
        ),
        migrations.CreateModel(
            name='Anmeldelse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forfatter', models.CharField(max_length=50)),
                ('medium', models.CharField(max_length=50)),
                ('gratis', models.BooleanField()),
                ('fil', models.FileField(upload_to='anmeldelser/')),
                ('utdrag', models.TextField(blank=True)),
                ('produksjon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anmeldelser', to='SITdata.Produksjon')),
            ],
            options={
                'verbose_name_plural': 'anmeldelser',
                'ordering': ['produksjon__premieredato', 'forfatter'],
            },
        ),
    ]
