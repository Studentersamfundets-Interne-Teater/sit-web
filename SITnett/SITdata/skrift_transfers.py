import sys
# FYLL INN DIN LOKALE FILSTI TIL SITNETT HER:
#sys.path.append("/home/cassarossa/sit/web/sit-web-2020/SITnett")
sys.path.append("C:/Users/jonas/Documents/Kode/Django/sit-web/SITnett")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SITnett.settings")
import django
django.setup()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django_super_deduper.merge import MergedModelInstance

from SITdata import models, forms

from django.conf import settings
from bs4 import BeautifulSoup
import pdb
import datetime
import requests
import shutil

produksjonstype_dict = {'Radioteateret': ['radio', 'hørespill'], 'Ungdomsforestilling': ['ungdomsteater'], 'Ekstern statistjobb': ['eksternt', 'skildring'], 'Revykavalkade': ['revykavalkade', 'revy'], 'Musikal, 100 års jubileum': ['musikal', 'skildring'], 'Oppsetning': ['nei'], 'Ridderskapsmøte, 31 oktober': ['skildring'], 'sketsj': ['sketsj'], 'Revynummer': ['revynummer'], 'Improvisasjonsteater': ['improvisasjonsteater'], '16. mai-picnic': ['skildring'], 'Forestilling med eldre revynummer': ['revykavalkade', 'revy'], 'Eksternt arrangement': ['eksternt'], 'Dialog': ['dialog'], 'Storsalsteater': ['nei'], 'Revykafé': ['revykafé', 'UKA', 'revy'], 'Trikketeater': ['trikketeater'], 'parodi på Heibergs «Balkonen»': ['parodi', 'skildring'], 'Aperitiff, immatrikuleringsmøtet': ['aperitiff', 'skildring'], 'parodi': ['parodi'], 'Knausteateret': ['intimteater'], 'Teater': ['nei'], 'Musikal': ['musikal'], 'en-akter': ['enakter'], 'Aperitiff / Eksternt arrangement.': ['aperitiff', 'eksternt'], 'parodi på «Synnøve Solbakken»': ['parodi', 'skildring'], 'Aperitiff på immatrikuleringsmøtet': ['aperitiff', 'skildring'], 'Tre enaktere': ['enakter', 'skildring'], 'Tambateater': ['tambateater', 'UKA'], 'Improvisasjonshappening': ['improvisasjonsteater'], 'Nattforestilling': ['nattforestilling', 'UKA'], 'Kunsterisk': ['kunstnerisk'], 'Konsert': ['konsert'], 'Eksternt arrangement / Kunstnerisk': ['eksternt', 'kunstnerisk'], 'KUP-musikal': ['KUP', 'musikal'], 'UKE-revy': ['revy', 'UKA', 'UKErevy'], 'Aperitif': ['aperitiff'], 'Enakter': ['enakter'], 'Eksternt arrangement (?)': ['eksternt'], 'Aperitiff': ['aperitiff'], 'B-nummer': ['nei'], 'Rammemøte': ['skildring'], 'Intimteater - Komedie': ['intimteater', 'komedie'], 'Korverk med dans': ['kor', 'dans'], 'Revy': ['revy'], '3-akter': ['treakter'], 'Dukketeater': ['dukketeater'], 'Fysisk teater': ['fysisk teater'], 'Intimteater': ['intimteater'], 'operaparodi': ['opera', 'parodi'], 'Kunstnerisk': ['kunstnerisk'], 'Innslag på eksternt arrangement': ['eksternt'], 'KUP': ['KUP'], 'Barneteater': ['barneteater', 'UKA'], 'Lansering av jubileumsbok': ['skildring'], 'parodi på «Vårbrytning» av Wedekind': ['parodi', 'skildring'], 'parodi på «Pelikanen»': ['parodi', 'skildring'], 'Rocke-musikal': ['musikal', 'rock'], 'Dassteater': ['dassteater'], 'Innslag': ['nei'], 'kabaret': ['kabaret'], 'Turne': ['turné'], 'Kupping': ['KUP'], 'Intimrevy (kavalkade)': ['intimteater', 'revykavalkade', 'revy'], 'I regi av Kulturutvalget.': ['skildring'], 'aperitiff': ['aperitiff'], 'Bestlt AFEI til Lille-UKA': ['UKA', 'Lille-UKA', 'skildring'], 'Intimforestilling': ['intimteater'], 'Månedsrevy': ['revy', 'månedsrevy'], 'Eksternt arrangement / Kulturutvalget': ['eksternt', 'skildring'], 'AFEI': ['AFEI'], 'Devised intimteater for ISFiT-17': ['intimteater', 'ISFiT', 'skildring'], 'Studenterkomedie': ['komedie'], 'Jubileumsrevy, SIT 70 år': ['revy', 'revykavalkade', 'skildring'], 'Picnic': ['skildring'], 'B-nummer (føljetong)': ['nei'], 'Innslag, immatrikuleringsmøte': ['skildring'], 'ISFiT-teater': ['ISFiT'], 'Aperitiff?': ['aperitiff'], 'Radio': ['radio'], 'Radioprogram med Otto Nielsen': ['radio', 'skildring'], 'Ungdomsteater': ['ungdomsteater'], 'Kunstnerisk?': ['kunstnerisk']}


lokale_dict = {'SIT-hybelen': ['SIT-hybelen'], 'Buss': ['Eksternt', 'skildring'], 'Storsalsgulvet': ['Storsalen', 'skildring'],
               'Klubben, 8 forestilliniger': ['Klubben'],
               'Studentersamfundet': ['Diverse'], 'Selskapssiden/Strossa': ['Selskapssiden', 'Strossa'],
               'Kanalen': ['Eksternt', 'skildring'],
               'Hjorten': ['Eksternt', 'skildring'], 'Storesalen, lørdagsmøte': ['Storsalen'], 'Mediahuset': ['Eksternt', 'skildring'],
               'Over alt': ['Diverse'],
               'Venstervinds årsmøte': ['Eksternt', 'skildring'], 'Oslo Konsterthus': ['Eksternt', 'skildring'],
               'Trøndelag Teater': ['Eksternt', 'skildring'],
               'Haandværkeren': ['Eksternt', 'skildring'], 'Klæbu': ['Eksternt', 'skildring'], 'Gråkallen': ['Eksternt', 'skildring'],
               'All over the place': ['Diverse'],
               'Spisesalen (Edgar?)': ['Spisesalen'], 'NRK P2': ['Radio', 'skildring'], 'Biblioteket': ['Biblioteket'],
               'buss': ['Eksternt', 'skildring'],
               'På lerretet': ['Film'], 'Edgar, 8 forestillinger': ['Edgar'], 'Elgeseter gate 4': ['Eksternt', 'skildring'],
               'Cirkus': ['Cirkus'],
               'Bodegaen': ['Bodegaen'], 'Nors Revyfestival': ['Eksternt', 'skildring'],
               'Tunga kretsfengsel': ['Eksternt', 'skildring'],
               'Storsalen / Kvinneseksjonen i Faglig 1.-maifront': ['Storsalen', 'Eksternt', 'skildring'],
               'Edgar': ['Edgar'],
               'Sanfundet, Storsalen': ['Storsalen'], 'Klubben, 8 forestillinger': ['Klubben'],
               'Storsalen / ?': ['Storsalen'],
               'I friluft': ['Utendørs'], 'Der du minst forventer det': ['Diverse'], 'Samfundet': ['Diverse'],
               'Teaterbygningen Prinsens gate': ['Eksternt', 'skildring'], 'Storsalen, gulvet': ['Storsalen', 'skildring'],
               'Cirkus?': ['Cirkus'], 'Samfundet/Storsalen': ['Storsalen'],
               'Storsalen, 11 feb 61': ['Storsalen', 'skildring'], 'Levanger': ['Eksternt', 'skildring'], 'Kartdagene': ['Eksternt', 'skildring'],
               'Knaus': ['Knaus'], 'Reitgjerdet': ['Eksternt', 'skildring'],
               'Herretoalettet ved Rundhallen': ['Herretoalettet ved Rundhallen'],
               'Realistforeningen Oslo': ['Eksternt', 'skildring'], 'Bakscenen': ['Bakscenen'],
               'Knaus og fritidsklubber': ['Knaus', 'Eksternt', 'skildring'], 'Graakallbanen': ['Eksternt', 'skildring'],
               'Knaus / Radio Revolt': ['Knaus', 'Radio', 'skildring'], 'Storsalen, Samfundet': ['Storsalen'],
               'Sentrum Kino': ['Eksternt', 'skildring'], 'Studentersamfundet, 19.juni': ['Diverse'],
               'Edgar, 6 forestillinger': ['Edgar'], 'UKE-senderen': ['Radio', 'skildring'],
               'Tema88': ['Eksternt', 'skildring'], 'Daglighallen Pub': ['Daglighallen'], 'BUL': ['Eksternt'],
               'lørdagsmøte': ['Storsalen', 'skildring'], 'Sangerhallen': ['Sangerhallen'],
               'Samfundet, Storsalen': ['Storsalen'], 'Samfundet, Knus': ['Knaus'],
               'Estenstadmarka': ['Utendørs', 'skildring'], 'Overalt!': ['Diverse'], 'Bergen': ['Eksternt', 'skildring'],
               'Intimen': ['Eksternt', 'skildring'], 'Nidarøhallen': ['Nidarøhallen'], 'Selskapssiden++': ['Selskapssiden++'],
               'Fengselstomta': ['Fengselstomta'], 'Knaus + Scene 7 i Oslo': ['Knaus', 'Eksternt', 'skildring'],
               'Teltet i parken': ['Eksternt', 'skildring'],
               'Studentersamfundet/Ungdomsskoler': ['Diverse', 'Eksternt'], 'Kopirommet': ['Gjenganretningen'],
               'Storsalen, januar': ['Storsalen'], 'Storsalen, lørdagsmøte': ['Storsalen'],
               'Ble aldri satt opp': ['Diverse', 'skildring'], 'Palmehaven': ['Eksternt', 'skildring'],
               'Frimurerlogen': ['Eksternt', 'skildring'], 'Studentersamfundet, Storsalen': ['Storsalen'],
               'Storsalen 29 sep ': ['Storsalen'], 'Storsalen, 1 sep': ['Storsalen'],
               'Storsalen i Chateau Neuf': ['Eksternt', 'skildring'], 'Bodø': ['Eksternt', 'skildring'],
               'Samfindet, Storsalen': ['Storsalen'], 'Prinsen Hotell': ['Eksternt', 'skildring'],
               'storsalen': ['Storsalen'], 'Klubben': ['Klubben'], 'Storsalen, 4. desember': ['Storsalen'],
               'Sentrum': ['Eksternt', 'skildring'], 'Knaus ': ['Knaus'], 'Knaus, Storsalen': ['Knaus', 'Storsalen'],
               'Samfundet, Knaus': ['Knaus'], 'Ryttergangen': ['Ryttergangen'],
               'I store og små rom': ['Diverse'], 'Verdal': ['Eksternt', 'skildring'], 'Storsalen': ['Storsalen'],
               'Kunstindustrimuseet / Storsalen': ['Storsalen', 'Eksternt', 'skildring'],
               'Teaterbygningen i Prinsens gate': ['Eksternt', 'skildring'], 'Her og der': ['Diverse']}

verv_dict = {'Konsulent, lysreklamen': {0: "lysreklamist", 1: 'konsulent', 2:"annen prod"}, 'Konsulent, kostyme': {0: "kostymesyer", 1: 'konsulent', 2:"annen prod"},
             'Konsulent, kulisse': {0: "kulissebygger", 1: 'konsulent', 2:"annen prod"},'Konsulent, FFK': {0: "forfatter", 1: 'konsulent', 2:"annen prod"},
             'Lys, konsulent': {0: "lystekniker", 1: 'konsulent', 2:"annen prod"}, 'Lyd, myggkonsulent':{0: "lydtekniker", 1: 'konsulent', 2:"annen prod"},
             'Lyd, konsulent': {0: "lydtekniker", 1: 'konsulent', 2:"annen prod"}, 'Skuespiller, Guest Star': {0: 'skuespiller', 1:"guest star", 2:"annen prod"},
             'input': {0: 'verv', 1: 'rolle', 2: 'type'}, 'Sjåfør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
             'Musikalsjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, 'KUPer': {0: 'KUPer', 1: 'ingen', 2: 'annen prod'},
             'Scenografkonsulat': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
             'Bandleder': {0: 'musiker', 1: 'kapellmester', 2: 'annen prod'},
             'Leder forfatterkollegiet': {0: 'forfatter', 1: 'leder', 2: 'annen prod'},
             'Lys': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'konsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
             'UKE-lege': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Danser': {0: 'danser', 1: 'ingen', 2: 'annen prod'},
             'Markedsføring': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Fotograf': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kullisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'MedKUPkoordinator': {0: 'produsent', 1: 'assistent', 2: 'prodapp'}, 'Scenografiansvarlig': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'}, 'Lysreklamekonsulent': {0: 'lysreklamist', 1: 'konsulent', 2: 'annen prod'}, 'Kost- og losjiansvarlig': {0: 'forpleier', 1: 'leder', 2: 'annen prod'}, 'Kulissesjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Dotcom': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Bandet': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Lydbrigader': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'}, 'Lyddesigner': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'}, 'Trine Skei Grande': {0: 'skuespiller', 1: 'Trine Skei Grande', 2: 'annen prod'}, 'Konsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'kulisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Cocktailsyer': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Koreografassistent': {0: 'koreograf', 1: 'assistent', 2: 'prodapp'}, 'Lysdesigner': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'}, 'Filmarbeider': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Regi-ass.': {0: 'regissør', 1: 'assistent', 2: 'prodapp'}, 'Musikksnupp': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Uspesifisert': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sufflør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'LYD': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'}, 'Instruktør ': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Visedirektør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Konsulenter lys': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'}, 'FFK-koordinator': {0: 'forfatter', 1: 'forfatterkollegieleder', 2: 'annen prod'}, 'Sminkør': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Kulissearbeidsleder': {0: 'kulissebygger', 1: 'arbeidsleder', 2: 'annen prod'}, 'Musiker': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Produksjonsdesigner': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymeassistent': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kulissearbeider': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Kulissebygger': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Lydansvarlig': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'}, 'Sypike': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Musikk': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Oberst': {0: 'oberst', 1: 'ingen', 2: 'prodapp'}, 'Blondiekomiteen': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'VK-revy': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Regiassistent': {0: 'regissør', 1: 'assistent', 2: 'prodapp'}, 'Instruktør/forfatter': {0: 'Regissør/Forfatter', 1: 'ingen', 2: 'prodapp'}, 'Festivalstyret': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Skodespelar': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'}, 'Orkesterinspisient': {0: 'musikalsk inspisient', 1: 'ingen', 2: 'prodapp'}, 'Ukelege': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'undefined': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Plakat / Program / Tegning': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'}, 'instruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Kostyme': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Sminkeassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'}, 'Videotekniker': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'}, 'Fittingsassistent': {0: 'fittings', 1: 'assistent', 2: 'annen prod'}, 'Skuespiller/manus': {0: 'Skuespiller/Forfatter', 1: 'ingen', 2: 'annen prod'}, 'Teknisk inspisient': {0: 'teknisk inspisient', 1: 'ingen', 2: 'prodapp'}, 'Barneteatersjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, '17 mai': {0: 'KUPer', 1: '17. mai', 2: 'annen prod'}, 'Lyssnupp': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Iscenesetter': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sminkeansvarlig': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Publikumsverter': {0: 'publikumsvert', 1: 'ingen', 2: 'annen prod'}, 'Guest 1.assistant director': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lysansvarlig': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'}, 'Følgespotsjef': {0: 'lystekniker', 1: 'følgespot', 2: 'annen prod'}, 'Program': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Leif Ronny': {0: 'skuespiller', 1: 'Leif Ronny', 2: 'annen prod'}, 'Kontentum': {0: 'lyddesigner', 1: 'kontentum', 2: 'prodapp'}, 'NM-ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Komponister': {0: 'komponist', 1: 'ingen', 2: 'prodapp'}, 'Forfatterkollegiekoordinator': {0: 'forfatter', 1: 'leder', 2: 'annen prod'}, 'Regi-assistent': {0: 'regissør', 1: 'assistent', 2: 'prodapp'}, 'Insruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Band (Berits venner)': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Suppelyd': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'}, 'Hår- og sminkestylist': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Scenograf og kostymedesigner': {0: 'Scenograf/Kostymedesigner', 1: 'ingen', 2: 'ingen'}, 'Billettansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Teatersjef/revysjef': {0: 'Teatersjef/Produsent', 1: 'ingen', 2: 'prodapp'}, 'Video v/VK': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Frisør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Forfatterkollegiet': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'}, 'Skuespiller og musiker': {0: 'Skuespiller/Musiker', 1: 'ingen', 2: 'annen prod'}, 'Lys.1': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Funksjonær': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kursholder': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kulissebygger/scenearbeider': {0: 'Kulissebygger/Scenearbeider', 1: 'ingen', 2: 'annen prod'}, 'ISFiT ledervalg': {0: 'KUPer', 1: 'ISFiT ledervalg', 2: 'annen prod'}, 'Lydkonsulent': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'}, 'Markedsfører og billettansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Grafisk designer': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Trener': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lys ved Regi': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Orkestersjef v/musikerlåfte': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Revysjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, 'Inspisientassistent': {0: 'inspisient', 1: 'assistent', 2: 'prodapp'}, 'Lysreklamesjef': {0: 'lysreklamist', 1: 'leder', 2: 'annen prod'}, 'Dramaturg': {0: 'dramaturg', 1: 'ingen', 2: 'annen prod'}, 'Video v/ARK': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Konsulent.1': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Forfatterkollegieleder': {0: 'forfatter', 1: 'leder', 2: 'annen prod'}, 'Hår- og sminkeassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'}, 'Manuskript': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'}, 'Helseansvarlig': {0: 'helseansvarlig', 1: 'ingen', 2: 'prodapp'}, 'Kostymedesigner': {0: 'kostymedesigner', 1: 'ingen', 2: 'prodapp'}, 'Skuespiller/forfatter': {0: 'Skuespiller/Forfatter', 1: 'ingen', 2: 'ingen'}, 'Animatør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Videokonsulent': {0: 'videotekniker', 1: 'konsulent', 2: 'annen prod'}, 'Fysisk trener': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Gnark': {0: 'skuespiller', 1: 'gnark', 2: 'annen prod'}, 'Kulissegjengen': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Lyd': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'}, 'Arbeidsleder': {0: 'kulissebygger', 1: 'arbeidsleder', 2: 'annen prod'}, 'Suppesnupp': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Medinstruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Forpleiningsansvarlig': {0: 'forpleier', 1: 'ingen', 2: 'annen prod'}, 'Lysreklameansvarlig': {0: 'lysreklamist', 1: 'leder', 2: 'annen prod'}, 'Garderobeslusk': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Konsulent i Lysreklamen': {0: 'lysreklamist', 1: 'konsulent', 2: 'annen prod'}, 'Scenograf ': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'}, 'Band': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Myggslusk': {0: 'myggslusk', 1: 'ingen', 2: 'annen prod'}, 'ULYD': {0: 'lydtekniker', 1: 'uLYD', 2: 'annen prod'}, 'Ein slags regi': {0: 'regissør', 1: 'en slags', 2: 'prodapp'}, 'Forfatterkollegiekonsulent': {0: 'forfatter', 1: 'konsulent', 2: 'annen prod'}, 'Sanger': {0: 'sanger', 1: 'ingen', 2: 'annen prod'}, 'Konsulent lys': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'}, 'Lydsnupp': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'}, 'MEDlyd': {0: 'lydtekniker', 1: 'MedLYD', 2: 'annen prod'}, 'Gjesteartist': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Rekvisitørassistent': {0: 'rekvisitør', 1: 'assistent', 2: 'annen prod'}, 'Komponistkollegieleder': {0: 'komponist', 1: 'leder', 2: 'prodapp'}, 'Korrektur': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Seremoniregissør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sang': {0: 'sanger', 1: 'ingen', 2: 'annen prod'}, 'Komponistkollegiet': {0: 'komponist', 1: 'ingen', 2: 'prodapp'}, 'PR': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lyd.1': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'}, 'konsulent.1': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Helseansvarlig/trener': {0: 'helseansvarlig', 1: 'ingen', 2: 'prodapp'}, 'Lys v/Regi': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'}, 'Kostymetegner': {0: 'kostymesyer', 1: 'arbeidsleder', 2: 'annen prod'}, 'Oversetter': {0: 'oversetter', 1: 'ingen', 2: 'prodapp'}, 'VIdeo': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Medlyd': {0: 'lydtekniker', 1: 'MedLYD', 2: 'annen prod'}, 'Kulissekonsulent': {0: 'kulissebygger', 1: 'konsulent', 2: 'annen prod'}, 'Layout': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lyssnopp': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Lyd v. FK': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lysreklamist': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'}, 'KUPkoordinator': {0: 'produsent', 1: 'KUPkoordinator', 2: 'prodapp'}, 'FK': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'}, 'Videokunster': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Scenograf/Rekvisitør': {0: 'Scenograf/Rekvisitør', 1: 'ingen', 2: 'prodapp'}, 'inspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'}, 'Kostymehospitant': {0: 'kostymesyer', 1: 'hospitant', 2: 'annen prod'}, 'Administrativ assistanse': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sminke- og hårassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'}, 'Suppedirektør': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, 'Cocktailarbeidsleder': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lyd v/FK': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'}, 'Suppelys': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Sminkørassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'}, 'Konsulenter lyd': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'}, 'SIT Revy': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Billett-, økonomi- og sikkerhetsansvarlig': {0: 'Økonomiansvarlig/Billettansvarlig/Sikkerhetsansvarlig', 1: 'ingen', 2: 'prodapp'}, 'Sikkerhetsansvarlig': {0: 'sikkerhetsansvarlig', 1: 'ingen', 2: 'annen prod'}, 'Teatersjef': {0: 'teatersjef', 1: 'ingen', 2: 'styret'}, 'Designkonsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'SIT Blæst': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Forfatter og skuespiller': {0: 'Forfatter/Skuespiller', 1: 'ingen', 2: 'annen prod'}, 'Piano': {0: 'musiker', 1: 'piano', 2: 'annen prod'}, 'Sangteknisk instruksjon': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'}, 'Instuktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Kostymeoberst': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'}, 'Forpleiningssjef': {0: 'forpleier', 1: 'leder', 2: 'annen prod'}, 'Publikumsvert': {0: 'publikumsvert', 1: 'ingen', 2: 'annen prod'}, 'Konsulent Lyslaget': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'}, 'Skjermbilde': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Grafisk design': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'UKEsjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'SIT styret': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Deltaker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sang-instruktør': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'}, 'Manusbearbeidelse': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Bygdefolk': {0: 'statist', 1: 'ingen', 2: 'annen prod'}, 'CD': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Performance på Husfest': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sminke- og hårstylist': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Fittings': {0: 'fittings', 1: 'ingen', 2: 'annen prod'}, 'Kulisser': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymesjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Rekvisitør': {0: 'rekvisitør', 1: 'ingen', 2: 'annen prod'}, 'Repetitør': {0: 'repetitør', 1: 'ingen', 2: 'annen prod'}, 'Rekvisittassistent': {0: 'rekvisitør', 1: 'assistent', 2: 'annen prod'}, 'Markedsfører': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Illustratør': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'}, 'Orkestersjef': {0: 'musiker', 1: 'kapellmester', 2: 'annen prod'}, 'Videomester': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'}, 'Festtale': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lydeffekter': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'}, 'Administrasjon': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Medvirkende': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymemaker': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Økonomiansvarlig': {0: 'økonomiansvarlig', 1: 'ingen', 2: 'prodapp'}, 'Konsulent.2': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'kostyme': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Stemme på intervju': {0: 'skuespiller', 1: 'stemme på intervju', 2: 'annen prod'}, 'Masker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Dirigent': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymesyer': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Oversettelse': {0: 'oversetter', 1: 'ingen', 2: 'prodapp'}, 'Lyddesign': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'}, 'Suppesnuppe': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymekonsulent': {0: 'kostymesyer', 1: 'konsulent', 2: 'annen prod'}, 'Sminke': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Materialforvalter orkester': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Hospitant': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Festdeltaker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Komponist': {0: 'komponist', 1: 'ingen', 2: 'prodapp'}, 'Scenograf': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'}, 'Kostymeslusk': {0: 'kostymeslusk', 1: 'ingen', 2: 'annen prod'}, 'Teknisk Inspisient': {0: 'Teknisk Inspisient', 1: 'ingen', 2: 'prodapp'}, 'Sceneteknikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Komponistkonsulent': {0: 'komponist', 1: 'konsulent', 2: 'prodapp'}, 'Ymse': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sangpedagog og repetitør': {0: 'Sangpedagog/Repetitør', 1: 'ingen', 2: 'prodapp'}, 'Tribuneansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'skuespiller': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'}, 'Kommentator': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Statist': {0: 'statist', 1: 'ingen', 2: 'annen prod'}, 'Pianist': {0: 'musiker', 1: 'piano', 2: 'annen prod'}, 'Lystekniker': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Kunstnerisk koordinator': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Instruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Kulissegjeng': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Konsulent.3': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'lysreklamen': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'}, 'Produksjonsassistent': {0: 'produsent', 1: 'assistent', 2: 'prodapp'}, 'Manus': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'}, 'Regissør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'}, 'Sangpedagog': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'}, 'Suppesnupp/-snopp': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Produksjonsansvarlig': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, 'Orkesterleder': {0: 'musiker', 1: 'kapellmester', 2: 'annen prod'}, 'Sekretær': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Koreograf': {0: 'koreograf', 1: 'ingen', 2: 'prodapp'}, 'Revyorkester': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Skuespillerinspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'}, 'Rekvisittansvarlig': {0: 'rekvisitør', 1: 'ingen', 2: 'annen prod'}, 'Kostymekoordinator': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'}, 'Musikksnopp': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Kostymegjeng': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Forpleiningsassistent': {0: 'forpleier', 1: 'assistent', 2: 'annen prod'}, 'Turneleder': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Konsulent video': {0: 'videotekniker', 1: 'konsulent', 2: 'annen prod'}, 'Nød-bærehjelp i tolvte time': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lydsnopp': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'}, 'Lydig': {0: 'lydtekniker', 1: 'LYDig', 2: 'annen prod'}, 'Lysbilder v/FG': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymearbeidsleder': {0: 'kostymesyer', 1: 'arbeidsleder', 2: 'annen prod'}, 'Forteller': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Butler': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Grafikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Ouvreuse': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'PR-ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lyslaget': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}, 'Økonomi': {0: 'økonomiansvarlig', 1: 'ingen', 2: 'prodapp'}, 'Scenearbeider': {0: 'scenearbeider', 1: 'ingen', 2: 'annen prod'}, 'Plakat': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'}, 'Slåssteknikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Skuespiller': {0: 'skuespiller', 1: '(Guest Star)', 2: 'annen prod'}, 'Smikør': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Rekvisitørkonsulent': {0: 'rekvisitør', 1: 'konsulent', 2: 'annen prod'}, 'Følgespotlaget': {0: 'lystekniker', 1: 'følgespot', 2: 'annen prod'}, 'Videografiker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'myggkonsulent': {0: 'myggslusk', 1: 'konsulent', 2: 'annen prod'}, 'Videolaget': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'}, 'Nestleder': {0: 'nestleder', 1: 'ingen', 2: 'styret'}, 'Videokomiteen': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'}, 'Oversetter/instruktør/produsent': {0: 'Oversetter/Regissør/Produsent', 1: 'ingen', 2: 'prodapp'}, 'Koreografisk ass.': {0: 'koreograf', 1: 'assistent', 2: 'prodapp'}, 'Stemmepedagog': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'}, 'FFK': {0: 'forfatter', 1: 'konsulent', 2: 'annen prod'}, 'Innbildt suppedirektør': {0: 'produsent', 1: 'innbilt', 2: 'prodapp'}, 'Skuespiller ': {0: 'skuespiller ', 1: 'ingen', 2: 'annen prod'}, 'Musikalsk ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Konferansier': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Inspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'}, 'Eva Person': {0: 'skuespiller', 1: 'Eva Person', 2: 'annen prod'}, 'Musikalsk leder': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kulissesnekker': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Instruktørveileder': {0: 'regissør', 1: 'konsulent', 2: 'prodapp'}, 'Kommandør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymekommandør': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'}, 'Kostymesyere': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Sminke/parykk': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'}, 'Orkesteret': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Noteskriver': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Film': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Publikumsinspisient': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Orkester': {0: 'musiker', 1: 'ingen', 2: 'annen prod'}, 'Forfatter': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'}, 'Kostymeskredder': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Pr-gjeng': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kulisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'}, 'Produsentassistent': {0: 'produsent', 1: 'assistent', 2: 'prodapp'}, 'Musikkarrangement': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Diverse': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymegjengen': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Systemtekniker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Suppesnopp': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymer': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'}, 'Verkstedansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lysreklamen': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'}, 'Video': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'}, 'Regiveileder': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'}, 'Byfolk': {0: 'statist', 1: 'ingen', 2: 'annen prod'}, 'Arrangementskomité': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lysmester': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'}, 'Jazz på dass': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Personal- og innkjøpsansvarlig - kostyme': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Artist': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Lyskonsulent': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'}, 'Kapellmester': {0: 'musiker', 1: 'kapellmester', 2: 'annen prod'}, 'Produksjonskonsulent': {0: 'produsent', 1: 'konsulent', 2: 'prodapp'}, 'Dovrefarer': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Regi': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Bilderedaktør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kupper': {0: 'KUPer', 1: 'ingen', 2: 'annen prod'}, 'Lys- og sceneinspisient': {0: 'teknisk inspisient', 1: 'ingen', 2: 'prodapp'}, 'Jørgen Person': {0: 'skuespiller', 1: 'Jørgen Person', 2: 'annen prod'}, 'Direktør': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Produsent': {0: 'produsent', 1: 'ingen', 2: 'prodapp'}, 'Skuespillere': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'}, 'Gjendiktning sangtekster': {0: 'gjendikter', 1: 'ingen', 2: 'annen prod'}, 'VK': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'}, 'Plakattegner': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'}, 'Forpleining': {0: 'forpleier', 1: 'ingen', 2: 'annen prod'}, 'Skuespiller.1': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'}, 'Lyslag': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}}



def replace_empty_tags(location):
    file = open(location, 'r')
    lines = file.readlines()
    i = 0
    while i < len(lines):
        b = lines[i].find("><")
        print(lines[i])
        if b != -1:
            lines.pop(i)
        else:
            i += 1

    a_file = open(location, "w")
    a_file.writelines(lines)
    a_file.close()


def getMedlemDict(location):
    soup = BeautifulSoup(open(location), features="lxml")
    # print(soup.prettify())
    data_dict = {}
    for tag in soup.find_all():
        try:
            tag_name = tag.name
            tag_str = tag.string
            data_dict[tag_name] = tag_str
        except:
            continue
    try:
        navn = data_dict['etternamn']
    except:
        if open(location, 'r').readlines().index('%>') < 5:
            return data_dict
        replace_empty_tags(location)
        return getMedlemDict(location)

    try:
        navn = data_dict['fornamn']
    except:
        if location.count("_") > 1:
            fornavn = location[(location.find("_") + 1):location.find("_", location.find("_") + 1)]
        else:
            fornavn = location[(location.find("_") + 1):-4]

        fornavn_lst = list(fornavn)
        for i in range(len(fornavn_lst)):
            if fornavn_lst[i] == 'ø':
                fornavn_lst[i] = 'å'
            elif fornavn_lst[i] == 'å':
                fornavn_lst[i] = 'ø'

        fornavn = "".join(fornavn_lst)

        data_dict['fornamn'] = fornavn.title()

    return data_dict


def getForestillingDict(location):
    f = open(location)
    soup = BeautifulSoup(f, features="lxml")


    # print(soup.prettify())
    data_dict = {}
    for tag in soup.find_all():
        try:
            tag_name = tag.name
            if tag_name == 'sidetekst':
                tag_str = str(tag)
            else:
                tag_str = tag.string
            data_dict[tag_name] = tag_str
        except:
            continue

    tekst = f.read()
    data_dict['produksjonsnamn'] = tekst[tekst.find('produksjonsnamn')+16:tekst.find('</produksjonsnamn')]
    if data_dict['produksjonsnamn']== "":
        data_dict['produksjonsnamn'] = data_dict['overskrift']

    # print(data_dict)
    return data_dict


def getAll(location, type='medlem'):
    directory = os.fsencode(location)
    list_of_dicts = []
    errors = []
    for file in os.listdir(directory):
        filename = location + os.fsdecode(file)
        try:
            if type == 'forestilling':
                list_of_dicts.append(getForestillingDict(filename))
            elif type == 'medlem':
                list_of_dicts.append(getMedlemDict(filename))
        except:
            errors.append(filename)
            continue
    # print(list_of_dicts)
    dict_of_lists = {}
    for i in range(len(list_of_dicts)):
        for key, value in list_of_dicts[i].items():
            try:
                dict_of_lists[key].append(value)
            except:
                dict_of_lists[key] = [value]
    dict_of_sets = dict_of_lists
    for key, value in dict_of_sets.items():
        dict_of_sets[key] = set(value)
        print(key, len(dict_of_sets[key]))
        print(dict_of_sets[key])

    return list_of_dicts, dict_of_lists, dict_of_sets, errors


def check_data(medlem=True, forestilling=False):
    if medlem:
        m_list_of_dicts, m_dict_of_lists, m_dict_of_sets, m_errors = getAll("/Users/jacob/Desktop/Fra skrift/medlem/",
                                                                            'medlem')
        print(m_dict_of_lists.keys())

    if forestilling:
        f_list_of_dicts, f_dict_of_lists, f_dict_of_sets, f_errors = getAll(
            "/Users/jacob/Desktop/Fra skrift/forestilling/")

        verv_set = set({})

        for key, values in f_dict_of_sets.items():
            if key[:4] == 'verv':
                verv_set = verv_set.union(set(values))

        print(f_dict_of_lists.keys())


def create_medlem(medlem_dict, arr_for_bilder, location):
    fornavn = try_get2('fornamn', medlem_dict, '')
    if fornavn == '':
        return
    mellomnavn = try_get2('mellomnamn', medlem_dict, '')
    etternavn = try_get2('etternamn', medlem_dict, '')
    studium = try_get2('studerer', medlem_dict, '')

    fodselsdato = hent_fodsel(medlem_dict)

    opptaksar = try_get2('opptak_aar', medlem_dict)

    # ['fodt_dto', 'fodt_mnd', 'fodt_aar', 'gjeng', 'status', 'opptak_aar', 'e_post', 'mobil', 'foto', 'dgk_ridder']

    telefon = try_get2('mobil', medlem_dict, '').replace(" ", "")
    kallenavn = try_get2('tidligare_namn', medlem_dict, '')

    epost = ''
    try:
        epost = medlem_dict['e_post'].replace(" (a) ", "@")
        epost.replace("(a)", "@")
        epost.replace("(a)", "@")
    except:
        pass

    medlemstype = 1
    undergjeng = None
    gjeng_medlemstype_dict = {'skuespiller': 1, 'Regi': 2, 'Kostyme': 1, 'Ekstern': 21, 'UKE-funk': 9, 'UKEfunk/Låftet': 5,
                        'Kulisse': 1, 'Skuespiller': 1}
    gjeng_undergjeng_dict = {'skuespiller': 3, 'Kostyme': 1, 'Kulisse': 2, 'Skuespiller': 3}
    try:
        medlemstype = gjeng_medlemstype_dict[medlem_dict['gjeng']]
        if medlemstype == 1:
            undergjeng = gjeng_undergjeng_dict[medlem_dict['gjeng']]
    except:
        pass

    status = 3
    status_dict = {'skuespiller': 1, 'Prangsjonist': 3, 'UKEfunk': None, 'Forlatt SIT': 4, 'Pangsjonisr': 3,
                   'Ekstern': None, 'Aktiv': 1, 'Permisjon': 4, 'Veteran': 2, 'Pang': 3, 'Pangsjonist': 3,
                   'pangsjonist': 3}
    # STATUSER = ((1,'aktiv'),(2,'veteran'),(3,'pangsionist'),(4,'inaktiv'))
    try:
        status = status_dict[medlem_dict['status']]
        if medlem_dict['status'] == 'skuespiller':
            undergjeng = 3
    except:
        pass

    portrett = '/default/katt.png'
    try:
        url = medlem_dict['foto']
        r = requests.get(url, allow_redirects=True, stream=True)
        fname = url.split("/")[-1]
        if r.status_code == 200:
            shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/portretter/' + fname, 'wb'))
            portrett = '/portretter/' + fname
    except:
        pass

    new_medlem = models.Medlem(medlemstype=medlemstype, fornavn=fornavn, mellomnavn=mellomnavn, etternavn=etternavn,
                               fodselsdato=fodselsdato,
                               opptaksar=opptaksar, undergjeng=undergjeng, status=status, portrett=portrett,
                               telefon=telefon,
                               epost=epost, studium=studium, kallenavn=kallenavn)
    new_medlem.save()

    create_utmerkelser(medlem_dict, new_medlem)

    update_gallery(medlem_dict, new_medlem, arr_for_bilder, location)

    print(new_medlem)


def hent_fodsel(medlem_dict):
    try:
        f_aar = medlem_dict['fodt_aar']
        if len(f_aar) < 4:
            f_aar = '19' + f_aar

        try:
            f_mnd = medlem_dict['fodt_mnd']
            if f_mnd[0] == '0':
                f_mnd = int(f_mnd[-1])
        except:
            f_mnd = 6
        try:
            f_dto = medlem_dict['fodt_dto']
            if f_dto[0] == '0':
                f_dto = int(f_dto[-1])
        except:
            f_dto = 15

        return datetime.date(int(f_aar), int(f_mnd), int(f_dto))
    except:
        return None


def create_utmerkelser(medlem_dict, new_medlem):
    try:
        ridder_ar = medlem_dict['dgk_ridder']
        utmerkelser = [models.Utmerkelse(tittel=1, orden=1, ar=ridder_ar, medlem=new_medlem)]
        try:
            kommandor_ar = medlem_dict['dgk_kommandor']
            utmerkelser.append(models.Utmerkelse(tittel=2, orden=1, ar=kommandor_ar, medlem=new_medlem))
            try:
                storkors_ar = medlem_dict['dgk_storkors']
                utmerkelser.append(models.Utmerkelse(tittel=3, orden=1, ar=storkors_ar, medlem=new_medlem))
            except:
                pass
        except:
            pass
        for utmerkelse in utmerkelser:
            utmerkelse.save()
    except:
        pass


def update_gallery(medlem_dict, new_medlem, arr, location):
    # print(medlem_dict)
    for key, value in medlem_dict.items():
        if key[:8] == 'galleri_':
            try:
                kontekst = produksjon_dict[key.replace('_', 'txt_')]
            except:
                kontekst = ""
            url = value.replace("""\\""", "/")
            fname = url.split("/")[-1]
            try:
                old_foto = models.Foto.objects.get(fil='/bilder/' + fname, kontekst=kontekst)
                old_foto.medlemmer.add(new_medlem)
            except:
                try:
                    r = requests.get(url, allow_redirects=True, stream=True)
                    shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                except:
                    shutil.copyfileobj(open(location + url, 'rb'),
                                       open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                fil = '/bilder/' + fname
                new_foto = models.Foto(fil=fil, kontekst=kontekst, arrangement=arr, fototype=1)
                new_foto.save()
                new_foto.medlemmer.add(new_medlem)
                new_foto.save()


def create_produksjon(data_dict, location):
    # 'p'- div tekst, sjekk om det er i sidetekst et sted --> info
    # 'semester' - semester, --> premieredato
    # 'aar'- år satt opp, --> premieredato
    # 'overskrift' - overskrift på siden, vanligvis det samme som produksjonsnavnet --> info?
    # 'sidetekst' - mesteparten av innholdet på siden, -->info
    # 'a'- sjekk om det er i sidetekst, -->info
    # 'b' - sjekk om det er i sidetekst, -->info
    # 'skildring' - kort beskrivelse av forestillingen, -->info
    # 'spelestad' - spillested, mye forskjellig her --> create lokale og link til forestillingen
    # 'opphavsmenn' - forfatter(e), replace "av " --> forfatter
    # 'uka' - ukeproduksjon? ja hvis tagen fins --> produksjonstype = 4
    # 'plakat' - plakat(bildelink) --> plakat
    # 'galleri_i' og 'galleritxt_i' --> lag Foto og link til produksjonen
    # 'verv_i', 'person_i' + 'karakter_i' --> lag erfaring knyttet til medlem og produksjon, lag medlem om medlem ikke finnes, bruk dict for å få riktige verv
    # 'produksjonstype' lag produksjonstags, kjør gjennom filter, inneholder også AFEI og KUP --> produksjonstype, enkelte kan kanskje gå som skildring også
    # 'produksjonsnamn' - kommer ikke med, men det er egentlig her tittel ligger -->tittel

    tittel = try_get2('produksjonsnamn', data_dict, "Ikke funnet")
    forfatter = try_get2('opphavsmenn', data_dict, "Ikke funnet").replace("av ","")

    try:
        if data_dict['semester'] in {'Hosø', 'Hørt', 'høst', 'Høst'}:
            premieredato = datetime.date(int(data_dict['aar']), 3, 1)
        else:
            premieredato = datetime.date(int(data_dict['aar']), 10, 1)
    except:
        premieredato = datetime.date(int(data_dict['aar']), 7, 1)

    produksjonstype = 0
    produksjonstag_list = []
    lokale_list = []

    info = ""
    info += try_get('overskrift', data_dict)

    try:
        produksjonstype_is_skildring, produksjonstype, produksjonstag_list = create_produksjonstags(produksjonstype_dict[data_dict['produksjonstype']])
        if produksjonstype_is_skildring:
            info += try_get('produksjonstype', data_dict)
    except:
        pass

    try:
        lokale_is_skildring, lokale_list = create_lokale(lokale_dict[data_dict['spelestad']])
        if lokale_is_skildring:
            info += try_get('spelestad', data_dict)
    except:
        pass

    try:
        a = data_dict['uka']
        produksjonstype = 4
    except:
        if produksjonstype == 0:
            produksjonstype = 1


    info += try_get('skildring', data_dict)

    info += try_get('sidetekst', data_dict)

    info += check_sidetekst('p', data_dict)

    info += check_sidetekst('a', data_dict)

    info += check_sidetekst('b', data_dict)


    try:
        if data_dict['produksjonstype'] == 'UKE-revy' and forfatter == "Ikke funnet":

            forfatter = "Forfatterkollegiet"
    except:
        pass

    plakat = None
    try:
        url = data_dict['plakat']
        r = requests.get(url, allow_redirects=True, stream=True)
        fname = url.split("/")[-1]
        if r.status_code == 200:
            shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/portretter/' + fname, 'wb'))
            plakat = '/plakater/' + fname
    except:
        pass

    new_produksjon = models.Produksjon(tittel=tittel, forfatter=forfatter, premieredato=premieredato, plakat=plakat, info=info)
    new_produksjon.save()

    if produksjonstag_list:
        for produksjonstag in produksjonstag_list:
            new_produksjon.produksjonstags.add(produksjonstag)
    if lokale_list:
        for lokale in lokale_list:
            new_produksjon.lokale.add(lokale)

    banner = update_produksjon_gallery(data_dict, new_produksjon, location)
    new_produksjon.banner = banner
    new_produksjon.save()
    create_erfaringer(data_dict, new_produksjon)
    print(new_produksjon)

def try_get2(data, data_dict, default=None):
    try:
        return data_dict[data]
    except:
        return default


def try_get(data, data_dict):
    try:
        return data + ":    " + data_dict[data] + "\n\n"
    except:
        return data + ":    " + "\n\n"

def create_produksjonstags(p_list):
    is_skildring = False
    produksjonstype = 0
    produksjonstag_list = []
    for tag in p_list:
        if tag == 'skildring':
            is_skildring = True
        elif tag == 'UKA':
            produksjonstype = 4
        elif tag == 'KUP':
            produksjonstype = 2
        elif tag == 'AFEI':
            produksjonstype = 3
        else:
            produksjonstag = models.Produksjonstag(tag=tag)
            produksjonstag.save()
            produksjonstag_list.append(produksjonstag)

    return is_skildring, produksjonstype, produksjonstag_list

def create_lokale(lok_list):
    is_skildring = False
    lokale_list = []
    for tag in lok_list:
        if tag == 'skildring':
            is_skildring = True
        else:
            lok = models.Lokale(navn=tag)
            lok.save()
            lokale_list.append(lok)
    return is_skildring, lokale_list

def update_produksjon_gallery(produksjon_dict, new_produksjon, location):
    banner = '/default/katter.png'
    for key, value in produksjon_dict.items():
        if key[:8] == 'galleri_':
            try:
                kontekst = produksjon_dict[key.replace('_', 'txt_')]
            except:
                kontekst = ""
            url = value.replace("\\","/")
            fname = url.split("/")[-1]

            # medlemmer[]
            # try:
            #     person_list = produksjon_dict[key.replace("galleri", "persongalleri"].split(",")
            #     for person in person_list:
            #         fornavn = person[:person.find(" ")]
            try:
                old_foto = models.Foto.objects.get(fil='/bilder/' + fname, kontekst=kontekst)
                old_foto.arrangement = None
                old_foto.produksjon = new_produksjon
                old_foto.save()
                if key[-1] == '0':
                    shutil.copyfileobj(open(settings.MEDIA_ROOT + '/bilder/' + fname, 'rb'),
                                       open(settings.MEDIA_ROOT + '/bannere/' + fname, 'wb'))
                    banner = '/bannere/' + fname
            except:
                try:
                    r = requests.get(url, allow_redirects=True, stream=True)
                    shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                except:
                    url = url.replace("//sit", "").replace("/sit", "")
                    shutil.copyfileobj(open(location + url, 'rb'),
                                       open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                fil = '/bilder/' + fname
                if key[-1] == '0':
                    shutil.copyfileobj(open(settings.MEDIA_ROOT + '/bilder/' + fname, 'rb'),
                                       open(settings.MEDIA_ROOT + '/bannere/' + fname, 'wb'))
                    banner = '/bannere/' + fname

                new_foto = models.Foto(fil=fil, kontekst=kontekst, produksjon=new_produksjon, fototype=1)
                new_foto.save()
    return banner

def create_erfaringer(data_dict, produksjon):
    for key, value in data_dict.items():
        if key[:7] == 'person_':
            navn = value
            navn_lst = navn.split(" ")
            fornavn = navn_lst[0]
            etternavn = navn_lst[-1]
            # mellomnavn = ' '.join([str(elem) for elem in navn_lst[1:-1]])
            verv_input = data_dict[key.replace('person_','verv_')]
            verv_name = verv_dict[verv_input][0]
            # ar = data_dict['aar']
            try:
                medlem = models.Medlem.objects.get(fornavn=fornavn, etternavn=etternavn)
            except:
                medlem = False

            if verv_name == "tittel":
                try:
                    rolle = data_dict[key.replace('person','karakter')]
                    if rolle == None:
                        rolle = ""
                except:
                    rolle = ""
                if medlem:
                    erfaring = models.Erfaring(medlem=models.Medlem.objects.get(fornavn=fornavn, etternavn=etternavn),
                                           tittel=value, produksjon=produksjon, rolle=rolle)
                else:
                    erfaring = models.Erfaring(navn=navn, tittel=value,
                                               produksjon=produksjon, rolle=rolle)
            else:
                rolle = verv_dict[verv_input][1]
                if rolle == 'ingen':
                    try:
                        rolle = data_dict[key.replace('verv','karakter')]
                    except:
                        rolle = ""
                else:
                    try:
                        rolle += ", " + data_dict[key.replace('verv','karakter')]
                    except:
                        pass
                typ = verv_dict[verv_input][2]
                verv = update_verv(verv_name, typ)
                if medlem:
                    erfaring = models.Erfaring(medlem=medlem,verv=verv,
                                           rolle=rolle, produksjon=produksjon)
                else:
                    erfaring = models.Erfaring(navn=navn, verv=verv,
                                               rolle=rolle, produksjon=produksjon)
            erfaring.save()

def update_verv(tittel, type):
    try:
        return models.Verv.objects.get(tittel=tittel, vervtype=4)
    except:
        if type == 'prodapp':
            vervtag = update_vervtag(type)
            new_verv = models.Verv.objects.create(tittel=tittel, erfaringsoverforing=True, vervtype=4)
            new_verv.save()
            new_verv.vervtags.add(vervtag)
            new_verv.save()
            return new_verv
        else:
            new_verv = models.Verv.objects.create(tittel=tittel, vervtype=4, erfaringsoverforing=False)
            new_verv.save()
            return new_verv

def update_vervtag(tittel):
    try:
        return models.Vervtag.objects.get(tag=tittel)
    except:
        vervtag = models.Vervtag.objects.create(tag=tittel)
        vervtag.save()
        return vervtag



def check_sidetekst(data, data_dict, data_check='sidetekst'):
    try:
        if data_dict[data_check].find(data_dict[data]) == -1:
            return data + ":    " + data_dict[data] + "\n\n"
        else:
            return ""
    except:
        return ""

def transfer_all_medlemmer(location):
    try:
        os.mkdir(settings.MEDIA_ROOT + '/bilder')
        os.mkdir(settings.MEDIA_ROOT + '/portretter')
    except:
        pass
    list_of_dicts, dict_of_lists, dict_of_sets, errors = getAll(location + 'medlem/')
    skrift = models.Lokale(navn='skrift.no')
    skrift.save()
    arr_for_pictures = models.Arrangement(tittel='Bilder fra skrift knyttet til medlemmer', offentlig=False,
                                          tidspunkt=datetime.date(2020, 12, 31), lokale=skrift)
    arr_for_pictures.save()

    for dict in list_of_dicts:
        create_medlem(dict, arr_for_pictures, location)

    print("Errors: ", errors)

    remove_duplicate_members()

def remove_duplicate_members():
    # pdb.set_trace()
    m_list = models.Medlem.objects.all()
    all_duplicates = set({})
    for medlem in m_list:
        if medlem in all_duplicates:
            continue
        else:
            duplicates = models.Medlem.objects.filter(fornavn=medlem.fornavn, etternavn=medlem.etternavn)
            if len(duplicates) > 1:
                # pdb.set_trace()
                duplicates = duplicates.exclude(pk=medlem.pk)
                MergedModelInstance(medlem, duplicates)
                medlem.save()
                for duplicate in duplicates:
                    all_duplicates.add(duplicate)

    for dp in all_duplicates:
        dp.delete()

def transfer_all_produksjoner(location):
    try:
        os.mkdir(settings.MEDIA_ROOT + '/plakater')
        os.mkdir(settings.MEDIA_ROOT + '/bannere')
    except:
        pass
    list_of_dicts, dict_of_lists, dict_of_sets, errors = getAll(location + 'forestilling/', 'forestilling')

    for dict in list_of_dicts:
        create_produksjon(dict, location)

    print("Errors: ", errors)



def fixtext(s):
    if s[0].isupper() and s[1:].islower():
        return s.lower()
    else:
        return s


if __name__ == "__main__":
    # FYLL INN DIN LOKALE FILSTI TIL SKRIFTDATA HER:
    transfer_all_medlemmer('/Users/jonas/Desktop/Skriftdata/')