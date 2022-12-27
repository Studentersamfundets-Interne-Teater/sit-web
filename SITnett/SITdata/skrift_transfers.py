import sys

# FYLL INN DIN LOKALE FILSTI TIL SITNETT HER:
# sys.path.append("/home/cassarossa/sit/web/sit-web-2020/SITnett")
sys.path.append("C:/Users/jacob/sit-web/SITnett")

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SITnett.settings")
import subprocess

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
import html2text as h2t

# import pickle

# coding=utf8
local_manus_dict = {'Jubileumsbokslepp, romantikk': '', 'Jubileumsbokslepp, utdeling av forfatterkatt': '',
                    'Mohrens sista suck 1. akt (1954)': '', 'Mohrens sista suck 1. akt (1958)': '',
                    'Mohrens sista suck 1. akt (1961)': '', 'Mohrens sista suck 2. akt (1954)': '',
                    'Mohrens sista suck 2. akt (1958)': '', 'Mohrens sista suck 2. akt (1961)': '',
                    'Mohrens sista suck 3. akt (1954)': '', 'Mohrens sista suck 3. akt (1958)': '',
                    'Mohrens sista suck 3. akt (1961)': '',
                    'Naar vi døde vaagner - X': 'For komplett liste over aktive snupper og snopper: klikk på \ufeff«Supperevyen\n2015».  \nVed å klikke på symbolet som dukker opp i nederste høyre hjørne når muspekeren\nføres over videoen, får du fullskjermformat. Dette øker ikke bildekvaliteten\nvesentlig, men fører til at aktørene framstår som litt mindre slanke.  \n\n\n',
                    'Kjærlighetsvise til byen': '![](uka/2003_glasur.jpg)Du e  \nhele norges lillebroder;  \nuflidd, ærlig, rocka, rå.  \nEn utfordrer som vil bli større;  \nbygge ut og bygge på.  \nStor i kjeften, møte motstand  \nbrannsår sku du også få  \nbrannsår sku du også få.  \n  \nrefreng:  \nHvis Trondhjem hadd et hode  \nva det gamle NTH,  \nog navlen villa logge  \nder kor domen e å sjå,  \nog hvis du bare bruke  \ndin litt skitne fantasi,  \nså finn du sikkert ut  \nka Olav Trygvason sku bli.  \n  \nDu e  \nonkel Trond, heimert i kaffen,  \nliten, tjukk, i harmoni.  \nEn humoristisk skrytepave  \ntrygg og træg, for ting tar ti  \nelegant med snurr på barten  \nmen e fri for snobberi  \nmen e fri for snobberi.  \n  \nrefreng:  \nHvis Trondhjem hadd et hode ...  \n  \nDu e  \nbestefar med rusten stemme  \ntusen år og like blid  \nVenn med konga og prinsessa  \nlandets far i svunnen tid  \nfuret, værbitt, rynka panne  \ndu e full av nostalgi  \ndu e full av nostalgi  \n  \nrefreng:  \nHvis Trondhjem hadd et hode ...  \n  \nLitt til venstre ned for hodet  \ne det slettes ikke dødt;  \ndet banke og pulsere  \ni no´ stort og rundt og rødt.  \nMed rike tradisjona  \nog en fest som ei tar slutt;  \ndet hjertelige Samfundet  \npulsere uavbrutt  \n\n\n',
                    'Bikini girls': '', 'Blanderegle': '', 'Dans og paljetter': '', 'Designet liv': '',
                    'Drikkevise': '', 'Finale 1. akt': '', 'Finale 2. akt': '',
                    'Lea Loff og Dora Mirakles heltesang': '', 'Let the water flow': '', 'Milles drømmesang': '',
                    'Satans sang': '', 'Takk til alle': '', 'Tenk hvis jeg var neger': '', 'Til ungdommen': '',
                    'Trine-Lises sang': '', 'Trondheimsvise': '', 'Åpning (Paradoks)': '', ',kåMMa,': '',
                    'Adolf Hitler parodierer Jan Eggum': '', 'Bare en drøm': '', 'Butlerballetten': '',
                    'Butlerboka/Oppskriften': '', 'Dama på Bunnpris': '', 'Dansen': '', 'Fly avsted': '',
                    'Girl I love you (liveversjon)': '', 'Girl I love you (studioversjon)': '',
                    'HKH Kronprinsen ankommer Storsalen': '', 'Hvem er jeg?': '', 'Kicker på katter': '',
                    'Ode til nyhetene': '', 'Samfundets Støtter': '', 'Skål!': '', 'Tango Maria': '',
                    'Trondheim, Trøndelag': '', 'Tusenårsbaby': '', 'Åpning (,kåMMa,)': '', 'Alt er sex': '',
                    'Alt er sex II': '', 'Drikkevise (Alt-er-sex)': '', 'Frivillig': '', 'Jeg er fri': '',
                    'Kor ska vi bo': '', 'Mona & Fiona': '', 'Om morran': '', 'Skj': '', 'Storhavets pris': '',
                    'Tante på Tustna': '', 'Trondheimsvise (Alt-er-sex)': '', 'Tuba i nesen': '', 'Ut av skapet': '',
                    'Why I speak': '', 'Beep': '', 'Buran-spelet': '', 'Den slemme sangen': '',
                    'Det det va og DDE': 'Teksten tar utgangspunkt i at et par kjente D.D.E.-tekster opprinnelig ble\nskrevet for UKE-revyer ([ **Du og æ og by´n**](index.asp?lyd=Du og æ og by´n)\n, UKA 1985 og [**Det umulige er mulig**](index.asp?lyd=Det umulige er mulig) ,\nUKA 1987 - og den mindre kjente [**Nøkken**](index.asp?lyd=Nøkken) , UKA\n1977).  \n  \nVi va´ nånn guta fra Namsos  \nsom brukt å spæll janitsjar  \nVi drømt om å bli som Åge  \nog bynt å spar te´ gitar...  \n  \n...for vi vesst at det va mulig det umulige  \nAv og te blir nye stjerna tent  \nVi trudd på det utrulige,  \nat også vi koin bli kjent  \n  \nVi hadd aldri vært i Paris  \nog vi hadd itj vært i Rom  \nVi hadd berre bodd i Namsos  \nså vi tænkt vi skoill syng om...  \n  \n...det å få vis dokk by´n vi bur i, sei dokk vil bli gla´in  \nJa, dra dokk med gjennom by´n vi går tur i  \nog håp dokk trives bra i´n  \nSjøl har vi gått så oft gjennom gatan  \npå leit ætt´ ein røykfylt kafé  \nmen vi veit itj kor, nei veit itj kor hæn den e  \n  \nDet va lurt å finn ein imitsj:  \nVi sang om by´n vi bur i  \nMen det va´ gamle UKE-sanga  \nsom hadd fått ein vri...  \n  \n...men det e´ ein hemlighet  \nEin herlig, herlig hemlighet  \nOg det e´ berre Idar Lind som veit  \nat det e´ sånn  \n  \nNo har vi kommi på TV  \nog vi syns at ailt e greit  \nFor vess vi går tom for teksta  \nså veit vi kor vi ska´ leit:  \nJarr-a-gakk Prin-ki-po Rægg-e-ti Narr-i-ciss  \nDe-cha-vi Bom-t-bom Fa-bu-la  \nJa, går vi tom for teksta  \nså veit vi kor vi ska´ leit  \n  \n\n\n',
                    'Dette kan vi kalle happy ending': '', 'Drikkevise koral': '', 'En liten sang om engasjement': '',
                    'Finale (Skjer-mer-@)': '', 'Fix & Alexa gjør rent bord': '', 'Georgsangen': '',
                    'Gjør det på TV': '',
                    'Hjørdis´ siste jul': 'Utgangspunktet for nummeret var at det ikke lenger var mulig å få igjen\nvekslepenger på bussen i Trondheim, du fikk en kvittering og måtte oppsøke\nkontoret til Trondheim Trafikkselskap får å få kontanter.  \n  \nDet var tidlig julemorgen  \ni en by i Norges land,  \nog nå skulle gamle Hjørdis  \nut og handle litegrann  \n  \nNedi veska lå en lapp som  \ndet sto "Bok om Oddvar Brå,  \nheklabrikke, fire telys og  \nen flaske Portvin" på  \n  \nI sin gamle, slitte kåpe og  \nmed tusen kroner som hun  \nhadde spart til årets bytur  \nsto hun klar da bussen kom  \n  \nOg hun rakte fram sin sed-  \ndel med ei gammel, skjelven  \nhand for å løse en billett  \nhos trafikkselskapets mann  \n  \n"Vi væksl itj hær på buss´n,  \nsjø, du ska få dæ ein  \ntegodelapp te mæ du, sjø”  \n  \nMed nihundredeogtreognitti  \nkroner på en lapp (som var  \ngul) steg hun av i Prinsens  \ngate for å kjøpe gave til sin  \nhjemmehjelp til jul  \n  \nAlle gatene var pyntet  \nog på Torvet sto et tre  \nmed små julelys og stjerne,  \nHjørdis frydet seg ved det  \n  \nOg det bugnet i butikkene  \nav alt hun skulle ha  \nmen ved disken ble hun  \nstadig møtt av mennesker  \nsom sa:  \n  \n"Ka herre herran e?  \ndu får itj nån ting førr det  \npappiret der, nei"  \n  \n  \nMed nihundredeogtreognitti  \nkroner på en lapp (som var  \ngul) sto hun rådvill midt på  \nTorvet da det ringte inn til jul  \n  \nGamle Hjørdis ruslet rundt  \nog mintes svakt sjåførens  \nord om at pengene på lap-  \npen kunne fås på et kontor  \n  \nFørst da julestjerna lyste  \nfant hun døra hvor det sto:  \n"Grunnet høytid har vi  \nstengt fra klokka to"  \n  \nMed et tappert smil om munnen  \ntok hun atter en gang fatt,  \npå et langt og øde fortau  \nsom var isete og glatt  \n  \nMen ved fortauskantens  \nslutt fikk hennes gamle, skjøre ben et  \nskjebnesvangert møte  \nmed en frossen rennesten.  \n  \nGamle Hjørdis lå på  \nsykehus med dobbeltsidig  \nlårhalsbrudd til trettende  \ndag jul og i byens kloakk  \nlå det nihundredeogtreog-  \nnitti kroner på en lapp som  \nvar gul  \n  \n(Samtidig kor:)  \nMed nihundredeogtreognitti  \nkroner på en jul, lå  \nnihundredeogtreognitti  \nkroner - den var gul  \n  \n\n\n',
                    'Hva er kjærlighet, hva er sex': '', 'Jynarn': '', 'Maria': '', 'Petter Gevær': '',
                    'Takk bare bra': '',
                    'Tør vi mene noe om muslimer': 'Det e viktig å få ment nånting  \nnår man e student  \nom apartheid og om Chai Ling  \nog bya som har brent  \nI alle år har vi sunget pent om fred  \nmens lighterflammen har brent sakte ne´...  \n  \nMen tør vi mene noe om muslimer  \nTør vi finne et ord som rimer  \nTør vi kalle Ayatollah pervers  \nTør vi synge sataniske vers  \n  \nBlant publikum fins det mang  \nsom ikke e så tolerang  \nDet som nånn syns det e smell i  \ne det nånn som vil hold hellig  \nKrigens sjøfolk, Røde Kors og Shetlandslarsen,  \nHeyerdahl, Kyrkjebø, Nansen og Nordvestpassasjen,  \nsjømannskoret, stygge sykdommer og nød,  \nhutuer og tutsier og spyfluer og død,  \nhalte sauer, dysleksi og Wenche Foss,  \ntykke damer, likestilling, angst og Johann Koss,  \nhemorider, bulimi og Bjugn og Nobelprisen,  \npavens nese, Dalai Lama, Gud og Erik Diesen  \n  \nSå vi tør ikke....  \nmene noe om muslimer  \neller finne noen ord som rimer  \nAyatollaher er ikke så verst  \nOg sorte slør er ganske knæsjt  \n  \n\n\n',
                    'Var-hattkaill': '', 'Veita': '', 'Åpning (Skjer-mer-@)': '', 'Bare burger': '',
                    'Bergliots sang': '', 'Bill the kid': '', 'Blainnalag': '', 'Die Bobilferie': '', 'Drittsekk': '',
                    'En arm for mye': '', 'Fattigtrondhjem': '', 'Finale (Fabula)': '', 'For støgg for OL': '',
                    'Frokost': '', 'Gjemselsangen': '', 'Hvalvise': '', 'Juan Antonio': '',
                    'Kjøssekurs i Frausundvær': '', 'Refrenget': '', 'Rimesang': '', 'Siste vakt på Fyret': '',
                    'Slimkongesangen': '', 'Timeplansangen': '', 'Virtual reality': '', 'Åpning (Fabula)': '',
                    'Bom-T-Bom/Ett skritt tilbake, to skritt fram': '', 'Er det sant': '', 'God natt': '',
                    'Gråt min balalaika': '', 'Helse frelse': '', 'Kjappe krigers tango': '', 'Køfri': '', 'Laks': '',
                    'Munken': '', 'Plingfæst': '', 'Rockeprinsen': '', 'Teletorg': '', 'Trægost': '',
                    'Turist i egen by': '', 'Ut på by´n': '',
                    'Anna og jeg og Ole Jonny': '![](img/1989_anna_og_jeg_og_ole_jonny.jpg)Tekst Idar Lind, musikk Petter Wiik.  \n  \n\nDet var Anna og jeg og Ole Jonny.  \nVi var studenter. Vi var nitten. Vi var fri.  \nSjela utålmodig. En drøm var nettopp født.  \nVi kom til Samfundet høsten sekstini.  \nOle Jonny skulle jage USA fra Vietnam.  \nJeg ville møte EEC med felles front.  \nAnna så seg sjøl som formannskandidat\n\n\\- å nei, vi tre gjorde aldri sånt.\n\nVi satt i salen under debatten  \nog klappa til replikker med poeng.  \nOle Jonny traff ei rødhåra jente,  \nforelska seg og kjøpte dobbelseng.  \nJeg kjøpte en pils til  \nog tenkte at han heller kunne ha forelska seg i meg.  \nEn kveld sto Anna på talelista  \n\\- men trakk seg.\n\nVi møttes, studerte, skiltes  \nog møttes igjen under UKA-79.  \nSjela urolig. Rester av en drøm.  \nEnnå unge. Ennå ikke fylt tretti.  \nOle Jonny skulle flytte og bli husokkupant.  \nJeg ville kjøpe gitar og spille pønk.  \nAnna så seg sjøl i en lenkegjeng i Alta\n\n\\- å nei, vi tre gjorde aldri sånt.\n\nVi satt i baren på Selskapssida  \nog syns revyen skulle vært refusert.  \nOle Jonny var blitt far til en rødhåra gutt,  \nvar nyskilt og deprimert.  \nJeg feira magistergraden med rødvin  \nog tenkte at han godt kunne ha fått trøst hos meg.  \nAnna hadde bestilt billett til Alta  \n\\- men trakk seg.\n\nVi satt på Puben før revyen i dag  \nog snakka som om ingen ting hadde hendt.  \nSønnen min har planlagt å reise til Brasil  \nfor å redde regnskog, sa Ole Jonny.  \nJeg nippa til en Torres Coronas 1985  \nog tenkte at det grå ved ørene kledde ham.  \nAnna begynte å prate om den gangen hun sto på talelista  \n\\- og trakk seg.\n\nDer satt Anna og jeg og Ole Jonny  \nog snakka, som så mange ganger før.  \nSjela fylt av vemod. Drømmen nesten glemt.  \nMen vinden blåser liv i gamle glør.  \nOle Jonny skal bli med sønnen til Brasil.  \nJeg prøver å finne ut av dette med EF´s indre marked.  \nAnna har noe stort på gang.\n\n\\- Hun vil ikke si hva det er.  \nIkke denne gangen.\n\n  \n\n\n',
                    'Dåmkoret': 'Tekst Marit Moum Aune, melodi Tore Nedgård.  \n  \nHar du noen gang gått forbi,  \nNidarosdomen - sen natterstid  \nDet er stille -  \nmen plutselig høres et drønn  \nEt vell av stemmer i fra begge kjønn;  \n  \nRefr.:  \nDå-då-dåmkore hå-hei  \nDå-då-dåmkore vise vei  \nDet er koret som har vaska seg  \nDå-dåmkore hå-hei!  \n  \nBach og Beethoven og Liszt -  \nlett match for en korist.  \nBørge er i bassrekka,  \nalten tackler Rebecca  \n  \nDirigent´n e i slag  \nVi tar seier´n hjæm i dag  \nAnne, Øyvind og Mari  \nKom igjen så synger vi  \n  \nRefr.:  \nDå-då-dåmkore  \n  \nVi reise oss i Vestskipet  \nVi juble å syng me  \nFor ingen kor slår Dåmkore  \nå takk - å takk å låv for det  \n  \n\\- Svovelpreken, Svovelpreken,  \nHei, Hei, Hei .. .  \nDet er prekenen sin det  \n  \nDa e saken klar  \nÆ vil ha et svar  \nAlta, bassa og tenor  \nKæm e Norges bæste kor?  \n  \nRefr.:  \nDå-då-dåmkore hå-hei  \nDå-då-dåmkore vise vei  \nDet er koret som har vaska seg  \ndåmkore hå-hei!  \n  \nDåmkore - Halleluja  \nBæste koret i lainne  \n  \n\n\n',
                    'Ska det vera, ska det vera': 'Tekst Ralph Bernstein, melodi Morten Hofstad.  \n  \nJe er en riktig patriot,  \nog Brumenddal´n er slektas rot.  \nOg når jeg går på fest en kvell,  \nstår gutta der og byr seg tel.  \nI frå Romdal og Veldre, og Væillset og Vang  \nJa, dom ber på sine kne.  \nMen kjem dom å prøve på noe med meg,  \nda får dom klar beskjed.  \nPANG!  \n  \nSka det vara ska det vara Brumenddøl.  \nBrumenddøl som je e sjøl.  \nHæin kæin godt vara spikjin og flat som ei fjøl,  \nmen ska det vara ska det vara...  \n  \n...Brumenddøl  \nBrumenddøl som je e sjøl.  \nHæin kæin godt vara spikjin og flat som ei fjøl,  \nmen ska det vara ska det vara Brumenddøl.  \n  \nMen Brumenddal´n har endra seg.  \nFor mellom gran og timotei,  \nså kom det hit fra fremmedlaind  \nen kjøpmainn i fra Pakistan.  \nBåde Romdal og Veldre, og Væillset og Vang  \nEr nå bære likevel.  \nSå gutta dom måtte få ugraset vekk.  \nOg dynamitt det smell.  \nPANG!  \n  \nSka det vara ska det vara Brumenddøl.  \nBrumenddøl som dom er sjøl.  \nFor når Brumenddølknølen får seg øl.  \nså ska det vara ska det vara...  \n  \n...Arendal  \nArendøl som æ e sjøl  \nHan kan godt vere skraba og flad som ei fjøl,  \nmen ska det vere skal det vere Arendøl.  \n  \nJa, ta en tur te Arendal,  \nog Brumendal blir heilt banal.  \nEn pakkistaner å e det??  \nNei, ta en tur te oss å se.  \nMi har Libanon, Chile, Iran, Pakistan.  \nJa, et heilt asylmottag.  \nOg guttene våre kan drikke og sloss,  \nfor FMI si sag.  \n  \nSka det vere ska det vere Myrdal-døl  \nMyrdal-døl som æ e sjøl.  \nHan kan godt vere skraba og flad som ei fjøl  \nmen ska det vere ska det vere Myrdal-døl.  \n  \nSka det vara ska det vara  \nStjørdøl, Orkdøl, Namdøl, Verdøl  \nArendøl og Brumenddøl som vi er sjøl.  \nDu kan godt kaille hain Ola Pottit og knøl.  \nMen ska det vara ska det vara ... døl.  \nSka det vara, ska det vara Norges Blomsterdøl.  \nSANN!!!  \n\n\n',
                    'Surfer´n': '![](img/1989_surfern.jpg)Tekst: Kjell-Ivar Myhr. Musikk: Bjørn Willadsen.  \n  \nÆ e´ ein surfer! Surfer!  \nKjæm det ei bølge så hoppe æ på.  \nÆ e´ ein surfer! Surfer!  \nEin ækte bølgerytter i rosa trikå.  \n  \nÅtti-åras cowboy bruke ikke hæst.  \nGampen e´ bytta med et surfebrætt.  \nHer trængs ingen stetson, ingen frynsat væst.  \nBerre ein trikå som vise musklan lætt.  \n  \nÆ rir mot solnedgangen  \npå ein bølgetopp  \nog vise aill på stranda  \nein veltrena kropp.  \n  \nÆ e´ ein surfer! Surfer!  \nKjæm det ei bølge så hoppe æ på.  \nÆ e´ ein surfer! Surfer!  \nEin ækte bølgerytter i rosa trikå.  \n  \nSom langhåra hippi surfa æ i lotusstilling  \nover ei bølganes blomsteræng.  \n\\- Æ levd på dein rusen læng.  \nSom sjokk farga punker i piggtrådtrikå  \nokkupert æ et brætt med nagla og lær:  \n\\- Æ va´ sint! Æ va´ vulgær!  \nOg på toppen av jappebølgen  \nsurfa æ glatt på businessclass –  \n\\- Det va´ stas!  \n  \nÆ e´ ein surfer! Surfer!  \nKjæm det ei bølge så hoppe æ på.  \nÆ e´ ein surfer! Surfer!  \nEin ækte bølgerytter i rosa trikå.  \n  \nÆ rir mot nitti-åran  \nder nye bølga kjæm,  \nmen æ kain berre bli med  \nein siste bølge hjæm.  \n  \nÆ rir mot solnedgangen  \nog siste bølga kjæm.  \nÆ vil itj, men må bli med  \neldrebølgen hjæm.  \n  \n\n\n',
                    'Trondhjæm midt i hjertet': 'Tekst Forfatterkollegiet, melodi Bjørn Willadsen.  \n  \nStilt attmed Elva ligg Trondhjæm,  \nby´n som fortjene en sang.  \nAldri har æ lengta sånn hjæm  \nsom da æ va bortreist en gang.  \nTænk å vær oppvokst i Trondhjæm  \nder´n Hjallis og´n Bratseth e født,  \nder folk går sæ kveldtur te Lykkens Portal  \nved Elva for å spøtt.  \n  \nTrondhjæm, Trondhjæm,  \nIngen by e så fin!  \nMidt i mitt hjærte ligg Trondhjæm,  \nfor det e byen min!  \n  \nVårn e så vakker i Trondhjæm,  \nhvis du har foinne en venn.  \nDa rusle vi hånd i hånd hjæm  \nte Lamon og Ila igjen.  \nOm vintern ligg isen i gatan.  \nDu tar med dæ venn din på spark.  \nOg bli du litt frossen, så tine du snart  \nav trondhjæmspi og kar  \n  \nTrondhjæm, Trondhjæm,  \nIngen by e så fin!  \nMidt i mitt hjærte ligg Trondhjæm,  \nfor det e byen min!  \n  \nDæffor vil æ bo i Trondhjæm.  \nHer smile folk og e glad.  \nSiden, når Gud tar min ånd hjæm,  \ngår æ te Den Evige Stad.  \nDer sjer æ Domen og Stiftsgårn,  \nog Elva går svengat og djup.  \nOg når æ går inn te Vårherre teslutt,  \nså får æ trondhjæmssup!  \n  \nTrondhjæm, Trondhjæm,  \nIngen by e så fin!  \nMidt i mitt hjærte ligg Trondhjæm,  \nfor det e byen min!  \n  \n  \n\n\n',
                    'Vårres vesle vei': '![](img/1989_varres_vesle_vei.jpg)Tekst Marit Sofie Todal, musikk Bjørn\nWilladsen.  \nPå scenen: Kristin Nordstrøm.  \n  \nKan en ha det ber i sinne?  \nenn nårn dorme lett i sola  \nde e gått å verra mennesk  \nå ha heimadresse jorda.  \nDet e vår i veien vårres.  \nDe e grønne skudd på hekken,  \nkailln hainn driv på ut å jåbbe  \nme å dresser hageflekken  \n  \nom dæm krige litt i utlainne  \nde spell itj nå å sei  \nså læng vi har vår egen  \nstille fine villavei  \n  \nKailln har bøgd de hærre huses  \nå kom ungan åran etter  \nde va kollikkvondt og regningsbud  \nå mange våkenetter  \nmen no har de blitt så stille  \nat de skull du aildri sjå  \nungan vår har gått på gymnas  \nå avla barn å fløtta frå.  \n  \nungdom sless me kniv på Kålstad  \nde spell itj nå å sei  \nså læng vi har vår egen  \nstille fine villavei  \n  \nDe har vesst skjedd ett mord i Midtbyn  \nA en kollisjon på Ila  \nMen her i veien vårres  \nkjøre de så lite bila  \nUnga sniffe lim på Lamon  \næ brodere på stramei  \nde ska bli en klokkestreng  \nte stua i vår vei  \n  \nom dæm krige litt i utlainne  \nde spell itj nå å sei  \nså læng vi har vår egen  \nstille fine villavei  \n  \nPå verandan sitt vi åfte  \nnår de kvelles åver byen  \neiller rusle runt i hagen vår  \nog glane oppi skyen  \nfor stjernemyriaden e no aillti like sjønn  \nom dan´ kainn du vesst sjå´n i fra botten av en brønn  \n  \nFor stjernekrig og osonlag  \nde spell itj nå å sei  \nfor vårres stjernehimmel  \nover vårres vesle vei.  \n\n\n',
                    'De-cha-vi': '',
                    'Det umulige er mulig': '(tekst: Idar Lind, melodi Sigurd E. Liseth)  \n  \nHanda slapp taket i lekegrinda  \nDet første steget var tatt  \nVi så oss aldri tilbake  \nmot det vi hadde forlatt  \nVi skulle finne skatten bak den sjuende blåne  \nog hente prinsessa fra et berg av glass  \nreise østenfor sol og vestenfor måne  \nog lande i småfly på Den røde plass  \n  \nVi visste det var mulig, det umulige  \nVindmølla gir tapt for Don Quiote  \nVi trodde på det utrolige  \npå Soria Moria slott  \n  \nDe sa det var illusjoner  \nDet ville vi skjønne om noen år  \nMen vi la barndommen bak oss  \nVi visste at framtida var vår  \nVi skulle målbinde en politiker  \nGi de husløse husly i kongens palass  \nKle dem i keiserens gamle klær  \nog lande i småfly på Den røde plass  \n  \nVi visste det var mulig, det umulige  \nVindmølla gir tapt for Don Quiote  \nVi trodde på det utrolige  \npå Soria Moria slott  \n  \nMen ingen politiker narres til taushet  \nved synet av skjære og bukkehorn  \nDrageskatten står på konto i Sveits  \nDen blinde høna finner ikke korn  \nSultne prinsesser har ingen erter  \nDe sover på jordgulv uten madrass  \nTrollet sprakk ikke da sola rant  \nmen et småfly har landet på Den røde plass  \n  \nVi visste det var mulig, det umulige  \nVindmølla gir tapt for Don Quiote  \nVi trodde på det utrolige  \npå Soria Moria slott \n\n',
                    'Det va´ den vår´n...': '',
                    'En innflytters vise': '(Tekst Ralph Bernstein, melodi Arild Dragset)  \n  \nEn innflytters vise om Trondhjem  \nÆ kom som student, som så mang ainner gjør  \nÆ lært mæ jo fort dialekten  \nOg om vinter´n så regne det mer enn det snør  \nFor vinter´n sku ha vært kvit og klar,  \nen drøm om at våren e nær  \nÅ gå der og vente  \nå treffe ei jente  \n  \nMen vinter´n i Trondhjem vart aldri som vintra sku vær  \n  \nEi vise om våren i Trondhjem  \nBlir alltid ei vise som e litt for kort  \nNår endli´ eksamen e over,  \ndu går ut, da e våren allerede bort  \nMen våren sku ta seg bedre tid  \nOg kroppen vær lett som en fjær  \nOg du sku bli kjent med  \nei vårvakker jente  \n  \nMen våren i Trondhjem vart aldri som våra sku vær  \n  \nOg visa om sommer´n i by´n min  \nden handle om køa på reisebyrå  \nOm tåke og regnvær og kulde  \nSjøl nudistan har tjokkgenser´n på  \nMen sommer´n sku vær lyseblå  \nog varme et sommerbegjær  \nOg du sku vær solbreint  \ntætt innte ei jente  \n  \nMen sommer´n i Trondhjem vart aldri som somra sku vær  \n  \nMen høstvisa den ska bli vakker!  \nFor høsten i Trondhjem den kjæm som ei trøst  \nJa rett nok så regne og blæs det,  \nmen det ska det jo gjør når det e høst  \nOm høsten kjenne du at du e te  \nder du kjæmpe dæ fram med besvær  \nOg folk tår tett sammen i busskø og vente  \nOg tætt innte dæ  \nstår ei jente, ei jente  \n  \nJa om høsten er været i Trondhjem slik høstvær ska vær  \n  \n\n\n',
                    'En spennende dag': '', 'Hjæmbrygga': '', 'Kaffe og Vaffel': '',
                    'Kaffe og vaffel': '(tekst Idar Lind, melodi Arild Dragset)  \n  \n ****Vi kom frå Mausundvær og Brekstad og Ressa  \nI alle år tok vi båtn te byn  \nOpp under jul for å handel og te sjukhuse iblant  \nnår det va kleint me hjerte eller syn  \nDet hendt nok oft at det va hustri over Flakkfjordn  \nmen i salongen va det godt me røyk og prat  \nOg når vi klappa in te kaia va det første som vi gjord  \nå gå te Gildevangen for å få oss mat\n\nDer fikk vi kaffe og vaffel med brunost  \nTynnlefs med sukker og smør  \nOg ætte tre-fir timas tid va handleturn forbi  \nDa va det meddag som sto på menyn  \nOg vi åt kjøttkak me brunsaus og erter  \nKarbonade me erter og løk  \nOg va serveringsdama raus ga ho oss rikeli me saus  \nog dobbelt opp med både erter og løk\n\nVi kom me Kongsbussn te byn i dag tidlig  \nog gikk te Gildevangen som vi har gjort før  \nDa vi hadd gått opp trappa og skoll finn oss eit bord  \nvart vi møtt av ein skeivøygd servitør  \nHan ga oss spisekart me mange rare retta  \nfor no va Kaffistova Kina-restaurant  \nDer sto det chop suey og sursøt svinefile  \nog pekingand og bambusskudd med ris\n\nVi vil ha kaffe og vaffel med brunost  \nTynnlefs med sukker og smør  \nOg ætte tre-fir timas tid e handleturn forbi  \nDa e det meddag som står på menyn  \nVi vil ha kjøttkak me brunsaus og erter  \nKarbonade me erter og løk  \nOg e serveringsdama raus gir ho oss rikeli me saus  \nog dobbelt opp med både erter og løk\n\nVi kom te Beverly og Butterfly og Børchen  \nfor å kvil oss og få oss litt mat  \nÆ vil ha rundstykke med kvitost!  \nVi har bagætt med brie  \nog kroasang med kammambær  \nÆ vil ha brus, æ vil ha Farris!  \nVi har fransk Perrier.  \nvi sæll ijt vanlig brakkvann her.  \nÆ vil ha kaffe!  \nVil du ha kappusjino, æspræsso eller kaffe å le\n\nNei! Vi vil ha kaffe og vaffel med brunost  \nog tynnlefs med sukker og smør  \nOg ætte tre-fir timas tid e handleturn forbi  \nDa e det meddag som står på menyn  \nVi vil ha kjøttkak me brunsaus og erter  \nKarbonade me erter og løk  \nOg e serveringsdama raus gir ho oss rikeli me saus  \nog dobbelt opp med både erter og løk\n\n\n\n',
                    'Kardemomme by': '', 'Kom og se!': '', 'Marilyn': '', 'Olav Trygvesøns vise': '',
                    'Pingwienervals': '',
                    'Pompel og Pilt': 'Tekst: Ralph Bernstein.  \n  \nNummeret tok utgangspunkt i ei sann historie: Restauratør Benito Nava sendte\nsine ansatte på sykkel ut i byen. Når de kom til et parkometer som var utløpt,\nla de på penger og la igjen en hyggelig hilsen fra Benitos under\nvindusviskeren. Dette mente parkeringsetaten i Trondheim var helt ulovlig, det\ner forbudt å betale parkometeravgift for andre.  \n\n\n',
                    'Rio på Rye': '',
                    'Romantikk': '(Tekst Tor Gunnar Heggem, melodi Eli Moen)  \n  \nJeg husker fra min ungdom hvordan mannen av i går  \ngjorde kurtise for sin kvinde.  \nHan bukket alltid høflig, og han kysset hennes hånd  \nog røpet aldri hva han hadde i sinne  \nHan ba sin sin kvinne med på kinograf og resturang,  \npå kjelken bak oss satt han med sin lange stang  \nog styrte kjelken for sin venninde  \n  \nRomantikk, romantikk  \net lite smil, et lite nikk,  \ndet var nok for de gamle piker  \n  \nOg fridde han, så rødmet vi og hvisket frem vårt ja,  \nslik måtte det være. Slik var skikken.  \nHan torde knapt å kysse oss før bryllupsklokken slo,  \nVi måtte nøye oss med romantikken.  \nVi måtte alltid passe på så ingenting gikk galt.  \nEn ubetenksomhet, det kunne bli fatalt,  \nså gikk da grensen ved strømpestrikken.  \n  \nRomantikk, romantikk  \net lite smil, et lite nikk,  \ndet var nok for de gamle piker  \n  \nMen årene gikk fort. Moralen ble lagt bort.  \nDet sjokkerte den gamle skole.  \nDen unge Eva sto frimodig frem og lo  \nog kastet brystholder, skjørt og kjole.  \n  \nRomantikk, romantikk  \net lite smil, et lite nikk  \nvar mer enn nok for de gamle piker  \n  \nFor vi var født for tidlig, før pille og spiral.  \nDe unge gjorde kort prosess med gammledags moral.  \nRomantikk, romantikk  \net lite smil, et lite nikk,  \nvar mer enn nok for de gamle piker  \n  \nMen nå er ringen sluttet. Nå er det blitt som før.  \nFor nå er moralen på ny fornøden.  \nOg to som søker sammen må som dengang regne med  \nå elske hverandre inn i døden.  \nNå gjør ingen lenger det som alle gjorde nyss  \nNå tar du sjanser selv med litt for hete kyss,  \nslikt legger en demper på elskovsgløden.  \n  \nRomantikk, romantikk,  \net lite smil, et lite nikk  \nfår være nok for de unge piker.  \n\n\n',
                    'Sleipe Johan': '', 'Ænkeltvindu': '',
                    'Du og æ og by´n': '(tekst Idar Lind, melodi Sigurd E Liseth)  \n  \nKan æ ein gong få vis dæ by’n æ bur i  \nveit æ du vil bli gla’ i ’n  \nVil du bli med gjennom byn æ går tur i  \nska du nok trives bra i ’n  \nHand i hand ska vi gå gjennom gatan’  \nmed murbygg og småhus av tre  \nMen – Æ veit ijt kæm  \nÆ veit ijt kor hæn du e\n\nKanskje sæll du støvla og sko  \ni ein butikk i Moskva  \nEller du står ved eit samleband  \ni Detroit, USA  \nKanskje du kjøre som drosjesjåfør  \ni skyggen av Notre Dame  \nEller du går ut’n jobb og driv  \nlangs kaian’ i Amsterdam  \nKanskje i Tokyo, kanskje i Wien  \nKanskje i Bonn, eller i Aberdeen  \nÆ veit at du e der  \nÆ veit du e fin  \nÆ veit det e du og æ\n\nKan æ ein gong få vis dæ by’n æ bur i  \nveit æ du vil bli gla’ i ’n  \nVil du bli med gjennom byn æ går tur i  \nska du nok trives bra i ’n  \nKinn mot kinn ska vi sett oppmed  \nKristiansten og sjå sola gå ne  \nMen – Æ veit ijt kæm  \nÆ veit ijt kor hæn du e\n\nDu søng ei salme i Warszawa  \nsom ein av tus’n, i Solidaritet  \nI fjella ved Kabul, Afghanistan  \nser du barn i uskyldig leik  \nEin høstkveld i Nicaragua  \nspælle du mjukt på gitar  \nBlant svarte vænna i Johannesburg  \nkjenne du styrken dåkk har  \nKanskje i Belfast, eller Manila  \nI Teheran, eller Guatemala  \nÆ veit at du e der  \nÆ veit du e bra  \nÆ veit det e du og æ\n\nKan æ ein gong få vis dæ byn æ bur i  \nveit æ du vil bli gla’ i ’n  \nVil du bli me gjennom byn æ går tur i  \nska du nok trives bra i ’n  \nHud mot hud ska vi gå inn i natta  \nOg natta ska vi ha i fred  \nMen – Æ veit ijt kæm  \nÆ veit ijt kor hæn du e\n\n\n\n',
                    'En gang bare en': '', 'Finale (Narr-i-ciss)': '', 'Happy jippi': '', 'Ligger vi sammen': '',
                    'Musikk': '', 'Narr-i-ciss': '', 'Ouverture (Narr-i-ciss)': '', 'Sammen på Tinget': '',
                    'Snusen': '', 'Trappa': '', 'Treningsvise': '', 'Trønderbart': '', 'Å Å Å Å': '',
                    'Bomberomrumba': '', 'Dårlig kvinne': '', 'Finale (E-de-ber)': '', 'Hagebruk': '', 'Hjemmekos': '',
                    'Opp og ned': '', 'Otto': '', 'På UKA': '', 'Reisebrev frå Flå': '', 'Sterke mennesker': '',
                    'Terrific Trondheim': '', 'Trønderrock': '![](img/uka-83-tr%C3%B8nderrock.jpg) \n\n', 'Vignett': '',
                    'Åpningssang (E-de-ber)': '', 'Det blomstrende parkometer': '', 'Dyrenes tema': '',
                    'Ei dopa ei': '', 'F-16': '', 'Finale (Fan Tutte)': '', 'Frelserens veger': '', 'Gamle hus': '',
                    'His way': '', 'I hagen': '', 'Lech Walesa': '', 'Ouvertyre (Fan Tutte)': '',
                    'Pils og slips og politikk': '', 'Trivelige Trondhjem': '',
                    'Blokkens ansikt (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1963, [Kissmett](index.asp?produksjon=1963_kissmett).  \n  \nFramført av Kjersti Lie, Haavard Gjestland, Ole Henrik Eriksen, Sverre Aam,\nTore Bye og Truls Gjestland.  \n  \nNummeret fortsetter her: [**Juryen / Han skal dømmes**](index.asp?lyd=Juryen -\nHan skal dømmes \\(Gjengangere\\)). \n\n',
                    'Calypso (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1957, [Krussedull](index.asp?produksjon=1957_krussedull).  \n  \nFramført av Knut Stenberg og ensemblet.  \nIntro: Kjersti Lie.  \n  \nSiste nummer:  \n[ **Velkomstsangen / Krokus**](index.asp?lyd=Velkomstsangen - Krokus\n\\(Gjengangere\\))  \n\n ****\n\n****\n\n\n\n',
                    'Dagdrøm - (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1955, [Vau-de-ville](index.asp?produksjon=1955_vau-de-\nville).  \n  \nFramført av Torfinn Carlsen.  \n  \nNeste nummer:  \n[ **Calypso**](index.asp?lyd=Calypso \\(Gjengangere\\))  \n\n\n',
                    'En tradisjonell forestilling i Lilleby (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nVår egen lille verden (fra UKA 1931, [Mammon-\nra](index.asp?produksjon=1931_mammon_ra))  \nFramført av ensemblet.  \n  \nFra UKA 1955, [Vau-de-ville](index.asp?produksjon=1955_vau-de-ville):  \n  \nFlatbrøst, Truls Gjestland og Tore Bye + Hilde Roald Bern og Else Barratt-Due.  \nDyd (Badeliv), Hilde Roald Bern og Else Barratt-Due.  \nDen gamle sang, Kjersti Lie, Truls Gjestland og Tore Bye + ensemblet.  \nProtest, ensemblet.  \n  \nNeste nummer:  \n[ **Trikkeførerrumba**](index.asp?lyd=Trikkeførerrumba \\(Gjengangere\\))  \n\n\n',
                    'Farvel Cirkus (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1925, [Merry go\nround](index.asp?produksjon=1927_merry_go_round).  \n  \nFramført av Ove Solum, Else Barratt-Due, Hilde Roald Bern, Lise Beate Siverts\nog Ole Henrik Eriksen.  \n  \nNeste nummer:  \n[ **Veteraner**](index.asp?lyd=Veteraner \\(Gjengangere\\))  \n\n\n',
                    'Hadjet-Larchens vise (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1919, Jazz.  \n  \nIntro: Kjersti Lie og Torfinn Carlsen.  \nHadjet-Larchen: Sverre Åm.  \n  \nNeste nummer:  \n[ **Hjemve / Tramp**](index.asp?lyd=Hjemve - Tramp \\(Gjengangere\\))  \n\n\n',
                    'Hjemve - Tramp (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nHjemve (fra UKA 1925, [Bing Bang](index.asp?produksjon=1925_bing_bang))  \nTore Bye  \n  \nTramp (fra UKA 1927, [Merry go\nround](index.asp?produksjon=1927_merry_go_round))  \nEnsemblet  \n  \nNeste nummer:  \n[**Farvel Cirkus**](index.asp?lyd=Farvel Cirkus \\(Gjengangere\\))  \n\n\n',
                    'Juryen - Han skal dømmes (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1963, [Kissmett](index.asp?produksjon=1963_kissmett).  \n  \nForsettelse av [**Blokkens ansikt**](index.asp?lyd=Blokkens ansikt\n\\(Gjengangere\\)).  \nFramført av Kjersti Lie, Haavard Gjestland, Ole Henrik Eriksen, Sverre Aam,\nTore Bye og Truls Gjestland.  \n  \nJuryen - Han skal dømmes  \nFramført av Hilde Roald Bern, Lise Siverts, Ove Solum og Trond "Toftis"\nToftevaag  \n  \nNeste nummer:  \n[ **Klubbaften**](index.asp?lyd=Klubbaften \\(Gjengangere\\))  \n\n\n',
                    'Kaldflir (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nNummeret er fra UKA 1953, [Gustibus](index.asp?produksjon=1953_gustibus).  \nFramført av Kjersti Lie og Truls Gjestland.  \n  \nNeste nummer:  \n[ **The Cnayp brothers**](index.asp?lyd=The Cnayp brothers \\(Gjengangere\\))  \n\n ****\n\n****\n\n\n\n',
                    'Karlson fra reinholdsverket (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1957, [Krussedull](index.asp?produksjon=1957_krussedull).  \n  \nFramført av Torfinn Carlsen.  \n  \nNeste nummer:  \n[ **Blokkens ansikt**](index.asp?lyd=Blokkens ansikt \\(Gjengangere\\))  \n\n ****\n\n\n\n',
                    'Klovna og sjela (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1963, [Kissmett](index.asp?produksjon=1963_kissmett).  \n  \nFramført av Kjersti Lie.  \n  \nNeste nummer:  \n[ **Livets fjær**](index.asp?lyd=Livets fjær \\(Gjengangere\\))  \n\n\n',
                    'Klubbaften (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er en parodi fra våren 1969.  \n  \nFramført av Else Barratt-Due, Hilde Roald Bern, Haavard Gjestland, Kjersti\nLie, Lise Beate Siverts, Ole Henrik Eriksen, Sverre Aam, Tore Bye og Torfinn\nCarlsen.  \n  \nNeste nummer:  \n[ **Dagdrøm**](index.asp?lyd=Dagdrøm - \\(Gjengangere\\))  \n\n\n',
                    'Livets fjær (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1969, [Prinkipo](index.asp?produksjon=1969_prinkipo).  \n  \nFramført av Else Barratt-Due, Haavard Gjestland og Lise Beate Siverts.  \n  \nNeste nummer:  \n[ **Vi har vår egen lille verden**](index.asp?lyd=Vi har vår egen lille Verden\n\\(Gjengangere\\))  \n\n ****\n\n\n\n',
                    'Nu Klinger - Debutantenes vise (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nNu klinger (fra UKA 1929, Cassa Rossa)  \nEnsemblet og Trond "Toftis" Toftevaag.  \n  \nDebutantenes vise (fra UKA 1953, Gustibus)  \nKjersti Lie og Torfinn Carlsen.  \n  \nNeste nummer:  \n[ **Hadjet-Larchens vise**](index.asp?lyd=Hadjet-Larchens vise\n\\(Gjengangere\\))  \n\n\n',
                    'Pyromanvisa (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1969, [Prinkipo](index.asp?produksjon=1969_prinkipo).  \n  \nFramført av Torfinn Carlsen.  \nTekst: Richard Solem.  \nMelodi:  "In München steht ein Hofbräuhaus" (Wilhelm ´Wiga´ Gabriel).  \n  \n  \nNeste nummer:  \n[ **Klovna og sjela**](index.asp?lyd=Klovna og sjela \\(Gjengangere\\))  \n\n\n',
                    'Rasmussens vise (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1931, [Mammon-ra](index.asp?produksjon=1931_mammon_ra).  \n  \nFramført av Trond "Toftis" Toftevaag.  \n  \nNeste nummer:  \n[ **Reimgjerdet hopsasa**](index.asp?lyd=Reimgjerdet hopsasa \\(Gjengangere\\))  \n\n\n',
                    'Reimgjerdet hopsasa (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1979, [Ræggeti](index.asp?produksjon=1979_raggeti).  \n  \nFramført av Hilde Roald, Lise Beate Siverts, Ove Solum og Trond "Toftis"\nToftevaag.  \n  \nNeste nummer:  \n[ **Pyromanvisa**](index.asp?lyd=Pyromanvisa \\(Gjengangere\\))  \n\n\n',
                    'The Cnayp brothers (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nNummeret er fra UKA 1959, [Krakatitt](index.asp?produksjon=1959_krakatitt).  \nFramført av Kjersti Lie, Knut Stenberg, Sverre Åm og Trond "Toftis" Toftevaag.  \n  \nNeste nummer:  \n[ **Karlson fra reinholdsverket**](index.asp?lyd=Karlson fra reinholdsverket\n\\(Gjengangere\\))  \n\n\n',
                    'Trikkeførerrumba (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nNummeret er fra UKA 1933, [Næmesis](index.asp?produksjon=1933_namesis).  \nOgså kjent som Den musikalske trikkefører.  \nFramført av Sverre Åm.  \n  \nNeste nummer:  \n[ **Kaldflir**](index.asp?lyd=Kaldflir \\(Gjengangere\\))  \n\n ****\n\n\n\n',
                    'Velkomstsangen - Krokus (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \n  \nVelkomstsangen (fra UKA 1951, [Akk-a-mei](index.asp?produksjon=1951_akk-a-\nmei))  \nFramført av ensemblet.  \nOrdfører: Sverre Åm.  \n  \nKrokus (fra UKA 1973, [Skubidi](index.asp?produksjon=1973_skubidi))  \nFramført av Kjersti Lie.  \n  \n\n ****\n\n****\n\n\n\n',
                    'Veteraner (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1955, [Vau-de-ville](index.asp?produksjon=1955_vau-de-\nville).  \n  \nFramført av Haavard Gjestland, Tore Bye og Truls Gjestland.  \n  \nNeste nummer:  \n[ **Rasmussens vise**](index.asp?lyd=Rasmussens vise \\(Gjengangere\\))  \n\n\n',
                    'Vi har vår egen lille Verden (Gjengangere)': '![](img/gjengangere.jpg)Opptak fra jubileumsrevyen Gjengangere, 1980.  \nNummeret er fra UKA 1931, [Mammon-ra](index.asp?produksjon=1931_mammon_ra).  \n  \nFramført av ensemblet.  \n  \nNeste nummer:  \n[ **En tradisjonell forestilling i Lilleby**](index.asp?lyd=En tradisjonell\nforestilling i Lilleby \\(Gjengangere\\))  \n\n\n',
                    'Akk og hjemve': '', 'Ayatollahs lullaby': '', 'Cassa Rossa': '',
                    'Den hydrauliske rhododendron': '', 'Erichsen': '', 'Festsang': '', 'Fossen': '',
                    'Hikkedrikkesang': '', 'Joggerock': '', 'Kassa': '', 'Las Vegas': '', 'Pianostemmerlåt': '',
                    'Prinsens gate': '', 'Reimgjerdet hopsasa': '', 'Ræggeti': '', 'Rødhette': '', 'Rørsang': '',
                    'Skogsang': '', 'Tamburinrock': '', 'Tristesang': '', 'Vampyrvise': '', 'Agent theme': '',
                    'Blue jeans': '', 'Blyg æ, nei?': '',
                    'Drømmeby - Fiskefarse': 'Drømmeby  \n  \nTekst Idar Lind, melodi Jon-Sverre Berg.  \n  \nTrondhjem, du e by´n som æ har drømt om  \n(Trondhjem) det e du som fylle drømman´ min kvar natt  \nKvar gong æ har lagt mæ og ska sov´ da veit æ at  \ndrømmen dukke opp igjen om litt  \nDrømmen om dæ  \nTrondhjem, mett mareritt  \n  \n\n* * *\n\n  \nFiskefarse  \n  \n![](img/1977_fiskefarse-foto.jpg)Tekst Idar Lind, melodi Jon-Sverre Berg.  \nPå scenen Marit Solbu (foto Fotogjengen).  \n  \n\nJa, det va torsken Findus  \nog torsken Frionor  \nDem budd på fryselag´ret  \nder alle torska bor  \nDem lå i kvar si hylle  \nmed mange torska i  \nog dem va heilt forelska  \nsom alle torska bli\n\nJa, trass i ulik hylle:  \nDem ramla så totalt  \nMen elskoven va kjølig  \nog fryserommet kaldt  \nDem lå i kvar sin stabel  \nog venta, men te slutt  \nva pinslan demmes over  \nog dem vart bore ut\n\nNo vart dæm lagt som vara  \ni sjappas frysedisk  \nDer lå dem kant i kant  \nog va forelska frossenfisk  \nOg romantikken blomstra  \nog elskov smelte is  \nOg dem vart lett bederva  \nog straks satt ned i pris\n\nJa, kjærligheit e vakker  \nog lunefull og rar  \nOg Findustorsken la  \nen tube Kavlis kaviar  \nMen akk, no kjem tragedien  \ni nok ein ny versjon:  \nFor småtorsk får du aldri  \nom du bruke prevensjon\n\nOg kæm ska skru av korka  \nfor ein torsk med ereksjon\n\n  \n  \n  \n  \n\n\n',
                    'Flosshattenes inntogsmarsj': '', 'Harens vise': '', 'Herodes´ disipler': '', 'Hun og han': '',
                    'Jakten er slutt': '',
                    'Jubileumsvelkomst': '![](img/1977_jubileumsvelkomst.jpg)Velkommen hit til jubile for Huset og\nrevyen  \ni 50 år har Samfundet vært del av denne byen  \nMen siden 1917 har studentan spilt revy  \nog samlet opp et 60-årig godt og gammelt ry  \net jubile i ny og ne er ingen overdose  \n  \nRef.:  \nChampagnekorken smeller, spill opp musikken  \nkast nå kroppen ut i rytmikken  \nla deg rives med av komikken  \nher er vår revy \n\n',
                    'Laugalaga': '', 'Mørk ballade': '', 'Nidvise': '', 'Nøkken': '',
                    'Ouverture (Laugalaga)': '![](uka/1977_laugalaga.jpg) \n\n', 'Regla': '', 'Revens andre vise': '',
                    'Revens første vise': '', 'Rødhettes vise': '',
                    'Siste skrik': 'Ja, så står jeg da bak disken, her i butikken  \nHer har vi siste skrik i jeans  \nVi kan skaffe alt du ønsker, om du følger moten  \nVi har alt som finns  \ni jeans  \n  \nEn dag står jeg ikke lenger  \nmen løper ut i gata  \nder hvor biltrafikken kjører  \nog den lyden som du hører da  \nden er mitt siste skrik  \ni jeans  \n  \n  \n\n\n',
                    'Skrap': '![](uka/1977_laugalaga.jpg)Opptak fra UKE-revyen 1977, Laugalaga.  \n  \nTekst Idar Lind, melodi Jon-Sverre Berg.  \nSolist Svein Gladsø. \n\n',
                    'Sur & blå': '', 'Tannfilevise': '', 'Tid-vise': '',
                    'Trondheim by': '![](img/1977_trondheim_by.jpg)Tekst Svein Gladsø, melodi og tekstbearbeiding\nJon-Sverre Berg.  \nPå scenen: Trond Toftis Toftevaag.  \n  \nTrondhjem by  \nEg e så glad i deg  \nÅ kor du vokser, ja du blir som ny  \nEndelig  \nså blir det skikk på deg  \nno skal du virkelig bli stilig  \n  \nNo blir du en by  \nlik kem som helst annen by  \nDe samme gater  \nsamme hus  \nog Prinsens gate blir aveny  \nRiv stygt og smått  \nBygg stort og grått  \nAlt det gamle  \nkan vi ikkje samle på.  \n  \nTrondhjem by  \nEg e så glad i deg  \nDu har jo blitt en liten perle  \nTrondhjem, å eg e så glad i deg  \n\n\n',
                    'Ulvens vise': '', 'Vals': '', 'Brainnsprøyt': '', 'Chipssang': '', 'Da-i-tida': '',
                    'Gratulasjonssang': '', 'Grønne enger': '', 'Hei Skolebakken 8': '', 'Kronelegi': '',
                    'Munkgata': '', 'Ouverture (Sirkuss)': '', 'Plattfodblues': '', 'Politidamas entré': '',
                    'Presseduett': '', 'Ryktevise': '', 'Sirkussmusikk (Finale)': '', 'Skillingsvise (Halmrast)': '',
                    'Skillingsvise (Historien gikk sin gang)': '', 'Skillingsvise (Historien går sin gang)': '',
                    'Skillingsvise (Moral)': '', 'Smilende offiserer': '', 'Studentersang': '', 'Tragisk vise': '',
                    'Trøndelag (Sirkuss)': '', 'Visa om fettet': '', 'Ansettelsesvise': '', 'Automater': '',
                    'Det er deg jeg vil ha': '', 'Det var meg': '', 'Dobbeltrensa': '', 'Eg har ei trøye': '',
                    'Ekspert(v)ise': '', 'Hundre blomstrar': '', 'Kjære gamle Basse': '', 'Kjære lille scene': '',
                    'Krokus': '', 'Livets gåte': '', 'Nær demokrati': '', 'Orden og system fallera': '',
                    'Ouvertyre (Skubidi)': '', 'Skubidi': '', 'Smile pent': '', 'Speil': '', 'Sørensens marsj': '',
                    'Tango sympatie': '', 'Trafikkvise': '', 'Trondhjæm, Trondhjæm': '', 'Alle har respekt for meg': '',
                    'Det er de fleste som dør': '', 'Du skal sprøytes full av buljong': '',
                    'Du svever fritt omkring': '', 'Et argument for det bestående': '', 'Farevise': '',
                    'Gi et svar': '', 'Jænsn å æ': '', 'Lænsmainn i Nyårk': '', 'Navnevise': '',
                    'Når du er fire år': '', 'Og byen skrek': '', 'Prostituert': '', 'Skapt for å bile': '',
                    'Skitt i by´n': '', 'Solidaritet I': '', 'Solidaritet II': '', 'Sterke røde hender': '',
                    'Tygge grus': '', 'Vi skal rehabilitere': '', 'Åja (finale)': '', 'Åja (åpning)': '',
                    'Amors piller': '', 'Bunny': '', 'Evolusjonsetyde': '', 'Finale': '', 'Gjengangere': '',
                    'Gullkalven': '', 'Livets fjær': '', 'Mutasjon': '', 'Månen': '', 'Norway fair': '',
                    'Ouvertyre': '',
                    'Pyroman': 'Solist: Torfinn Carlsen.  \nTekst: Richard Solem.  \nMelodi:  "In München steht ein Hofbräuhaus" (Wilhelm ´Wiga´ Gabriel).  \n\n\n',
                    'Gullkvartetten': '', 'MS Goddagen': '', 'Skilsmissesladder': '', 'To pils': '',
                    'The brothers safe': '',
                    'Delikat': 'Video med tillatelse fra [Fotogjengen, Studentersamfundet i\nTrondhjem](http://fotogjengen.samfundet.no/).  \n  \nJeg syns så synd på deg  \nsom går til sengs med meg.  \nJeg har deg helt i min makt.  \n  \nAt jeg får pels og bil  \nfor mine drevne smil,  \ner den fatale kontrakt.  \n  \nHar du forstått det helt, min venn.  \nDu er kun en av mange menn.  \nNår din konto melder pass,  \ntar jeg en ny.  \n  \nSå du må være flott  \nog nytte tiden godt,  \nsnart går jeg fra deg igjen.  \nDa vil du angre, min venn.  \n  \nSelv om du elsker alt  \nfor hva du har betalt,  \nhar jeg for deg kun forakt.  \n  \nJeg gir deg noe nytt.  \nSå føl deg ikke snytt.  \nHusk på, vi har vår kontrakt.  \n  \nMin posisjon er delikat,  \nså du må være diplomat.  \nJeg har min forsvarsadvokat,  \nså vær på vakt!  \n  \nGjør ingen ekstra sprell,  \njeg har deg likevel,  \nfor jeg går alltid fri, fri ...  \n  \n\n\n',
                    'Graverne': 'Video med tillatelse fra [Fotogjengen, Studentersamfundet i\nTrondhjem](http://fotogjengen.samfundet.no/).  \n  \nDet er en gammel kirkegård  \nhvor gravene står tett,  \nmen ennu er det plass til mange fler.  \nVi ser med lengsel på hver sjel  \nsom er blitt blek og trett.  \nVi vil ha mer, vi vil ha fler,  \nsom vi kan grave ned.  \n  \nVi har en gammel Daimler Benz  \nmed silkesort komfort  \nog søtlig tung kremeringskarakter.  \nDen kjører vi i femte gear  \nhjem til vår kirkegård,  \nmed stadig fler, og fler og fler,  \nsom vi kan grave ned.  \n  \nVed middagstid vi går en tur  \nblandt parkens høye trær.  \nDet gleder oss å høre barn som ler.  \nEt lite syrlig drops  \nmed arsenikk til hver især.  \nVi byr dem fler og står og ser  \npå at de svelger ned.  \n  \nEn tidsinnstillet bombe sprang  \nog flyet styrtet ned.  \nVi stod der med vår Daimler like ved.  \nTitanic ble for oss suksess,  \nvi lå med båt i le,  \nog dukket ned og hentet fler  \nog grov dem alle ned.  \n  \nEn stor del av vårt klientell  \nforspiser seg på fett.  \nOg intet er mer gledelig enn det.  \nEn kiste til en profitør  \nsom ble så alt for mett,  \nfår gullbeslag og rosa polster  \nfør den senkes ned.  \n  \nEt Hiroshima om igjen  \ndet venter vi nå på.  \nVi ser på og vi lar det gjerne skje.  \nVi skal ikke beklage oss  \nså lenge vi kan få,  \net lite stykke jord igjen  \nså vi får gravd dem ned.  \n\n\n',
                    'Justitia': 'Video med tillatelse fra [Fotogjengen, Studentersamfundet i\nTrondhjem](http://fotogjengen.samfundet.no/).  \n  \nPå tide at du ser deg om, Justitia.  \nDu er bedratt, ta bindet vekk, Justitia.  \nVerden har dømt seg selv,  \nnå vil jeg titte.  \nMen det du ser forblir hos deg, Justitia.  \n  \nEinstein sa at tid og sted er relativt.  \nÅ skille mellom løgn og sannhet - så naivt.  \nMin vekt ubrukelig,  \nmitt sverd har rustet.  \nMen dette må du tie om, Justitia.  \n  \nDet var en gang et lite land hvor alle sov.  \nSå skjedde det en ulykke - det vekket dem.  \nRegjeringen måtte gå -  \nfor noen uker.  \nHysj - la dem sove videre, Justitia.  \n  \nDet skjedde i moralens høyborg - Engeland.  \nTenk, adelen hadde natteliv, kan slikt gå an?  \nWard, stakkar, måtte dø,  \nvisste for meget.  \nHold tett med det du vet om ham, Justitia.  \n  \nI Sovjet er den frie kunst blitt politikk -  \nden brukes til å fremme Lenins dogmatikk.  \nHvor er du, Pasternak?  \nSkriver du ennu?  \n´Han kan du ikke hjelpe, fru Justitia.  \n  \nSlik har ditt navn blitt misbrukt, fru Justitia.  \nMed falske lodder på din vekt, Justitia.  \nEn taus kvinne, observant,  \nhun vet for meget.  \nMen det du vet blir aldri sagt, Justitia.  \n  \n  \n\n\n',
                    'Duell': '![](uka/1959_krakatitt.jpg)Nyinnspilling fra 1967.  \n  \nPletted blevet er vor Ære  \nVaabenskioldet er tilsmudset  \nMig bedraget har min Kjære  \nBedraget mig - - med dig!  \nDerfor maa vi duellere  \nVore Ærer renovere  \nVi hinanden perforere  \nPerforere!  \n  \nNaar man til pistolduellen gaae  \nNøle er at iakttage  \nTager man en stivet Skiorte paa  \nMed en kniplingskrage  \nRætter man derpaa sit Kalvekryds  \nFør man faar en Quindes afskeedskyds  \nSkræmme Mølden fra sin sorte Frakk  \nog sin Chapeau-Claque!  \n  \nPaa en Kværn lidt Krut formal et er  \nKuglen sændkes nedi Løbet  \nSpænder kiækt den rappe Hanefiær  \nDer af Staal er støbet  \nTørker man sig nu rundt Næsen  \nTager ud Protesen  \nSiunge derpaa Marseillaisen  \nHele Marseillaisen!  \n  \nSkrive ned den siste Villie  \nUndertægne Testamæntet  \nFolde man saa sine Fingre  \nTil et Fadervor  \nHiertet maa bli´ spar´t for et Attaque  \nNiude man en Klybe Skraatobak  \nFugter Struben med et Glass Cognak  \nLite Glass Cognak  \n  \nGriber Vaabnet udi Haanden  \nDerpaa fire Skridt at vandre  \nEt Sekund man holder Aanden  \nVænder hastigt om  \nRætte Løbet mod hinanden  \nKonsulterer nu Forstanden  \nSigte grundigt efter Panden  \nFy for Fanden  \n  \nLukker man det venstre Øie til  \nKrumme høire Pegefinger  \nStunden kommet er at aabne Ild  \nMonne vi faae Vinger ?  \nAlle broer er nedbrændte  \nKuglene de er ivænte  \nOg vi ere sagtens spændt  \nSagtens spændte!  \n\n\n',
                    'Memoirer': '![](uka/1959_krakatitt.jpg)Nyinnspilling fra 1967.  \n  \nNoen priser skjønne kvinner ....  \nAndre nyter vin....  \nBestiger kanskje steile tinder....  \nSnuser kokain ....  \nLivet byr så mange rike gleder her på jord!  \nSelv så koser jeg meg helst med et koffertmord.  \n  \nJeg tar kofferten med meg til godsekspedisjonen.  \nDet er leitt at det sjelden blir mer enn en pr. dag.  \nMen spaserturen gir meg den daglige mosjonen,  \nog det hører jo med til mitt fag....  \nPå min veg titter jeg på de skjelmske unge piker,  \nog formaner noen barn som vil slåss.  \nSå leverer jeg kofferten på sentralstasjonen,  \nden skal sendes til noen på Moss.  \n  \nSå vemodig jeg minnes den første gang jeg vandret  \nmed en koffert i hånd (svinelær med remmer små).  \nSiden er mangt og meget blitt sørgelig forandret:  \nJeg er verkbrudden, gammel og grå.  \nÅ — den jul jeg kom over den første forskjærkniven!  \nÅ — min bensag som jeg fikk av mor!  \nJa — min bensag, min kniv og en passelig stump blyrør  \nble for meg aller kjærest på jord!  \n  \nMuntre piker jeg elsket! Mitt liv det var å feste!  \nIngrid, Kiss, Jacqueline, — jeg minnes særskilt dem!  \nMen til Moss ble de sendt, — ja — i alle fall det meste..  \nOg jeg tror at det nådde vel frem.  \nAkk — en lokk nesehår og noen bleke kinner  \nvar omtrent alt jeg hadde igjen!  \nMen mitt liv fikk nytt innhold, — jeg finner atter gleder,  \njeg er flyttet inn på gamlehjem!  \n\n\n',
                    'Munke-liv': '![](uka/1959_krakatitt.jpg)Nyinnspilling fra 1967.  \n  \nSanctus Bodega — bringer regn og sne og sol  \ntørker støvet av min kubbestol og lar poteten gro  \n  \nSanctus Bodega — krøller skjegget om mitt kinn  \nog lar månen skinne inn igjennom cellegluggen min  \n  \nSanctus Bodega — du lar året dra forbi  \nvarmer brødrernes pedi i denne kolde vintertid  \n  \nSanctus Bodega — du lar markens blomster gro  \nog lar fluene få surre på vårt tomanns klosterdo  \n  \nVi er tilfredse — godt fornøyd med skjebnen vår  \nenser ei at tiden går og at vi eldes år for år.  \n  \nSom´ren er omme — årets vinhøst har vært god  \ni vår kjeller gjærer øl og vin om abbeden er tro  \n  \nHvis noen nonner — skulle vandre her forbi  \nskulle de få smake på vår årgang 1310  \n  \nOg hvis de ønsket — skulle de bli buden inn  \nog vi skulle klappe dem på baken og på deres kinn  \n\n\n',
                    'Munke-øl': '![](uka/1959_krakatitt.jpg)Nyinnspilling fra 1967.  \n  \nEn øl må man ha i en sådan stund  \n— Broder, fyll ditt krus —  \nLa fanden slå takten mot tønnas bunn  \n— syng en sang  \ntil begerklang —  \nØlet er godt og vår tørst er stor.  \nTønna er full og da synger vi i kor:  \nTa og sving din seidel, svirebror,  \nTa deg en tår når din tørst er stor  \nav det  \nSkummende  \nDuggende  \nKjølig forfriskende  \nKildeklare  \nKjernesunne  \nKjellerkalde  \nØL.  \n  \nNår seid´len er tom går en runde til  \n— Nok en runde øl —  \nNår tønna er tømt går vi ut pa dill  \n— med promill  \nog pigelill —  \nHylende kvinner på alles fang  \nØIskum fra øre til øre og vår sang:  \nTa og sving din seidel, svirebror,  \nsyng med din sugende øl-tenor om det  \nSkummende  \nDuggende  \nKjølig forfriskende  \nKildeklare  \nKjernesunne  \nKjellerkalde  \nØ L.  \n  \nMen når det så ikke er mer igjen  \n— og vår seiel er tom —  \nBesøker vi nærmeste klostervenn  \n— som ha øl  \nfullskjegg med krøll —  \nBanker vi stille påklosterets dør  \nÅpner og synger idet vi gjør honnør:  \nTa og sving din seidel, svirebror,  \ngi oss en plass ved ditt svirebord  \nog no´n  \nSkummende  \nDuggende  \nKjølig forfriskende  \nKildeklare  \nKjernesunne  \nKjellerkalde  \nØ L.  \n  \n\n\n',
                    'The Cnayp brothers': '![](uka/1959_krakatitt.jpg)Utganspunktet for nummeret var den svært populære\namerikanske sanggruppa Deep River Boys. Nyinnspilling fra 1967.  \n  \nJag traff en little flicka ifrån Lademoon, Lademoon, Lademoon.  \nJeg beliver at hun loved meg, det sade hun  \nfør hun kissed på min munn.  \nI remernber absolut det var en aftenstund jeg var extra brun, extra brun.  \nI min fang hun satt og veiet mange hundre pund  \nmens hun bubbelade bubbeligum.  \n  \nRefr.:  \nBut I can´t huske no more vad hun hade for navn  \nJeg husker kun a big volum  \nmed bubbelande bubbeligumskum.  \n  \nOh brother, tell me nå, var hennes øyne blå eller grå, - - blågrå?  \nNei, de var ganske brune ty hun tygde skrå  \narvet etter en i Gudes gate två.  \nVar hennes latter ikke rein og klokkeklar, klokkeklar, klokkeklar?  \nDet er det very plenty mulig at den var,  \nbut the walls came tumblin down.  \n  \nRefr.  \n  \nVar hun inte yr og vill og lidenskabelig, lidenskabelig, lidenskabelig?  \nShe was heller astmadisponabelig.  \nThat lidenskap var very variabelig.  \nHennes kyssar dom var just presis som dynamit, dynamit, dynamit!  \nHun bestandig nesten druknet når det regnet stritt,  \nty hun hadde slik en diger underbitt!  \n  \nRefr.  \n  \nHun trippede avsted så myeket elegant, elegant, elegant.  \nJa — nærmest som en epileptisk elefant  \nda, hennes nye ytre venstre treben brant!  \nBut I am very sure hun smilte glad mot meg, glad mot meg, glad mot meg.  \nMen ikke før hun tok din lommebok fra. deg,  \nlike før hun gikk sin way.  \n  \nRefr.:  \nBut I can´t huske no more vad hun hade for navn.  \nJeg husker kun a big volum  \nmed bubbelande bubbeligumskum.  \n\n\n',
                    'Ælg': '![](uka/1959_krakatitt.jpg)Nyinnspilling fra 1967.  \n  \nVi e´ fire kailla ifra bøgdesjøttarlaga,  \nvi e´ ut på ælgejakt.  \nVi ha leidd oss vall´ å ska skjøt rusta uta Kraga  \n— ellers e´ a bra inntakt.  \n  \nJa, vi ha glædd oss si i fjor.  \n«Det var da æ skaut a svigermor,»  \nja, det gjor vi — ja, det gjor vi —  \nja, vi skaut a svigermor.  \nHæ-hæ-hæ  \n  \nJa, no er ælgjakta endelig begynt.  \nIngen e´ skottfri — vi plaffe ne tjukt og tynt.  \nIngen ælg e´ sikker, uten´n står i tjor,  \nmen ska det lønn sæ, må ælgen væra stor.  \n  \nVi har med oss sjøttarmerke — karske-sprit og longmos,  \npiller imot diaré  \nHoin ha fått træbein — for vi skaut´n litt på Røros,  \nhain spreng like godt for det.  \n  \nJa, no e´ ælgjakta begynt,  \nvarsku her, vi plaffe ned tjukt og tynt.  \nJa, det gjør vi — ja, det gjør vi —  \nja, vi plaffe ned tjukt og tynt.  \n  \nÆlgjakta e´ kun for oss som e´ litt kvekk på labben,  \nvi et bare havergrøt.  \nE´ det nå som røre sæ, så må´n itj gjør den tabben:  \nat´n veinte med ´å sjøt.  \n  \nDa kain itj høvve vær ta tælg:  \n— Kain jo værra at det e´ en ælg.  \nKain jo værra, kain jo værra —  \nja, det kain jo vær en ælg.  \n  \nJa, no er ælgjakta endelig begynt.  \nIngen e´ skottfri — vi plaffe ne tjukt og tynt.  \nIngen ælg e´ sikker, uten´n står i tjor,  \nmen ska det lønn sæ, må ælgen vera stor.  \n  \nForri høsten va vi heldi — det va reine fæsten,  \nvi fikk lagt ned fire dyr.  \n«Æ skaut kvigan te´n Lars». «Å æ tok mæ ta hæsten».  \n«Æ vart jaga i ei myr».  \n  \nVi skaut som et artilleri —  \nMæn De sjønne, ælgen — hain gikk fri.  \nJa, det gjor´n — ja, det gjor´n,  \nja, den ælgen hain gikk fri. —  \n  \nHerre året mista vi hain diskenspringer Bratte.  \nHain satt for sæ sjøl på huk.  \n«Æ så at det glimta i ei skinke borti kratte´ —  \nplaffa laus mot ælgebuk.»  \n  \nMæn, enda va vi fire mainn,  \nså vi hadd itj nå behov for hain.  \nNei, vi greidd oss — nei, vi greidd oss.  \nDet va nok med fire mainn.  \n  \nJa, no er ælgjakta endelig begynt.  \nIngen e´ skottfri — vi plaffe ned tjukt og tynt.  \nVi fikk lagt ned Bratte, no hain søv i fre,  \n«— æ punkterte lænsmainsbila — så ho sank i kne».  \n\n\n',
                    'Calypso': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nTanken går til den skjønne vår  \nda jeg sang i mannskoret Polyfon  \ntil den turne da vi dro av sted  \nmed lokaltog fra Trondhjems sentralstasjon  \n\nVi var 20 mann pluss´n Karl Johan,  \nbeste bass i Norges land.  \nVi sang og lo så hele toget forstå  \nat vi var sangere på vei til Lundamo  \n\n  \nJeg satt ned i min togkupé  \nuten tankte for annet enn sangsuksess  \nmen vis a vis bak en dagsavis  \nsatt en pike det var noe særskilt ved.  \n  \n\nVi var 20 mann pluss´n Karl Johan ...  \n\n  \nSanger bror --- du vet sikker hvor  \njeg til da kun levet for kor og sang.  \nAkk før vi dro over Skansen bro  \nvar jeg fylt av elskov for første gang.  \n  \n\nVi var 20 mann pluss´n Karl Johan ...\n\n  \nSkulle jeg presentere meg  \neller bare prate kjekt i vei?  \nOh onde makt! Da min plan var lagt  \ngikk hun på toalettet for å sminke seg.  \n  \n\nVi var 20 mann pluss´n Karl Johan ...\n\n  \nHun kom inn med sin ferskenskinn  \nog hun satte seg ned på plassen sin.  \nVi var på Ler etter tre kvarter,  \nmen jeg satt der stum på finalen min  \n  \n\nVi var 20 mann pluss´n Karl Johan ...\n\n  \nToget stod på en ensom mo  \nog jeg glødet av heftig kjærlighet.  \nMin stemmes klang var som lerkesang  \nda jeg spurte henne hva stedet het.  \n  \n\nVi var 20 mann pluss´n Karl Johan ...\n\n  \nDa min tro fikk jeg se de sto  \npå et skilt at dette var Lundamo.  \nJeg måtte da se og hoppe av  \nmens min elskov videre med toget dro.  \n  \n\nVi var 20 mann pluss´n Karl Johan ...\n\n\n\n',
                    'Det store spill (Golf)': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nVi gikk sammen gjennom skolen  \ni den aller første vår.  \nOg vi lekte oss i solen  \nvar familiens hvite får.  \nVi var gatens fløtegutter,  \nhang i skjørtene på mutter,  \ninntil vi i moden alder  \nfant den sport som passet oss -  \n  \nGolf. — Et spill for de spreke karer  \nsom før gikk på byens barer  \nSatt hos Lunde  \nmed sin kunde,  \nog drakk dus med en hvemsomhelst.  \nNå er livet blitt et annet  \nNår vi dyrker golfens gleder,  \nslik som Oslos Bogstad-reder,  \ner vi med i det store spill.  \n  \nRefr.:  \nTra la la la la la lei  \nHere we do it the english way  \nTra la la la la la la —  \nJa, vi har det riktig bra  \nher på Sommersetera.  \n  \nVi har hver vår lille butikk,  \nsom vi driver ganske bra,  \nog er stadig vekk på utkikk  \netter nytt fra USA.  \nMens vi går omkring og lurer  \npå no´n nye agenturer  \nkan vi bile opp i 12-tiden  \nog ta et lite slag —  \n  \nGolf. — Vi har ikke energien  \ntil innsats i industrien.  \nEr for strevsomt,  \ner for krevsomt,  \nfor vi tjener allikevel.  \nVi har hver vår lille Mersche Bentz  \nmed extra Shell på tanken  \nog har penger nok i banken  \ntil å ta oss en Oslo-tur.  \n  \nRefr.  \n  \nTenk hvor gildt det måtte være  \nå ha nord-norsk filial.  \nMen da må vi nok dessverre  \nimportere kapital.  \nAlle sure pengemenner  \nblir som smør i våre hender  \nnår vi biler opp i 12-tiden og tar et lite slag, ---  \n  \nGolf. — Slik lykke vi alle føler  \nved 14 passerte høler,  \nDet er godt slått.  \nGanske flott slått,  \nog det gir oss slik fin mosjon.  \nFør vi inntar middagsmaten  \ngår vi opp på badevekten.  \nSliktno´ øker selvrespekten  \nnår man deltar i store spill.  \n  \nRefr.  \n  \n\n\n',
                    'Et annet sted': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967 med Siri Nansen Jemtland m.\nfl.  \n  \nHvis vi har skjønt hr. Platon rett  \ner alt som vi har undersøkt og sett  \nuvirkelig og bare dill  \nfor livet er et skyggespill.  \n  \nIfølge Platons tankegang  \ner jeg som står og synger denne sang  \net uttrykk for en slags idé  \nsom er et ganske annet ste´.  \n  \nHr. Korsmo er professor her på NTH, heter det.  \nMen vi vet alle og enhver  \nat han er et helt annet ste´.  \n  \nSå derfor kan vi lett forstå  \nat verden er så meningsløs og grå  \nnår selve det: å være til  \ner helt verdiløst skyggespill.  \n  \nDet rare med filosofi  \ner at såsnart et hjemmegjort geni  \nfår skrellet all fornuften vekk  \nså blir det hele klart som blekk.  \n  \nVi mener da å kunne si  \nat man skal satse mere på esprit.  \nDitt travle liv som jordisk trell  \ner likevel en bagatell.  \n  \nOg er du sur en regnværsdag  \nså grip vår lille idé  \nOg du vil med et trylleslag  \nvære et helt annet ste´.  \n  \nMed denne form for dobbeltliv  \nfår fremtiden et lystig perspektiv  \nnår vår eksamensdag tar til  \ngår vi med Platon ut på dill.  \n\n\n',
                    'Glad og fri': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nVi er en utvalgt hoppertropp  \nVi trenes i  \nå gå på ski  \nmed både sjel og kropp.  \n  \nVi hører stadig Thorleif si:  \n«Hvis du skal nå  \ntil topps da må  \ndu være gla og fri.»  \nOg nå er vi så frie så —  \nFra jobben min har jeg tatt  \nfri i 14 månter nå. Vi er på  \nkurser hele året rundt  \nVi lever godt og fritt og sundt.  \n  \nVi trosser både sol og regn  \nog slapper a´  \nog spenner fra  \nmed både sinn og bein.  \nVi hopper over vanlig strev  \nfor det er bra  \nå være gla´  \ni både sats og svev.  \nDe må´kke bruke tinningen  \nda får´u straks  \nen liten saks  \nog kluss med bindingen  \nNei, vi må være bare lykkelig,  \nhvis vi skal hoppe godt på ski.  \n  \nI Morgedal har vuggen stått  \ni sol og sne.  \nPå tross av det  \nså blir vi alltid slått.  \nDet finns jo andre som har vugga litt.  \nog derfor må  \nvi hoppe på  \nhvis vi skal holde tritt.  \nNår bakken har en tysk profil  \nså tar jeg svensk,  \nog jeg tar finsk,  \nog de tar russisk stil.  \nMen seierherren skal bli norsk en da´  \nnår vi har lært å slappe a´.  \n\n\n',
                    'Kalson (fra renholdsverket)': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nMitt navn e Kalson fra Reinholdsverket  \næ sope tidlig og sope seint.  \nOg der ´n Kalson har vært, der mærke  \ndæm bætterdø at der blir det reint.  \nMen ka det hjælpe å værra reinslig  \nnår heile væla e foill av skjit,  \ndet e da fåfængt å gå her einslig  \nmed kost og spae, og sop og slit.  \n  \nNo ska itj æ gå og harselere  \nen haug med ting æ itj har no med,  \nmen av og te må æ spekulere  \npå kolles væla e laga te.  \nDet e no bakveindt med mangt og myttji,  \ndet e no gæli med ailt som skjer,  \nså snart´n trur´n har gjort no nyttig  \nså kjæm det no´n og riv trua ner.  \n  \nJa ta æksæmpelvis vælferdsstaten  \nsom ska gjør livet så lyst og lætt.  \nDæm gir oss trygder og smør på maten  \nog barnebidrag og stæmmerætt.  \nDet sjer så rørandes ut i navnet  \ndet der med bidrag for ditt og datt,  \nmen ka e vitsen, når pængan havne  \nder kor dæm kom fra, som ækstra skatt.  \n  \nOg sje på væla og på tæknikken  \nmed sattelitter og deinslags lort.  \nNo e det straks før dæm kjøre trikken  \ndirækte opp te Sankt Peters port.  \nMæn ka bli egentlig sluttpoænget  \nmed aillt vårt jordiske stræv og mas  \nså læng vi veit at en dag så sprænge  \ndæm heile skjiten i tusen knas.  \n  \nSlik e det laga at aillt i væla  \ngår roint sæ sjøl i en evig dans.  \nFørst bli det vinter med frost og tæla  \nså bli det sommersol og St. Hans.  \nMen e det rart at´n bli forbainna:  \nså snart som gatan e fri for snø  \ngå æ og sope deinn samma sainna  \nsom æ brukt vinteren te å strø.  \n\n\n',
                    'Kjøp bil': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nAgent:  \nDagens løsen er jo speed  \nalle vil vi spare tid.  \nBønder fra Trysil og til Sogn:  \nKjøp vogn!  \n  \nDagens tempo er jo hardt  \nalt som teller, det er fart.  \nFiskere, slutt med sild og rogn.  \nKjøp vogn!  \n  \nMannens plass er bak et ratt  \nuten vogn er livet matt.  \nHold deg i takt med tidens stil:  \nKjøp bil!  \n  \nVirker vognen triviell,  \nkjøp deg da en ny modell,  \nen som har splitter ny profil.  \nKjøp bil!  \n  \nFeinschmecker:  \nEn bil kan være så lekker den vil,  \nforfinet i formen, i linjenes spill,  \net teknisk vidunder  \nen racer, en drøm,  \nen sølvpil som blinker  \ni gatens strøm.  \nDen har ingen ånd!  \n(Uten en kvinnes behanskede hånd!)  \n  \nEn bil i seg selv er en sjelløs ting,  \nglir frem og tilbake — i meningsløs ring.  \nDen blinker forgjeves  \nmed nikkel og lakk  \ndens kamp om vår gunst  \ner et flaut attakk  \nhvis den ikke har ånd!  \nNemlig — en kvinnes behanskede hånd.  \n  \nHvem husker vel bilen som raste forbi  \nmed livsnære direktør Hansen i?  \nHvem husker vel boken  \nsom bare var perm?  \nHvem husker vel bilen  \nsom bare var skjerm?  \nMen man husker en hånd  \nsom hvilte behansket på rattet  \n—skjødesløs — fjern — sånn!  \n  \nDirektøren:  \nEr du nybakt direktør  \nkjør da med privat sjåfør åttesylindret, toppventil.  \n  \nAlle:  \nKjøp bil!  \n  \nEngelsk lord:  \nHvis du er en engelsk lord  \nkjøp deg da en gammel Ford.  \nMen hvis du er en parvenue ---  \n  \nAlle:  \nKjøp ny!  \n  \nMann med ridebukse:  \nBilen er så populær  \nat den snart er blitt vulgær  \nridning det passer storfolk best!  \n  \nAlle:  \nKjøp hest!  \n  \nBonden:  \nBur du trangt og vilt og bratt  \nhøgt til fjells i knaus og kratt  \nkan du´kje leva som ein pamp.  \n  \nAlle:  \nKjøp gamp!  \n  \nFotgjenger:  \nHvorfor bli en fartens trell, -----  \ningen kjører fra seg selv.  \nVis meg en bil som målet når!  \nJeg går.  \n  \nAgenten:  \nBry deg ikke om han der  \nhan er helt reaksjonær.  \nFyren er sprø og halvt senil!  \nKjøp bil!  \n  \nAlle:  \nKjøp bil! Kjøp bil!  \n\n\n',
                    'Krussedull': '![](uka/1957_krussedull.jpg)Nyinnspilling fra 1967.  \n  \nVi har fått en gummimann  \nfyllt med vannstoff så han kan  \nleve på et høyt nivå  \nog sveve helt i det blå.  \nTenker ikke alltid på  \nhva man må og ikke må.  \nTenk om alle andre kunne det  \nså gøyalt det ble.  \n  \nDen kolde fornuft  \nden har en duft  \nsom kan gi oss vondt i magen.  \nLitt mer sympati  \nfor fantasi  \nville kanskje gjøre seg.  \nJa, tenk om man ble  \nlitt mer distre  \n— kunne drømme midt på dagen  \nog sveve til værs  \nsånn litt på tvers  \nav den slagne landevei.  \n  \nDing dang krussedulle  \nsnurrige personer  \nVi syns at de skulle  \nfå en liten sang.  \nAlle de vi kjenner  \n— sure som sitroner —  \nskal få gummimenner  \ngratis i presang.  \n  \nNå må det bli tatt  \nopp til debatt  \nom det er så galt å gjøre  \nlitt mer originalt  \nog unormalt,  \n— det som ikke helt går an.  \nJa, tenk om man sa  \nno rart hver da´  \nkanskje hjalp det på humøret?  \nSå føler du trang  \nså si ding dang  \nsom en voksen, modig mann.  \n  \nDing dang krusedulle  \nsnurrige personer.  \nVi syns at de skulle  \nfå en liten sang.  \nAlle de vi kjenner  \n— sure som sitroner —  \nskal få gummimenner  \ngratis i presang.  \n  \nEn statsfunksjonær  \nmed bare knær  \nburde ha den største gasje.  \nEn ekspeditør  \nmed godt humør  \nskulle æres med pensjon.  \nEn gøyal poet  \nav kvalitet  \nmå få gå med rød mustasje.  \nEn proff som har skjegg  \nog legger egg  \nskulle få et pent diplom.  \n  \nDing dang krusedulle  \nsnurrige personer.  \nVi syns at de skulle  \nfå en liten sang.  \nAlle de vi kjenner  \n— sure som sitroner —  \nskal få gummimenner  \ngratis i presang.  \n\n\n',
                    'Dagdrøm': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling med Tor Jemtland fra 1967.  \n  \nJeg har aldri vært en glad student,  \njeg må heller stå som eksponent  \nfor den store duskemassen,  \nden som ingen tenker på.  \n  \nJeg var full av lyst til å ta fatt  \nNår jeg hjemme på min hybel satt,  \nog jeg så meg selv i ånden  \nsom et midtpunkt her i salen stå.  \n  \nI min formannsperiode  \nvar det ei den episode  \nsom jeg ikke mestret flott.  \nJeg ble alltid møtt med heder,  \njeg var født den store leder,  \nog var venn med flere av datidens store personligheter,  \njeg nevner i fleng: Gabriel Scott,  \nJeg la opp et helt semester  \nmed et veld av store gjester,  \ndet var virkelig nivå.  \nOg som toppen på suksessen,  \nble jeg skrevet om i pressen,  \nog tatt opp blant Sorte Får.  \n  \nMen for slike gleder ble jeg snytt,  \nikke en gang omtalt i Studenternytt,  \ni den store duskemassen  \ner man liten blant de små.  \nJeg var full av lyst til å ta fatt  \nnår jeg hjemme på min hybel satt,  \nog jeg så meg selv i ånden  \nsom et midtpunkt her på scenen stå.  \n  \nJeg var proppfull av talenter  \nog var en av de studenter  \nsom ga Trondheimsvisen ry.  \nSelvsagt var jeg og forfatter,  \nhele salen gråt av latter,  \ndet var virkelig revy.  \nDet skal nerver til å tåle  \nprojektørens skarpe stråle,  \nmed salongen fullt besatt.  \nJeg ble matt av all applausen,  \nog ble gratulert i pausen,  \nog tatt opp som Gylden Katt,  \n  \nMen for slike gleder ble jeg snytt,  \nteater passet ikke helt for mitt gemytt.  \nI den store duskemassen  \nblir talenter dysset ned.  \nIkke alle kan få laurbær på sin vei,  \nhva var vel de store gutta uten meg.  \nDET VAR MEG SOM SØRGET FOR APPLAUSEN  \nnår de store inn i salen skred.  \n\n\n',
                    'Den gamle sang': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling fra 1967.  \n  \nDen gamle sang fenger,  \nden tids gode refrenger —  \n«Oh Sweetheart, don´t you love me any more?»  \n  \nDen gamle sang minner  \nom tider som forsvinner —  \nde skjønne tider som ei mer består.  \n  \nDen gang man gikk på vaudeville,  \nmed spaserstokk og med skalk,  \nda man gikk arm i arm  \nog trykket til sin barm  \nsin pigelill så varm.  \n  \nDen gamle sang fenger  \nden tids gode refrenger —  \n«Oh Sweetheart, don´t you love me any more?»  \n  \nKan du huske den gang,  \nførste gangen vi sang  \nden gamle melodien,  \nDet er lenge, lenge siden.  \n  \nVi blir unge igjen  \nnår vi nynner på den.  \nDen var vårt store nummer  \nfra vår store tid, den rommer  \n  \nminner, om forførende kvinner  \nom den gangen vi drømte om  \nvår pigelill så varm.  \n  \nKan du huske den gang,  \nførste gangen vi sang —  \n\n\n',
                    'Kossemos': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling fra 1967.  \n  \nMel.: En sømand har sin ene gang....  \n  \nStem opp, stem opp en månesang  \nom luftfart og teknikk,  \nom himmelrom og forskertrang  \nog sfærenes musikk,  \nom vårs som kom fra Lilleby  \nog ville sette seg  \net minnesmerke udi sky,  \nhan Andersen og jeg.  \n  \nFra Lilleby med knall og brak  \nhan Andersen og jeg  \nfår opp og splintra himmærns tak,  \n— da skreik vi hu og hei!  \nNå er vi mer sånn vemodsfylt,  \nti udi mørkets rom  \nvi snurrer som en liten bylt,  \nog flaska mi er tom.  \n  \nOg mannen i den månen her  \nskal lissom værra meg,  \nja, bortsett ifra Andersen,  \nmen han er blitt så kjei.  \nHan nekta først å værra med,  \nhan sa det var no tull  \nå måtte værra ny og ne  \nog ikke alltid  \n  \nEn jordens træl jeg alltid var,  \nnå er den tid forbi.  \nEt himmellegeme jeg har  \nsom gjør det koselig  \nå kaste ned på byens trær  \nog elskovsparras vei  \net lissom lett forheksa skjær  \nfra Andersen og meg.  \n  \nSå seiler vi i rottasjon  \nhan Andersen og jeg  \nog speller litt på grammafon  \npå vitenskabens vei udi  \ndet store kossemos  \nog natt og stjerneskjær.  \nMen ingen kan fortelle oss  \nhva vi skal gjørra der.  \n  \nJa, ja, godnatt da, Andersen, jeg ser deg vel i morra-tidlig.  \n\n\n',
                    'O-la-la': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling med Per Sjølie fra 1967.  \n  \nMel.: C´est magnifique.  \n  \nDetter er mer enn jeg ventet å se,  \nløv, kastanjetrær  \nlike under den evige sne.  \nFolk i pene klær.  \nHer fins alt fra musikkpavillion  \nlike til trikk, jernbanestasjon.  \nLuften er paradisisk varm,  \nalt har en egen parisisk charme.  \n  \nHer er en duft  \nsom røver all fornuft,  \no-la-la-la,  \njeg er beruset.  \nMed pling, pling, pling  \ngår trikker rundt omkring,  \no-la-la-la,  \njeg er forbauset.  \nOg piker går  \nforbi med lysblondt hår,  \njeg er helt fortryllet.  \nHer er charmant,  \njeg tror knapt det er sant,  \njeg er beruset.  \n  \nSkjønt det er Lilleby, ikke Grandville,  \nhøres der vis a vis  \nførsteklasses pianospill,  \n— ja, så sannelig.  \nHer er visst ikke en kannibal,  \nisbjørnfaren er nok minimal,  \nalle kvinner er ondulert,  \nmennene vasket, salonbarbert.  \n  \nDet er en duft  \nsom røver all fornuft,  \no-la-la-la,  \njeg er beruset.  \nMen pling, pling, pling  \ngår trikker rundt omkring,  \no-la-la-la,  \njeg er forbauset.  \nOg piker går  \nforbi med lysblondt hår,  \njeg er helt fortryllet.  \nHer er charmant,  \njeg tror knapt det er sant,  \njeg er beruset.  \n  \nUndres hva han fordyper seg i,  \nhan på benken der?  \nLærebøker i filosofi!! ?  \nJeg får fluer her.  \nFor en kvinne, så lys som en fe!  \nPiken: S´il VOUS plait, monsieur!  \nHan: Merci, mademoiselle!  \nC´est formidable, elle parle francais.  \nNei, nu mister jeg min forstand,  \nføler meg som en sardin på land.  \nDet går i ring,  \ndet sier singeling.  \n0-la-la-la,  \nc´est fantastique.  \nOg trikken roper  \ntingelingeling,  \nc´est comme en France.  \n\n\n',
                    'Presten': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling med Eigil Nansen fra 1967.  \n  \nDe hilser. De hilser bestandig på presten,  \nskjønt få av dem egentlig tror hva han sier.  \nMen ingen vil jo holde på den gale hesten,  \nog spå kan man hverken om ener eller tier  \npå livets forunderlige totalisator.  \nSå kjøper man i stillhet en tokroners bong  \npå meg, en outsider, «From Senator»,  \nifall jeg skulle gå opp i denne sesong.  \nDet kunne jo skje. Jeg er ikke så lubben  \nsom ifjor. Jeg kunne for å holde meg til denne sjargong,  \npassere både «Doktor» og «Dollargubben».  \n  \nSå hilse, det gjør de, og letter på hatten,  \nmen satser det meste på de trygge favoritter.  \nSelv de som mumler på et Fadervår om natten,  \nde dyrker om dagen sine renter og kreditter,  \nkjører sine biler og snyter på skatten.  \nDe tviler, de fleste, på den kirkelige lære.  \nDet nytter ikke skjenne det ringeste grann på dem.  \nDe enser ikke meg — ja, det måtte da være  \nhvergang de får barn, og ber meg skvette vann på dem.  \nOg hvergang det kommer en yndig, ung brud  \nsom syns det er tryggere liksom å spe på  \nmed orgel og salmer og snehvitt skrud  \nog tyve venninner i ryggen — til å se på.  \n  \nMen ellers står kirken og samler på støvet.  \nI høyden er den en slags katakombe  \nfor slike som skjelver som aspeløvet  \nhver gang det springer en splitter ny bombe.  \nJa, den ja --- skal være så god blir det sagt,  \nsom håndfast og slående argument  \ni diskusjonen om djevelens makt,  \nden er så å si som fra himmelen sendt,  \nså alle kan tippe den riktige hesten  \nog for alvor begynne å hilse på presten.  \nJeg nekter å tro at denslags greier  \nkan bringe vår sak noen varig seier.  \n  \nMen hvorfor blir jeg da her -- likevel,  \nog steller med de store og små profeter.  \nJeg undres i blant om jeg tror på dem selv.  \nJeg kunne visst like godt dyrke poteter.  \nMen nei. Jeg blir. Og ingen skal få meg  \nherfra, og aldri kaster jeg kappen og kraven  \nså lenge de hilser på meg....  \nOg det gjør alle. For alle skal i graven.  \nJa, det står fast. Og si hva da vil,  \njeg tror nok at det ble en vanskelig ting,  \nden dag ikke jeg hjalp til.  \nSe derfor er vi en usynlig ring,  \nog derfor ser du oss alltid vandre  \nsammen, som fremmede, -- og hilse på hverandre.  \n\n\n',
                    'Sportsfiskeren': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling fra 1967.  \n  \nHvis du har fått en flekk på hjernen,  \nog det er aldeles umulig å fjerne´n,  \nog du ikke greier å viske bort´n,  \nda er det bare en ting som hjelper,  \nog det er forsyne meg — fiskesporten.  \nVel å merke, hvis man har utstyret i orden:  \nVadere, varmt undertøy, sammenleggbar hov,  \nditto klepp, fiskekurv og minst to stenger,  \nhelst tre, — ørretstang, tohånds laksestang  \nog slukstang. Vaselin, nål og tråd.  \n  \nMan blir lei av menneskene, ikke sant?  \nDe er så dumme, farer helst med tøv og tant,  \ndet er så mange materialister  \nav den sure, griske sorten.  \nVi har dem her i byen og,  \nog mot dem vet ikke jeg annen råd enn fiskesporten.  \nMen utstyret, det må´n ha i orden:  \nSplitcanestang, — bambus holder ikke, snakeringer,  \nagat toppring og korkhåndtak med fluefeste.  \nOgså må det være ordentlig snelle, helautomatisk  \nmed laksegir og snørefører. Også en liten tutt her  \npå siden. Og husk: det må være dyre saker.  \nJa, også en ting til: kordestål i slukstanga.  \n  \nLivet er så ensformig her i staden,  \nde samme ansikter å se på gaten,  \nså mye smålighet og sladder, tisk i porten.  \nMot sånt fins det bare et eneste botemiddel,  \nog det er, gud hjelpe meg, fiskesporten.  \nMen jeg må innprente det med utstyret: Førsteklasses  \nsnøre, dobbelttapered nylon, og nailen fortom, flueboks,  \nen til tørrfluer og en til våtfluer. Tørrflueolje så  \nflyter fluen bedre. Apropos fluer, så vil jeg overlate  \ndet til den enkelte. Der spiller personligeheten en viss  \nrolle. Selv har jeg gjort gode erfaringer med Green-  \nwells Glory. men jeg nekter ikke at en March Brown også  \nkan ha sine fordeler.  \n  \nNå er jo saken den, at fisk fins det som bekjent  \nikke, selv har jeg aldri fått en eneste en, ikke  \nen eneste en, men fisket har jeg. Også har jeg  \nhatt utstyret iorden. Og ikke en eneste gang har  \ndet hendt meg at jeg har fått backlash, og det er  \nviktig. Meget viktig. Kanskje det viktigste av alt.  \n  \n\n\n',
                    'Veteraner (Det var i 1905)': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling fra 1967.  \n  \n(Melodi: Den tapre landsoldat)  \n  \nDet var i 1905, det var i 1905,  \nvi dro med fynd og klem, ja, vi dro med fynd og klem.  \nDet var i 1905, vi dro med fynd og klem,  \ndet var i 1905 at vi dro ut med fynd og klem.  \nOg spør du når vi dro ut, så var det 1905,  \nog spør du hva vi dro ut med, så var det fynd og klem.  \nOg da det vel var slutt, så ble det festsalutt,  \nda vi dro hjem igjen.  \n  \nDen gang vi dro avsted, den gang vi dro avsted,  \nKrag-Jørgen tok vi med, ja, Krag-Jørgen tok vi med.  \nDen gang vi dro avsted, Krag-Jørgen tok vi med.  \nDen gang vi dro avsted så tok vi alle Krager´n med.  \nOg spør du hvor vi dro hen, så var det langt avsted,  \nog spør du om Krag-Jørgen, så hadde vi den med.  \nOg jaggu ble det skutt, en kraftig festsalutt,  \nda vi dro hjem igjen.  \n  \nVår appetitt var fresk, vår appetitt var fresk,  \nvi spiste kjøtt og flesk, ja, vi spiste kjøtt og flesk.  \nVår appetitt var fresk, vi spiste kjøtt og flesk,  \nvår appetitt var fresk, vi spiste erter, kjøtt og flesk.  \nOg spør du om vi åt, så var appetitten fresk,  \nog spør du hva vi åt, var det erter, kjøtt og flesk.  \nFor god og kraftig mat, det trenger en soldat,  \nsom er på grensevakt.  \n  \nDa vi en dag dro hjem, da vi en dag dro hjem,  \ndet var med fynd og klem, ja, det var med fynd og klem.  \nDa vi en dag dro hjem, det var med fynd og klem,  \ndet var i 1905, at vi dro hjem med fynd og klem.  \nVi husker godt vi dro hjem med veldig fynd og klem,  \nog tar vi ikke feil, var det nittenhundreogfem.  \nDa hørtes uavbrutt vår glade festsalutt:  \nHurra, hurra, hurra!  \n\n\n',
                    'Vuggevise': '![](uka/1955_vau-de-ville.jpg)Nyinnspilling fra 1967.  \n  \nSov, hr. ordfører, hvil Dem en stund.  \nIngen vil nekte Dem rett til en blund.  \nHøyremann, venstremann, sosialist,  \ntrøtt -- det blir alle i hop til sist.  \ndiar seg en svipptur til slu.mreland.  \nSov, hr. ordfører, sov mens De, kan.  \n  \nSov, hr. ordfører, glem politikken,  \nbyskatt og femørestillegg på trikken,  \ntøysprat, og tullprat i dagens debatt,  \nden som tilslutt gjorde hjernen matt  \nuten å gagne det ringeste grann.  \nSov, hr. ordfører, sov mens De kan.  \n  \nDrøm, hr. ordfører, drøm at engang  \nverden blir renset for unødig tvang,  \nvelgerhensyn og denslags krøll.  \nDrøm at du tar deg en ordentlig øl.  \nEllers så går det jo bare på vann.  \nDrøm du, ordfører, drøm mens du kan.  \n  \nDrøm at du svever på englers vis  \nrundt i et hvitt sosialt paradis  \nhvor alle er innskrevne medlemmer i  \net kjempestort kristelig folkeparti,  \nog du er dets ledende mann.  \nSov, kjære ordfører, sov mens du kan.  \n  \nSov, hr. ordfører, hvil ifra strid.  \nIngen er mer enn et barn av sin tid.  \nHøyresak, venstresak, hva er vel det?  \nAlt er som fotspor i nyfallen sne.  \nDråper i tidens bunnløse spann.  \nSov, hr. ordfører, sov mens De kan.  \n\n\n',
                    'Debutantenes vise': '![](uka/1953_gustibus.jpg)Nyinnspilling fra 1967.  \n  \nVi er komedianter  \nkveldens tre debutanter  \nførsteklasses representanter  \nhåper på klapp og applaus.  \n  \nMødre, onkler og tanter  \nfyller flere kvadranter  \nsitter som sekundanter  \nhåper på klapp og applaus.  \n  \nSe mot taket! Gå på rett maner!  \nHevet hake! Dans og deklamer!  \n  \nSelv som kunstens drabanter  \nfrykter vi kverulanter  \nkjære onkler og tanter  \ngi oss litt klapp og applaus.  \n  \nVi har skaffet billetter  \ntil kusine og fetter  \nhele byen er etter  \noss som får klapp og applaus.  \n  \nVi har øvet dager og netter  \nredusert til skjeletter  \nlevd på sterke tabletter  \nfor å få klapp og applaus.  \n  \nSkjelv i knærne, -- fjas-ko? nei suksess  \nDet er dere som bestemmer det.  \n  \nNu når forteppet detter  \ngår vi hjem og ser etter  \nom avisen beretter  \nbare om klapp og applaus.  \n\n\n',
                    'Kaldflir': '![](uka/1953_gustibus.jpg)Nyinnspilling med Siri Nansen Jemtland og Tor\nJemtland fra 1967, disse framførte også visa i 1953.  \n  \nJaggu er det trist om da´n,  \ndårlig lite mord og ran,  \nmen vi er ør og spenna gal  \nfor vi har vært på cowboyfilm på Rosendal.  \n  \nÅåååå — Ååååå  \nfra vi kom og til vi gikk så sa det: Bang.  \nÅåååå — Ååååå  \ngjennom lufta suste glass og møblemang.  \n  \nOg hele tia så sto´n Rogers bare og kaldflira.´  \n  \nUten noe dikkedar  \nrydda´n hver en jævla bar,  \ndengte skurken uten skån,  \nså ikke en gang mora kjente trynet på´n.  \n  \nÅåååå osv.  \n  \nOg hele tia osv.  \n  \nRogers klatra med gitar  \ninn i damas boudoir,  \nen som prøvd´ å jekke´n ut  \nrei ut gjennom døra på en kulesprut.  \n  \nÅåååå — Ååååå  \npå et blunk ble gitar´n bygd om til kanon,  \nÅåååå — Ååååå  \ndet er´ke verst å bruke plekter som patron.  \n  \nMen Rogers var ikke dårligere kar enn at han spelte på´n etterpå, han.  \n  \nØrkensand og måneskinn,  \nRoger hviska: «Er du min?»  \nDem smelta sammen i et kjøss  \nå dægern å dem klina gitt, ja dra til sjøs.  \n  \nÅåååå — Ååååå  \nhele salen satt og stønna, ja dem hvein,  \nÅåååå — Ååååå  \nog på galleri satt søstra mi og grein.  \n  \nMen selv midt i kjøsset så hadde´n Rogers ene handa på pistolen.  \n  \nHvor skal vi få penga fra  \ntil kino, røyk og ukebla?  \nSelge skjorta på auksjon,  \nfor til mandag er det Hopalong med mod´rasjon.  \n  \nÅåååå — Ååååå  \nFolka trur at vi er splitterpine gal,  \nÅåååå — Ååååå  \ncowboy er og blir vårt store ideal.  \n\n\n',
                    'Multeplukkeren': '![](uka/1953_gustibus.jpg)Nyinnspilling med Hans Kristiansen fra 1967.  \n  \nUnnskyld meg, men er det noen  \nsom har sett en rubus her i trakten,  \net eksemplar av disse gule små,  \nsom fjellet nu i år skal være fullt´a,  \nsom fortrinnsvis har myren som sitt voksested,  \nog på folkesproget også kalles «multa».  \n  \nDen burde være velkjent,  \nden gjør jo megen gavn  \nsom føde.  \nJeg tenker særlig da på dens funksjon  \nsom efterrett og syltetøy på brødet.  \nMed rubus chamæmorus er man neppe så fortrolig,  \nDet er dens videnskapelige navn.  \n  \nFamilien er god: Rosaceae.  \nDens blad er nyreformet, rynket, fliket,  \nog blomsten troner som en fjellets engel  \npå toppen av en ru og båret stengel.  \n  \nJeg nevner disse ting, fordi det ei bør glemmes  \nav dem, for hvem en multe kun er mat,  \nsom regner den i kilo og i masse,  \nat først var blomsten der - med farver og med em.  \nEn blomst, som fikk sin plass i det naturlige system  \nda Linne i sin tid gransket den, og satte den i klasse.  \n  \nMen tro nu ikke bare at på grunn av denne viden  \nkan jeg ikke se en rubus fra den spiselige siden.  \nÅ nei så tvert imot, men jeg er ikke blant dem  \nsom mener at å plukke er en grafsen og gramsen,  \nen faren løs på myrene med fnys og med fres,  \nen geberden langt verre enn selveste bamsen.  \n  \nDet er da flere hensyn som må tilgodesees:  \nman tar ikke en rubus som ikke slipper hamsen,  \nman ofrer da imellem en tanke på smaken,  \npå duften, på fargen, på fjellets majestet.  \n  \nNaturen er ensom, den trenger vår fortolkning,  \nden lengter etter våre sange.  \nAv multer er der få, og tar man altfor mange,  \nfornærmer man den stedlige befolkning.  \n  \nJavisst, de er få, men plukker man med ettertanke  \nog med varsom hånd  \nog i den rette, beskjedne ånd,  \nog hitter om bare et eneste bær,  \nda finner man kanskje sin glede der,  \nden sanne glede, ja nettopp det  \nsom romerne kalte: non multa, sed multum.  \n  \nJa leter man bare — hva sa jeg. Jo se!  \nder står det jo en i sin modne sødme.  \nDen eier nettopp den fine rødme,  \nden gylne saftighet som preger  \nen rubus som villig forlater sitt beger.  \nDen tar jeg.  \n  \nSe der, der har jeg den omsider. Nu er den min.  \nJeg gjemmer den til trøst i hårde tider.  \n\n\n',
                    'Utrøndersk virksomhet': '![](uka/1953_gustibus.jpg) \n\n',
                    'Åpningsvise (Lille meg)': '![](uka/1953_gustibus.jpg)Nyinnspilling med Siri Nansen Jemtland fra 1967, hun\nsto også på scenen i 1953.  \n  \nJeg skal kvede en smule til åpning.  \nJeg er for så vidt den skuffete forhåpning.  \nDere har jo børstet smokingen og vandret mann av huse,  \ndere ventet kanskje visen med det store store suset.  \nDere tenkte vel som så, at nå skal det jamen smake  \nmed litt virkelig sirkus og Napoleonskake.  \n  \nOg så fikk dere bare lille meg.  \n  \nJa, det er vel no´ pussig med livet,  \ndet er så ofte litt falskt i perspektivet.  \nMan kan drømme i sin ungdom  \nom å bli den store mester,  \nom å likne dirigenten for det mektige orkester.  \nMan kan fable om å rokke ved Jerikos murer  \nmens trompetene jaller og basunene durer.  \n  \nOg så blir det ikke mere enn et pling.  \n  \nOfte trøster jeg meg hjemme på kottet  \nmed stille håp om at hun som bor på slottet  \nkan bli lei av alle tjenerne som leker troll i eske,  \nkanskje er det hennes drøm å komme hjem med shoppingveske  \nstikke nøkkelen i døren til en enkel liten bolig,  \nog ta gutten sin om halsen og hviske så fortrolig:  \n  \nMin elskling, her har du lille meg.  \n  \nNå er det slett ikke tanken å ville  \nha sagt at jeg er det store i det lille.  \nSaken er jeg bare står her for å synge litt og nynne  \ndette lille som skal til for at revyen kan begynne.  \nMitt fineste poeng er det noen som har kvarta,  \nmen det gjaldt om å få trykt ut at nå har vi altså starta.  \n  \nOg den jobben den fikk da lille jeg.  \n\n\n',
                    'Byggstudent Havre': 'Nyinnspilling med Per Sjølie fra 1967. Tekst Hans Kristiansen.  \n  \n  \n\n\n',
                    'Flathundens sang': '![](uka/1951_akk-a-mei.jpg)Nyinnspilling med Tor Jemtland og Berent A. Moe fra\n1967.  \n  \nJeg er en hund med komodeben,  \nflat og fin og raseren.  \nNå skal jeg synge en liten sang  \nom hvorfor jeg er så flat og lang.  \n  \nSaken den er ganske enkelt sånn  \nflathet er jo tidens ånd.  \nFlathet og lathet og hengende vom  \ndet er alt det det dreier seg om.  \n  \nFør var det fint å være myndehund  \nmed lange ben og et «vovv» i munn.  \nMyndehunden var en åndsgigant,  \nformet tanken lett og elegant.  \n  \nNå er det mote med komodeben,  \nflat og fin og raseren.  \nNorge er blitt til et flathund-land  \nog flathunder er vi alle mann.  \n  \n  \n  \n  \n  \n\n\n',
                    'Hatten': '>\n\n',
                    'Hybelvisa (I et bittelite rom oppå loftet)': '![](uka/1951_akk-a-mei.jpg)Nyinnspilling med Tor Jemtland fra 1967. Han sang\nogså originalen.  \n  \nI et bittelite rom oppå, loftet  \nhar jeg seng og bord og vaskestell  \nog et skap med dress og lusekofte,  \nmen jeg koser meg likevel, — ja, jeg koser meg likevel.  \n  \nFra mitt vindu ser jeg snorer med laken,  \ningen skoger, ingen blåe fjell,  \nbare muren grå og kald og naken, —  \nmen jeg koser meg likevel, — ja, jeg koser meg likevel.  \n  \nOg her i ramme har  \njeg som min gjest  \nvertinnens gamle far på skytterfest.  \nHan stirrer ned fra min vegg  \nog mumler lurt bak sitt skjegg:  \n  \nI et bittelite rom oppå loftet  \nhar vi seng og bord og vaskestell  \nog et skap med dress og lusekofte,  \nmen vi koser oss likevel, — ja, vi koser oss likevel.  \n  \nJeg har knekkebrød og ost neri skuffen  \ntil min frokost som jeg steller selv.  \nJeg har bare margarin på loffen,  \nmen jeg koser meg likevel, — ja, jeg koser meg likevel.  \n  \nStundom ønsker jeg meg kaffe på senga  \nfor det er så trist å koke selv,  \nkaffe er´ke med i månedspenga,  \nmen jeg koser meg likevel, — ja, jeg koser meg likevel.  \n  \nOg borti kroken bor  \nsom venn og gjest  \nen liten musemor, —  \nhun liker best  \net stykke flesk og litt rull,  \nmen piper lell fra sitt hull:  \n  \nVi har knekkebrød og ost neri skuffen  \ntil vår frokost som vi steller selv.  \nVi har bare margarin på loffen,  \nmen vi koser oss likevel, — ja, vi koser oss likevel.  \n  \n\n\n',
                    'Morgenhymne': '![](uka/1951_akk-a-mei.jpg)Nyinnspilling fra 1967.  \n  \nFram kamerater mot den nye dag.  \nFortiden sover i sin sarkofag.  \nFram, fram, fram, slå et slag.  \n  \nSolo:  \nJa, det må vi jaggu gjøra.  \n  \nFølge sola  \ntil hu stuper,  \nstuper i havet.  \n  \nSolo:  \nOg så på´n igjen den neste morran.  \n  \nVeien den går igjennom støv og slam.  \nHåpet er alltid bakom fjellets kam.  \nDriver oss videre fram.  \n  \n  \n  \n  \n\n\n',
                    'Ouverture': 'Nyinnspilling fra 1967 med Kringkastingsorkesteret. (Komponist er\nsannsynligvis Per Hjort Albertsen.)  \n\n\n',
                    'Professormonolog': 'Nyinnspilling med Hans Einar Bøhm fra 1967.  \n  \n  \n\n\n',
                    'Velkomstsang (med tale)': 'Nyinnspilling fra 1967.  \n  \nVelkommen hjem, herr diplomingeniør,  \nAldri har vel bygda vært så lykkelig før.  \nFor nå har Anders kommet hjem,  \nNå har vi deg å vise frem.  \nVelkommen hjem, herr diplomingeniør,  \nAldri har vel bygda vært så lykkelig før.  \nFor ingen andre bygder har slik en sønn,  \nDu er vår stolthet og vår rikeste lønn.  \nNå skal du snu på jorda,  \nFlytte sola.  \nHeia Anders,  \nHeia Anders,  \nHeia Anders,  \nHipp, hipp, hipp, hurra.  \n\n\n',
                    'Vosserull (Gutane frå Voss)': '![](uka/1951_akk-a-mei.jpg)Nyinnspilling fra 1967.  \n  \n1\\. Eg er berre snill.  \n2\\. Eg går aldri på dill.  \n3\\. Eg køyrer aldri heim i drosjebil.  \nAlle: Vi er meire lur,  \ndrar til hytta på tur,  \nkjem aldri her på salen trøytt og sur.  \n  \nRefr.: Gutane frå Voss  \ndei er rett så populære.  \nGutane frå Voss  \ner dei beste utav oss.  \n  \nGutane frå Voss  \ndet er karar som er svære.  \nGutane frå Voss  \ndei kan prata som ein foss.  \nOg når vi har ein festleg kvell  \nmed spikekjott på bordet,  \nda høyrer vi på hardingspel  \nog trøyter tida vel.  \n  \nGutane frå Voss  \ndei er rett så populære.  \nGutane frå Voss  \ner dei beste utav oss.  \n  \n  \n\n\n',
                    'Drikkevise (Oppe i et juletre)': '![](uka/1949_domino.jpg)Nyinnspilling fra 1967.  \n  \nOppe i et juletre  \nsatt en elg i fred,  \ntygget talglys til den ble  \nveldig lei av det.  \nHvordan den skal komme ned  \nskjønner ikke je´.  \nIkke bry deg, men gi tål,  \ntalgelysets skal!  \n  \nNede i et badekar  \nsatt en pinnsvinfar  \npå et skittent putevar  \nog med pompen bar.  \nHvordan han får skrubba seg  \nskjønner ikke jeg.  \nIkke bry deg, men gi tål.  \npinsevinens skål!  \n  \nRundt omkring en enerbusk  \nløp et lommerusk.  \nTørket sved og annet snusk  \nav sin pannebrusk.  \nAffor´n ikke brukte bil  \n— skjønn det den som vil.  \nIkke bry deg, men gi tål,  \nlommeruskets skål!  \n  \nNede i en balje tom  \nsvømte Vilhelm om.  \nHvis det hull i baljen kom,  \nVilhelm straks kom om.  \nHvordan han får pudra seg  \nskjønner ikke jeg.  \nIkke bry deg, men gi tål,  \ntulleballets skål!  \n  \n\n\n',
                    'Duett på Baklandet': '![](uka/1949_domino.jpg)Nyinnspilliing fra 1967. Melodi: Per Hjort Albertsen.  \n  \n1\\. Jeg er trøtt, jeg vil hjem.  \n  \n2\\. Du er støtt  \nen av dem  \nsom har det med å miste piffen!  \n  \n1\\. Å, hold opp med sånt vrøvl!  \n  \n2\\. Ikke sitt der og snøvl,  \nmen se å få lått fart i biffen!  \n  \n1\\. Morgenstund er full i munn.  \n  \n2\\. Ser du månen - god og rund!  \n  \n1\\. Den gule osten er jeg lei a´.  \n  \n2\\. Hei, kan du si meg hvor det blei a´  \nden stjernen som nyss seilte  \nover halve himmelkuplens hvelv?  \n  \n1\\. Nei, i mitt eget kuppelhue har jeg nok av stjerner selv.  \n  \nArie:  \n  \n2\\. Knapt jeg merker 1\\. Hodet verker,  \n2\\. det er sent på natten 1\\. jeg er full som katten.  \n2\\. Se, min sønn 1\\. Jeg er grønn  \n2\\. hvor dagen gryr. 1\\. Jeg vet hva det betyr.  \n  \n1\\. Du falske poet, nå rusler vi hjem  \ntil hyblen med dynen og sengen.  \n  \n2\\. Ja, der har du rett, nu går vi til dem,  \nog enes i denne refrengen:  \n  \n1., 2. Hva er vel ære og palass  \nog søte pikebarn en masse,  \nhva er vel dram og fulle glass  \nmot sengens fjærende madrass?  \n  \nKor: Hvor i verden du er  \ner det en du har kjær.  \nO, det er sengen, sengen, sengen, sengen, sengen,  \nsengen, sengen, sengen, sengen.  \nO, du min seng.  \n  \n1\\. Hvor i verden du er  \ner det en du har kjær.  \n  \nKor: O ja, det er sengen — — —  \n  \n2\\. Hvor i verden du er  \ner det en du har kjær.  \n  \nKor: :/: O, ja, det er sengen. :/:  \n  \nKor: Om du mistet hver venn  \nalltid en ble igjen.  \nO, det er sengen — — — osv.  \n\n\n',
                    'Kroverten': 'Nyinnspilling med Per Sjølie fra 1967.  \n  \nJeg husker så mangen en kveld fra før.  \nJeg gjemmer på minner som aldri dør.  \nJeg sto her og så på den glade kankang  \nog lyttet til ungdommens sorgløse sang.  \nJeg sang den vel selv  \nfortumlet en kveld  \nmed glasset på bordet og piken på fang.  \nJeg sang den vel selv en gang.  \n  \nMin tone er stilnet. Mitt hår er grått.  \nJeg står og betrakter den vei jeg har gått.  \nJeg står og ser ungdommen toge forbi.  \nJeg minnes dens lykke og melankoli.  \nJeg minnes en drøm,  \nså ung og så øm,  \nen tindrende jubel med vemodstreif i.  \nEn drøm er mitt Tivoli.  \n  \nMin vakreste drøm er den tid som var.  \nOg spør du om den, skal du straks få svar.  \nMen spør du om livsgleden ennu er til,  \nda er det mitt håp: den har bare gått vill.  \nNår kommer du, venn,  \ntil jorden igjen  \nog muntrer oss tiden med sang og med spill  \nog nører den gamle ild?  \n\n\n',
                    'Morgenvise': '![](uka/1949_domino.jpg)Nyinnspilling med Berent A. Moe, Kjell Lund og Nils\nHaugstvedt fra 1967.  \n  \nSju mann i gata og plass for elefanten.  \nVi er litt glade for vi kommer fra fest,  \nog glasset var fullt, så vi titta over kanten.  \nNå går vi heimatt gjennom storm og blest.  \nMen dypt i sin seng sover piken på sitt øre  \nog faderen våkner av skrålet og røret,  \nmen sovner igjen med en gang han får høre  \nat gutta er ute i fra N. T. H.  \n  \n  \n\n\n',
                    'Talekoret (Brede seil)': 'Innspilling fra 1967. Skrevet av Bjørnstjerne Bjørnson i 1861. Nummeret ble\nførste gang vist på et lørdagsmøte i 1948, men ble vurdert som så bra at det\nble inkludert i UKE-revyen 1949.  \n  \nBrede seil over Nordsjø går;  \nhøyt på skansen i morgnen står  \nErling Skjalgsson fra Sole, -  \nspeider over hav mot Danmark:  \n«Kommer ikke Olav Trygvason?»  \n  \nSeks og femti de drager lå,  \nseilene falt, mot Danmark så  \nsolbrente menn; - da steg det:  \n«hvor bliver Ormen lange?  \nkommer ikke Olav Trygvason?»  \n  \nMen da sol i det annet gry  \ngikk av hav uten mast mot sky,  \nble det som storm at høre:  \n«hvor bliver Ormen lange?  \nkommer ikke Olav Trygvason?»  \n  \nStille, stille i samme stund  \nalle stod; ti fra havets bunn  \nskvulpet som sukk om flåten:  \n«tagen er Ormen lange,  \nfallen er Olav Trygvason.»  \n  \nSidenefter i hundre år  \nnorske skibe til følge får,  \nhelst dog i måne-netter:  \n«tagen er Ormen lange,  \nfallen er Olav Trygvason.»  \n\n\n',
                    'Brannmannssprøyt': '![](uka/1947_fandango.jpg)Nyinnspilling med Per Sjølie fra 1967.  \n  \nRektinokk så e æ gammel brannmainn,  \nmen likevel så kainn æ no bli harm.  \nD´e tredve år si´n æ sto i kulissan  \nfør første gang å venta på alarm.  \nÆ ha hørt mangen rævy å my studentersang,  \nmen æ syns dæm itj e som dæm va før.  \nNo søng dæm itj om ainna enn fart å futt å klang.  \nfor dæm trur de et gammelt, ækt humør.  \n  \nRefreng:  \nItjno e som gamle ting i Trondhjæm,  \nd´e patina´n som avgjør saken her,  \nå nye ting må ældes litt før dæm bli populær,  \n— på gamle minna e Trondhjæm miljonær.  \nItjno e som tradisjon i Trondhjæm,  \nd´e fortidsminnesmerka alt du sjer  \nsom dæm hoill på å kultiver´ å driv å reparer´,  \n— alt bli gammelt å trøgt å godt, — ka kainn vi ønske mer?  \n  \nVær-i-tass å Jazz å Cassa-Rossa  \nRa-ta-tah, Bing-Bang å Baccarat  \ndæm laga mye arti spell på tross a´  \ndæm itj hadd´ no sånt utstyr som i da´.  \nDe va en annen tone, de va en egen ånd  \ndenne tia da storkaran regjert´,  \nno syns æ feite glosa å skryt tar overhånd --  \nå sånt oppkok e bætterdø forsert!  \n  \nDi forstår at æ kainn bli forbainna  \nnår karan stå å song sånt tøys å toill,  \nslik at æ ta sprøyta mi i hainda  \nå bruke a litt mere enn æ skoill.  \nFor kainn da itj studenteran forstå at de itj går  \nå få laga no nytt i gammel dragt,  \ndæm må nokk prøv å produser´ no nytt — som om noen år  \nkainn bli gammelt å godt å anti sagt ...  \n  \nRefreng:  \nItjno e som gamle ting i Trondhjem, o. s. v.  \n\n\n',
                    'Kontiki-song': '![](uka/1947_fandango.jpg)Vi er i drift  \npå Stillehavets blå,  \nhåper å finne  \nnoe kultur snart.  \nHer er så varmt,  \nmen det er ikke rart,  \nfor det er sol-  \nskinn hele dagen lang.  \n  \nPalmer vi ser  \npå fjerne øer stå,  \nmen vi har ikke  \nlov å ro bort dit.  \nDen ø vi skal  \ntil må nok komme hit,  \nfor det er joks  \nå gjøre noe selv.  \n\n\n',
                    'Regnværsserenade': '![](uka/1947_fandango.jpg)Nyinnspilling med Berent A. (Bente) Moe fra 1967.  \n  \nDet er vann vi pusser tenner i  \nog blander i cement  \nog vasker våre hender i,  \ndet er fra himlen sendt.  \nSom damp det går til værs igjen  \nog blir til regnværssky,  \nså drypper det på deg min venn  \nog på din paraply.  \nOg skyene i øst og vest  \nde strømmer i mot nord,  \nde liker seg nok aller best  \nder hvor studenter bor.  \n  \nRefr.:  \nDe vil alltid innom Trondhjem  \nfor det er en hyggelig by,  \nden har lave trehus  \nog søte piker,  \nså har du engang vært der,  \nvil du søke dit på ny.  \nDu vil aldri glemme Trondhjem!  \nSelv om du forlater den,  \nvil ditt hjerte bindes,  \nalltid minnes  \ndenne by som ble din venn!  \n  \nDen luften som vi puster i,  \nsom er i sykkelring,  \nsom kjøkkenkniver ruster i,  \nsom bærer fugleving,  \nden luft som fuktig, klam og kold  \nseg trenger gjennom klær  \nog hyler høyt i dur og moll,  \nsom storm og vind i trær,  \nden luft som farer opp og ned  \nog tørker klær på snor,  \nden har et yndlingsblåsested  \nher oppe i mot nord.  \n  \nRefr.:  \nDen vil alltid innom ...  \n  \nNår vi har tatt diplomen vår,  \nså sier vi adjø  \nog tar vår hatt og frakk og går.  \nVi tjener selv vårt brød.  \nVi spres (som løv i en taifun,  \nsom korn for såmanns hånd,  \nsom erter fra en trekkbasun)  \nfra Moss til Babylon.  \nJa, livet er komplett hasard  \nhvor alt er i det blå,  \net lykkehjul på en basar;  \nmen en ting kan jeg spå:  \n  \nRefr.:  \nDu vil engang innom Trondhjem ...  \n\n\n',
                    'Skapelsen': '![](uka/1947_fandango.jpg)Nyinnspilling fra 1967.  \n  \nFra [Vår egen lille verden](index.asp?vis=1910-85): Fandango (1947) står i ei\nsærstilling blant etterkrigsrevyene. I ei tid da landet skulle bygges opp\nigjen, og i en by der NTH var et midtpunkt, retter denne revyen en kraftig\nadvarsel mot det å la seg fascinere for sterkt av teknikken. Forfatterne er\ntydelig påvirka av Aldous Huxley og andre likesinnede, og revyen advarer mot\n«tekniske roboter» ukritisk bruk av vitenskapen, oppdragere i sin\nalminnelighet (foreldre, lærere, agitatorer) og ny opprustning.  \n  \nJeg er alltid trøtt og sliten  \nvondt i hue´ òg,  \nholder nok slett ikke mål.  \nTrenger søvn og mat,  \ner alltid låk og lat,  \nnei, en skulle være gjort av stål.  \n  \nRefr.:  \nRobin, Robin skal vi lage,  \ndet skal bli en grepa kar.  \nMen´skets ånd og stålets styrke  \nskal bli hans mor og far.  \nUhyre sterk og mandig  \neksepsjonelt forstandig.  \nJa, en mann  \nsom virk´lig kan  \narbeide for folk og land.  \nRobin, Robin skal vi lage  \nmen´skeånd med kropp og stål.  \nMed all tidens kløkt og kunnskap  \nskal vi (nok) nå vårt mål.  \n  \nVerden vår er full av lengsler  \nelskov eller hat  \nmenneskenes skrik og skrål.  \nLidenskap har preget  \nvår verden alt for meget,  \nNei, en sku´ ha et hjerte gjort av stål.  \n  \nRefr.:  \nRobin, Rohin du skal bane  \nveien for den nye tid.  \nRobin, Robin med teknikkens  \nkalde kraft og flid.  \nHan kan´ke le og smile  \nbehøver aldri hvile,  \nslag i slag  \ni stadig jag  \narbeider han natt og dag.  \nRobin, Robin, heng i gutter,  \nskru ham sammen, gjør ham klar.  \nHan skal bli et barn av tiden,  \n(skal) bli en grepa kar.  \n  \nVi har slitt og strevet lenge  \nfor å lage ham,  \nja, vi har måttet gi tål.  \nMen nå har vi snart  \ngjort allting ganske klart,  \nja, nå har vi gjort en mann av stål.  \n  \nRefr.:  \nRobin, Robin har vi laget  \n\\---  \n\\---  \nse: Nå rørte han på seg!  \nRobin, Robin, snart så går du  \nfram på livets veg.  \nIntet blir utrolig,  \nfor deg er allting mulig,  \nhvor du står  \nog hvor du rår  \ner du den som alt formår.  \nRobin, Robin, vitenskapen  \nskaper her det nye liv.  \nTidens krav er kun at mannen  \nskal bli effektiv.  \n\n\n',
                    'Jakob på drømmestigen': 'Nyinnspilling fra 1967.  \n  \nSiden jeg den første gang  \ndrømte denne enkle sang  \nlangt tilbake i en svunnen tid,  \nhar så mang en Jakob hatt  \nslike drømmer dag og natt,  \nhiget opp mot høydene med flid.  \n  \nDu kan drømme deg bort fra en verden  \nsom er kjedelig, frynset og grå.  \nTrinn for trinn opp på stigen går ferden,  \ndit hvor himmelen alltid er blå.  \n  \nDu som før var forsømt  \nkan bli stor og berømt,  \nog du kjenner det svulmer i ditt bryst!  \n  \nMen så står du igjen nedpå jorda  \nog du er bare Jakob som før.  \n  \nHøstens store sensasjon  \ndet var valg og nom´nasjon,  \ndrømmestigen fikk da stor trafikk.  \nParti «ditt» og parti «datt»,  \nalle trygt i sadlen satt,  \ndet var klart at alle flertall fikk.  \n  \nMitt parti hadde beste programme´  \nog på listen stod jeg selvsagt først.  \nMine motstandere ble så tamme,  \nnår de hørte min lokkende røst.  \nJeg korn helt sikkert inn,  \nog gikk opp flere trinn,  \njeg ble statsråd og derpå fylkesmann.  \n  \nSom bekjent kom jeg ikke på tinget,  \njeg står nede på jorda igjen  \n  \nAlle kjenner sikkert meg,  \nfor på drømmestigens vei  \nhar jeg gått i mange herrens år.  \nTrinn for trinn har jeg gått opp,  \nhåper å nå stigens topp  \nså jeg engang bispestolen får.  \n  \nDa jeg drog var jeg temmelig sjabby,  \nmen jeg visste å komme meg opp.  \nI fra Finnmark til Westminster Abbey,  \ngikk min ferd til berømmelsens topp.  \nMen så kom jeg da hjem  \nog var en iblandt dem  \nsom gikk rundt med en bisp i magen sin.  \n  \nNå er Norge atter fritt  \nlandet er blitt mit og ditt.  \nSeieren er vår og krigen slutt.  \nMidt i seierens gledesrus  \nligger verden nesegrus  \ni beundring for at vi holdt ut.  \n  \nVi er en av de store nasjoner  \nsom skal reise en verden påny.  \nLille Norge med tre millioner,  \nhar nå endelig vunnet sitt ry.  \n  \nI en kjempestor ring,  \ngår allverden omkring.  \nJakob Nordmann som sentrum og som sol.  \n  \nMen en dag står vi atter på jorda,  \nog er en av de små slik som før.  \n\n\n',
                    'Mannjevning': 'Nyinnspilling med Dag Romlien og Nils Slaato fra 1967.  \n  \nØ: Kongens klær og  \nreim på bringa  \nbætteldress og  \nbil med bensin  \nSigurd Storkar  \ner vel namnet  \npå deg nå?  \n  \nS: Skjærio hur  \nmår du grabben  \nlang i maska  \nsid i rompa.  \nIkkje stå å  \nglo på Hæren.  \n  \nØ: Alle late  \nLærvelarver  \nstakk som sjuke  \nskremte skarver  \nut av landet  \nfor å ete,  \ndrikke, elske  \nSvenskens mat og  \nSvenskekvinsen  \n  \nS: Lite lokka  \nmat og kvinnfolk  \nkrigens kaute  \nkarske karar  \ndei som streid for  \nfred og fridom,  \nsleppte slepp og  \nbomba byer,  \ntenkte støtt på  \nsigerns sæle.  \n  \nØ: Maten minka  \nmøyer magrast  \nsveltihæl og  \nsvindsott herja.  \nTysketauser,  \nsagflisstomp og  \ntreullbrok, det  \nvar triste ting  \nå takast med.  \nKåte kvinnfolk  \ntobbaksrøyk og  \nsjokolade  \nhøvde helte-  \nhugen betre.  \n  \nS: Vi tok turen  \nover grensa  \nfor å vinne  \nveldig siger.  \nTrente trutt og  \nøvde leiken.  \n  \nØ: Våpenleik og  \nmerkejakt, var  \ndet kamp og strid?  \nDet blinker bjart  \npå bringa di,  \ner det sigerns  \nadelsmerker?  \nFeige Farmenn  \nflydde landet,  \nskaut til måls og  \nsleit ut støvler,  \nog kom heim med  \nrutebåten,  \nmens vi heime  \ntamde tyskern.  \n  \nS: Temja temmer  \ntamde tamt.  \nLite streid du,  \nmen trygg og treg  \nkom du fram da  \ntyskern tapte.  \nFantepakket,  \ngrøne griske  \ngaukegriser  \nlanga du dem  \nut av landet?  \n  \nØ: Skog og villmark  \nvar vår heimstad,  \nsvelt og sakn vi  \nmåtte tåle.  \nSverige, London,  \nslepp og bomber,  \ngagna det om  \nalle rømte?  \n  \nS: Vi var med på  \nverdens valen,  \nvant for Norge  \nkjeks og gudvill,  \ngraut til gryta,  \nmat til magan,  \nære, ry og  \nklær på kroppen.  \n  \nØ: Kjerringer og  \nfleire onger  \ndrog du heim der  \nsveken Solveig  \nsatt og venta.  \n\n\n',
                    'Pia og soldaten': 'Nyinnspilling med Pusa Lefring og Kjell Foss fra 1967.  \n  \nFra [Studenter i den gamle stad](index.asp?vis=SIT%201910-60): At revyer har\nsin egen betydningsfulle oppgave, viste en fint ironisk, men samtidig grotesk\nscene: En engelsk soldat har et henrivende møte med en trønderpike som\noverveldes av gaver, alt slikt som hun har måttet savne: sigaretter,\nsjokolade, silkeundertøy og parfyme. Han taler det sobreste engelsk, hun et\nherlig trønderengelsk. Men da hun får ikke ett par, men to par silkestrømper,\nda slår hun armene om halsen på ham og utbryter stormende takknemlig:\n«Liebling!» Spør om publikum «tok» denne belysning av et delikat emne.  \n\n\n',
                    'Åpningssang': '![](uka/1945_go-a-head.jpg)Nyinnspilling fra 1967. Melodi Hans Bangstad.  \n  \nFra [Studenter i den gamle stad](index.asp?vis=SIT%201910-60): Alle de i\nTrondheim boende ingeniører og arkitekter stilte seg til disposisjon for Uka.\nPremieren fant sted 10. november 1945. Og da fallskjermstudentene i\nåpningsscenen løsnet beltet på reglementsmessig måte (instruert av engelske\nmilitære) og ut mot en overbefolket Samfundssal slynget sitt: Go-a-head! Go-a-\nhead! [...] da slo takknemlighet opp mot disse teatergutta som når Samfundet i\nen vanskelig situasjon kaller på dem, gjør det umulige mulig. Det var\ngjenreisning!  \n  \nGO-A-HEAD. GO-A-HEAD  \nDet er valgsproget i vår revy:  \nSett i gang alle mann,  \nla oss vise vi kan  \nfå vår verden helt normal på ny.  \nGO-A-HEAD GO-A-HEAD  \nRiv og rusk og pirk i all elendighet,  \nslik som vi gjør det her  \nmed litt hipp til en og hver.  \nGO-A-HEAD, Ja, GO-A-HEAD  \n  \nGO-A-HEAD. GO-A-HEAD  \ner refrenget de 3 store har.  \nKom de hit fikk de se  \nhvordan slikt no´ bør skje.  \nDe kom etter i vårt fotefar.  \nGO-A-HEAD. GO-A-HEAD  \nsynger folk, men de gjør slett ingenting.  \nMen vi viser dem nå  \nrette veien de skal gå.  \nGO-A-HEAD, Ja, GO-A-HEAD  \n  \nGO-A-HEAD. GO-A-HEAD  \nReis vårt land helt på fote igjen.  \nAlle mann tar et tak  \nfor den herlige sak,  \nsom skal samle både by og grend.  \nGO-A-HEAD. GO-A-HEAD  \nSpar deg aldri, ta et tak, ja så det svir,  \nfor et krafttak må til  \nskal vi oppnå det vi vil.  \nGO-A-HEAD, Ja GO-A-HEAD!  \n  \n\n\n',
                    'Drikkevise (La det gå som det vil)': '![](uka/1939_tempora.jpg)Melodi: Ragnvald Graff.  \n  \nVi av vikingers blod har den fuktige skikk  \nat vi gjerne vil drikke iblandt.  \nVåre penger forsvinner i skummende drikk,  \nbare tørsten er alltid konstant.  \nMen er pengene borte så tar vi på borg,  \nfor studenten er freidig og fri.  \n  \nRefr.:  \nLa det gå som det vil,  \ndet er øl som må til.  \nD´er utrolig hvor tørst man kan bli.  \n  \nByens piker de er jo så søte og små.  \nDet har sikkert nok mange erkjent,  \nog utallige er disse pikene nå  \nsom blir hengende ved sin student.  \nBare jeg har´ke fått mig non pike her nord,  \nblir vel peppersvenn hele min tid.  \n  \nRefr.:  \nLa det gå som det vil o.s.v.  \n  \nStår eksamen for døren så henger vi i  \nover bøkene tidlig og sent,  \nog vi håper nok at resultatet må bli  \nmeget bedre enn vi har fortjent.  \nKanskje står jeg tilbake så ribbet og rar  \nnår eksamen engang er forbi.  \n  \nRefr.:  \nLa det gå som det vil o.s.v.  \n  \nDen olympiske nektar, den nordiske mjød  \nfår vi tappet direkte fra fat.  \nOg er ølet tilstede, er tørsten kun søt,  \nt.or til drikk er jeg alltid parat.  \nLa kun verden få vandre sin skjeveste gang  \ndet er lenge før alt er forbi.  \n  \nRefr.:  \nLa det gå som det vil o.s.v.  \n  \n\n\n',
                    'Duett': 'Melodi: Ragnvald Graff.  \n  \nHan:  \nI allverdens vakre riker  \nfinns det mange smukke piker.  \nDet er ingen som jeg liker  \nfor jeg elsker jo bare deg.  \nDu er deilig som himlens engel  \nsom en rosenknopp på sin stengel,  \nsig mig syns du det er forengel-  \nighet å tro at du elsker mig?  \n  \nHun:  \nDu er helten i mine tanker  \nhvor mitt bævende hjerte banker.  \nSammen skal vi nu kaste anker  \nudi kjærlighets trygge havn.  \nPå min skjæbne du skal få trone  \nsom min konge med spir og krone,  \nog så er jeg din lille kone  \nsom du tar i din sterke favn.  \n  \nFrem til alteret skal jeg glird  \nlett og yndig som en sylfide  \nved din mandige sterke side  \n— Tenk at lykken er kun for to.  \n  \nHan:  \nHvilke øine som folk skal gjøre  \nnår til alters jeg skal dig føre  \nDu med blomster og løv bak øret,  \njeg i blådress og brune sko.  \n  \n\n\n',
                    'Gerd og Ottos vise': 'Nyinnspilling med Mette Kindt og Finn Andvik fra 1967, begge sto på scenen i\nTempora.  \n  \nOtto: Goddag, her er vi, vi er Gerd og Otto!  \nVi er underveis på en fin-fin turné,  \nhumør og kulør er bestandig vårt motto,  \nog reisen er blitt en success!  \nav de store.  \nGerd: Book Jensen og Rose med spillemenner  \nHerbert og alle det andre dro først  \nmen Otto og Gerd de har tusen av venner  \nså våres success blir nok størst.  \n  \nO: Og vi skal kjøpe et kostbart og skjønt palé  \nG: med åtte piker og tjener i grønn livré.  \nKor: Ja, sammen skal vi to nyte frukten av successen  \nnår vi engang blir ferdig med turnéen!  \n  \nO: Du skal få bisam og smykker og caddilac  \nG: og flotte rober med skinn både for og bak.  \nKor: Hver aften får vi roser, tulipaner, orchidéer  \nsom er større enn på andre folks turnéer!  \nG: Vi reiser rundt omkring  \nog synger rare ting,  \nog publikums beundring den er stor.  \nO: Vi synger vår duett  \ni fistel og falsett  \nrundt land og strand, i syd såvel som nord.  \n  \nG: Vi kjøper landsted og seilbåt og ridestall  \nO: Har soiréer med fest og champagneknall...  \nKor: Ja, sammen skal vi to nyte frukten av successen  \nnår vi engang blir ferdig med turnéen!  \n  \nG: Vi synger bedårende søte sanger  \nom bestemors have og søster og bror  \nog folk, de har jublet så mange ganger  \ntil luftslott på månen og hytten der nord!  \nO: Vi lager den flotteste lyd med nesen  \ndet klinger som banjo, gitar, saksofon ...  \ndessuten har vi et tekkelig vesen,  \nog kan synge, med mikrofon!  \n  \nO: Ja, folk beundrer og klapper til mig og Gerd.  \nG: Vi tjener penger som gress på vår store ferd.  \nKor: Og når vi kommer hjem så gjør vi ikke noe lenger  \nmen bare går omkring og bruker penger.  \n  \nO: Vi drar på reiser til Syden, og driver dank.  \nG: Til Monte Carlo og sprenger roulettens bank  \nKor: Ja, sammen skal vi to nyte frukten av successen  \nnår vi engang blir ferdig med turnéen!  \n  \nG: Til London og Paris,  \nog Rom, naturligvis,  \ntil Nizza og Neapel vi drar.  \nO: Middelhavets sol,  \nVenedig i Gondol,  \nog måneskinnssonate fra gitar.  \nG: Og vi skal bo på hoteller av første rang  \nO: og nyte lykken i elskov og vin og sang.  \nKor: Ja, sammen skal vi to nyte frukten av successen  \nnår vi engang blir ferdig med turnéen!  \n  \n\n\n',
                    'Holberg-monolog': '![](uka/1939_tempora.jpg)Nyinnspilling med Edvard Welle-Strand fra 1967, han\nsto også på scenen i Tempora.  \n\n\n',
                    'Barbereren fra Ila': '![](uka/1937_var-i-tass.jpg)Nyinnspilling med Arne Vikan og Arne Bratt fra\n1967.  \n  \nOthello: (bass)  \nAk, i hvilken stjerne stod det  \nslik pris skrevet på mitt hode  \n\n  \n\nCarlos: (tenor)  \nGuld, — hvad er vel det! Gud give  \njeg kun kom herfra i live,  \nEi i mine leveda´r  \nvel behandlet mig har  \nslik slyngel og. barbar  \n  \nOthello:  \nNei, de´rke mulig,  \nd´er helt utrulig  \nat det er mig som er blitt skamklippet så gru´lig  \nMen slikt no´ må man  \nforstå kan  \n´ke gå an;  \nsånn som De klipper  \nklapper  \nog klemmer  \nog klyper mig stakker.  \nsom var så vakker.  \nMitt hår forsvant  \nog månen rant  \nnu står jeg sant  \nå si her som en raka fant.  \n  \nBarber: (bass)  \nDet var da fanken  \nom den der manken  \npå to tre hårstrå skulde volde hjertebanken.  \n  \nOthello:  \nOm håra enn var få,  \ndet er da måte på  \nslik å  \nbarbere,  \nbrodere,  \nfrottere,  \nfrisere,  \nmassere,  \ngrassere,  \nskalpere,  \nskamfere en mann.  \n  \nThackskiegg: (bass)  \nTider er gått,  \ndet siste hurtigtog til Skansen henrullet.  \nHåret blev grått  \nog skjegget vokste mens De gikk omkring og sullet.  \n  \nCarlos:  \nTror kanskje De  \nat jeg skal bli her evig?  \nDa tar De  \nfomlete,  \nfamlete,  \nfusentast,  \nfryktelig feil.  \n  \nBarber:  \nHvad er min brøst?  \n  \nTutti:  \nAt krumme hår på andres hoder er din styrke.  \n  \nBarber:  \nGives ei trøst?  \n  \nTutti:  \nDu har bragt skam og skjendsel over stand og yrke.  \n  \nSåpegutt: (tenor)  \nTross all min bønn  \ner ei min lønn forhøiet.  \nDu skulde  \nklynges  \nog klenges  \nog slynges  \nog slenges ihjel  \n  \nBarber:  \nAlt står mot mig, alle mener  \ndøden er hvad jeg fortjener. --  \nSå hav takk da, kam og knive  \nfor hver gledesstund i livet.  \nSaks, - gjør du ditt arbeid bra.  \nKlipp kun livstråden av.  \nFarvel! - Jeg drar herfra.  \n  \nTutti:  \nSlik fant han døden,  \nden gode barber i Trondhjem.  \nSonet er brøden.  \nGid himlen må ta hans ånd hjem.  \n  \nSåpegutt:  \nVi har glemt å tenke  \npå hvordan det går hans arme enke.  \nOg han har jo barn, de stakkars små  \n  \nCarlos:  \nsom nu står på  \nbakke bar,  \nog har  \nei lenger far.  \n  \nTutti:  \nDet er oss som har forvoldt hans død.  \nVi er skyld i barn og kones nød;  \nnu må vi gi barberbarna brød.  \n  \nOthello:  \nTanker  \nvanker,  \nbanker;  \ngrå hår mig i skjegget setter.  \nSøker,  \nspøker,  \nøker  \nangsten i de lange netter.  \n  \nTutti:  \nHan vil spøke,  \nevig søke  \noss med skjebnen kam.  \n\n\n',
                    'Missing links vise': '![](uka/1937_var-i-tass.jpg)Nyinnspilling med Rolf Jacobsen fra 1967.  \n  \nFra [Studenter i den gamle stad](index.asp?vis=SIT%201910-60): Den\nantifascistiske tendens var denne gang ytterligere understreket. Hva revyen\nville fortelle, ble derfor tydelig nok i scenen med «The missing link» som\nbåde var båret oppe av fin artistisk smak og dyp ironi. Mens nordlyset flammet\nover ham, følte vi med stigende uro at forskjellen mellom ham og\nnutidsmennesket kanskje ikke var så stor som vi hadde innbilt oss.  \n  \nJeg er Missing Link. Ja jeg  \ner stamfar til menneskene på jord.  \nFolk er stadig efter mig,  \nmen ingen er kommet mig på spor.  \nAlle lærde lurer: Har jeg kraketær?  \nEller horn i siden? Kanskje halefjær?  \n  \nHa - ha - ha - ha -  \n  \nRefr.:  \nIngen vet nå hvor Missing Link er gjemt.  \nDem graver her, graver der: ja la dem grave!  \nIngen skal nok fa se mig inneklemt  \ni et skap som no´ skrap fra gamle dage.  \n  \nJeg er fredløs, - uten hjem.  \nJeg får ikke Nansen-pass engang:  \nAlle vil ha «Stamfar» frem:  \ndem håper nok jeg ligner Don Juan  \nDem fant mig på Sumatra. det var´ke spor av tvil  \nmen så var det bror min, - han Trinil!  \n  \nHa - ha - ha - ha -  \n  \nRefr.:  \nIngen vet ---  \n  \nLarmen mig fra Ila drev,  \nden ristinga gjorde meg rar  \nTil helleristning blev hvert brev  \nog rista brød er´ke mat for en voksen kar  \nOg da dem drev og grov under Telegrafen gitt  \nfikk dem nesten tah i beinet mitt  \n  \nHa - ha - ha - ha -  \n  \nRefr.:  \nIngen vet ---  \n  \nNu er jeg den rene fant  \nalt jeg eide har dem gravet frem.  \nHer forleden år forsvant  \nmin siste shilling til British Muse´m.  \nMen nu har jeg fått hybel med bad og full pensjon  \nnede i kong Gløshaug´s region  \n  \nHa - ha - ha - ha -  \n  \nRefr.:  \nIngen vet ---  \n  \n  \n\n\n',
                    'Vise ved innvielse av Trondhjems bombesikre kjeller': 'Nyinnspilling med Rolf Jacobsen fra 1967.  \n  \nKilder er ikke sjekket, men det er grunn til å anta at dette handler om «det\nunderjordiske», altså det offentlige toalettet på Torvet.  \n  \nTrondhjem jo bestandig er  \nbyen hvor det noe skjer  \natter kommer vi med norgespremier´.  \nVi har nu fått satt istand  \nved hjelp av bisp og fylkesmann  \nførste bombesikre kjeller i vårt land.  \nSkrevet står: Der skal en kule ril en trønder,  \nmen det klinger ikke lenger riktig bra.  \n  \nRefr.:  \nNu er kuler blitt for små,  \nvi har bedre motto nå:  \nDer skal bomber til en trønder av i dag.  \n  \nDøtre seks og sønner tolv,  \nen av dem var Tordenskjold,  \ndenne tapre helt med trøndermot i bryst.  \nDa han på «Galeien» gikk  \nsvensken bittert føle fikk  \nat Tordenskjolds kanoner lynte langs hans kyst.  \nEngang sprang han ut i bølgens salte vover  \nog omkring ham sang kulene sin sang.  \n  \nRefr.:  \nNu er kuler ...  \n  \nTordenskjold er vandret hen,  \nmen vi har jo helter enn,  \nriktignok så kjemper man jo helst med penn.  \nI Adressa sitter Gnist,  \nkan´ke like en jurist  \nog han Skjånes som han tror er korrupist.  \nMen han skjønte at her kom det an på skytset,  \ndenne gang blev det for smått med en petit.  \n  \nRefr.:  \nNu er kuler ...  \n  \nRundt omkring i øst og vest  \nherjer krigens grumme pest,  \nderfor er blandt alle lande hjemme best.  \nVed vår borgerplikt har vi  \nskaffet oss et sikkert hi,  \nhvor vi søke kan i krig og trengselstid.  \nNu kan fienden bare spare sig — på kruttet,  \nnu har byen fått sitt bombesikre rum.  \n  \nRefr.:  \nNu er kuler ...  \n  \n\n\n',
                    'Studentervise 1935': 'G.:  \nJeg går på bygg.  \nB.:  \nOg jeg på maskin.  \nBegge:  \nBegge søkte vi kjemi´n,  \nmen vi forstår  \nat hvor vi enn går  \nså blir det slit i mange herrens år.  \nSulten og trøtt  \nmed øia halvt på gløtt,  \npå forelesning må vi støtt.  \nDertil må vi  \ntegne nydelig  \nså d´ erke grenser for vår arbeidstid.  \n  \nRefr.  \nVi tegner og regner og roter dagen lang  \nog pugger og nigrer om natten mangen gang.  \nNei vår tid er jaggu mager  \nmot de gamle dager.  \nda gutta på høiskolen stelte for sig selv,  \nDe tullet og fyllet i Cirkus natten lang,  \nog kranglet og ranglet mangen gang.  \nDe arbeidet mer på «Palmeny, enn pa skolen,  \nmen det gikk så fint allikevel,  \n  \nG.:  \nJeg bygger vei  \nover dal og hei,  \ndammer, broer tårn, (B.:) og jeg  \nstrever besatt  \nbåde dag og natt  \nmed en turbin som skal ha gear og ratt.  \n  \nBegge  \nStål og betong!  \nfunkisfasong!  \nfly til månen i ballong!  \nMen De forstår,  \nat hvad vi enn foreslår,  \nså sier proffen «Tror De dette går?»  \n  \nRefr.  \n  \nB.:  \nTenk om James Watt  \npå Høiskorn hadde gått  \nog korreksjon av proffen fått.  \nHans dampmaskin  \nsku jaggu blitt fin  \nhvis noen proff en dag fikk fingra i´n.  \nG.:  \nMangen farao  \nhviler i ro  \ni pyramider ingen proffer forestod.  \nBegge:  \nVi blir bestemt  \nnervøs og beklemt  \nog vår eksamen statisk ubestemt.  \n  \nRefr.  \n\n\n',
                    'Den musikalske trikkefører': 'Nyinnspilling med Otto Nielsen fra 1967.  \n  \nNæst efter trikken  \ne´ den ting æ ælske´ mest på jol´ musikken,  \nog æ syns det kling av tona i trafikken,  \nmen likvæl savne æ litt verkelig musikk iblandt.  \nDet e sant.  \nTe direktør´n  \ngjekk æ så ei vakker kvellstoind for å spør´n  \nom æ på min trikketørn  \nkoin´ ta reisegrammofon´ min med i trikken mens æ kjøre´n,  \nmen han nekta skvær kontant.  \n  \nOg skjønt æ savne´ grammofonens glade klange  \nså e´ æ væl fornøia med arrangemange´;  \nog skjønt æ mange gange  \nføle mæ som fange  \ni den lange, trange  \nvogna kann æ altså itj forlange  \ngrammofon med spæll og sange.  \nDet e´ forbudt ifølge sporveisreglemange´.  \n  \nÆ spelle´ moinspæll å æ driv´ å komponere´  \nmen protestere´ kraftig mot å debutere.  \nÆ rennonsere´  \npå den ære, for æ vil itj resikere  \nat ´n Gulbransson med flere  \nvil blamere  \nmæ fordi æ plagiere.  \nForræsten e´ de itj nå å tjæne på det derre.  \n  \nOg trækkspæll drar æ;  \ngehør det har æ;  \nimellem tar æ  \nen liten sang.  \n  \nFra trikken lar æ ofte desse strofan høre:  \nHei alle De som går og alle De som kjøre,  \nfor 15 øre  \nkan det også la sig gjøre;  \ngår det seint så får man smøre  \nsig med tålmot og så bør´e  \nikke verke på humøret;  \nmed sneglefarten e´ det ingenting å gjøre.  \nVi kjem´ nok siga´n te Singsaker holdeplass eingang.  \n\n\n',
                    'En vise om Munkholmen': 'Nyinnspilling med Per Sjølie fra 1967.  \n  \nOriginaltext af: Peder Griffenfeldt.  \n  \nEn Klippe op af Vandet staar,  \nsom mand Munkholmen kalde.  \nDen Bølgen iideligt paaslaar,  \nog Søers Magt anfalde.  \n  \nDer bryder skummend´ Bølge sig,  \nog Klippen slaar tilbage.  \nLær heraf fast at beskikke dig  \ni Modgangs haarde Dage  \n\n\n',
                    'Hu og hei': 'Nyinnspilling med Tor Jemtland m. fl. fra 1967.  \n  \nFra [Studenter i den gamle stad](index.asp?vis=SIT%201910-60): Men en vise\ngjorde stor lykke, «Kjekke gutters vise», en virkelig henrivende parodi på\nidrettsungdommens sjargong og selvbeundring.  \n  \nHu og hei!  \nVi er kjekke du og jeg.  \nKjekke gutter.  \nDrabelige gitt.  \nKjekke gutter.  \nVi er en sober bande.  \nTåle frost,  \ntåle haggelskur og blåst,  \ntåle tåke.  \nAldri guffen, gitt,  \naldri låke.  \n:/: Vi er en sober bande. :/:  \n  \nRykke stubber op  \nmed blader, bark og rot, gitt,  \nturne i trapes  \nog bryte av en fot, gitt.  \nSove veldig hardt.  \nDet krever makt og mot, gitt.  \nJuberg er hyggelig.  \nGutta bor  \nunder sneen, langt mot nord.  \nDet er tappert.  \nSolen skinner ei.  \nDet er tappert.  \n:/: Her er det bare nordlys. :/:  \n  \nPinadø  \ngjennem nordagufs og snø  \ngå på hytta.  \nSkjelbreia, gitt.  \nGå på hytta.  \nDet er en nåbel eske.  \nViddens sang,  \nblodets akkompagnement  \ninni gutten!  \nTanker går i svang  \ninni gutten.  \n:/: Tyttebærlyng og krekling. :/:  \n  \nBær mig, mine ski  \nhenover ås og knoll, gitt.  \nBosbergheias juv  \nog frem til Tempervoll, gitt.  \nBær mig - bær mig ut  \ntil Lagmannseters koll, gitt.  \nBær mig fra byens jag!  \nSpise tran,  \nfange tyv og pyroman,  \ndrikke velling.  \nBokse lid´li hardt  \nsom hr. Schmeling.  \nVi er no´n viltre gutter.  \nVi er en sober bande  \n\n\n',
                    'Psykoanalytisk vuggevise': 'Synger:  \n  \nHvis Nussemusse-gutt vil sove  \nog ikke skrike, stakkars kroken,  \nskal mamma ganske sikkert love  \nå lese høit for dig av boken.  \nSo ro,  \nbyss byss  \nTralleralleraIleealle  \nBæ, bæ  \nbukken.  \nfor Lillegutt skal bysselalle  \n  \nReciterer:  \n  \nI skumringen skal vi oss riktig kose  \nog granske Lillegutts sjeledyp.  \nDer vrimler det mange små stygge kryp  \nhist et kompleks og her en neurose  \n  \nDet første verset i denne legende  \nhør efter, kjæreste Lillegull:  \nHvad solskinn er for det sorte mull  \ner seksuell oplysning for mullets frende.  \n  \nAsbjørnsen og Moe de var  \nto sublimatorer.  \nVi har gjennemskuet dem,  \nvi moderne morer.  \nAskeladd var fetischist  \nBukken Bruse var sadist  \nog Tornerose fikk tæring  \nav erotisk underernæring.  \n«Bæ bæ lite lamm»  \nhar du hørt sånt tull  \nHemninger som sier seks,  \ntypisk animalkompleks,  \nsøte Lillegull  \n  \nSo ro  \nsov godt,  \ndrøm så sødt om Freud og Adler.  \nByss, byss  \ndet var  \nto herrer uten frykt og dadler.  \n  \nHysj barn, dim far leser lekser.  \n  \nLigger du så vondt da, stumpen.  \nMor skal hjelpe deg og ta  \nbort den mindreverdighetsklumpen.  \nBlev det bedre da?  \n  \nBestefar går efter plogen,  \nbringer poteter og korn i hus.  \nFar din han går i skogen  \nog veider Ødipus.  \nSøster din har sex appeal  \nbestemor er litt senil,  \nog tantes elskere skifter  \nmens bror din sublimerer sine drifter.  \n  \nSolen skinner vakkert om kvelden,  \nkatten har hemninger på hellen.  \nLammene gresser bak blomster små.  \nLillegutt, Lillegutt, sove nå.  \nSolen skinner på heia,  \nLibido, Libido, Libedeia.  \n  \nSov søtt  \ndu må ikke pille nese  \ndet be-  \ntyr at -  \nHysj vær stille  \nmor skal lese.  \n\n\n',
                    'Sang ved typisk massebryllup': 'Fra [Studentersamfundet i Trondhjem gjennem 25\når](index.asp?vis=SIT%201910-35): «Næmesis» hadde en god rød tråd: Studenten\nHansemann opkaster sig efter de beste og da brandaktuelle Hitler-mønster til\ndiktator ved Høiskolen. Professorene settes i konsentrasjonsleir, og da\ndiktatoren selv lokkes i kvinnens garn, kommer Næmesis: Med et maktbud tvinger\nhan alle sine kamerater til å gifte sig samtidig med ham i et kjempebryllup i\nDomkirken.  \n  \nKor av 120 brudepar:  \n\nHer skal bli fest!  \n\nHer skal bli blest!  \nFinn dig litt brennfort en brud og en prest!  \nHer skal bli stas,  \nkjempe-kalas!  \nNå er det slutt med eksamen og mas.  \n\n  \nEn kjekk brudgom til sin søte brud:\n\n  \nTimen er kommen  \nda vi skal dra  \nbort ifra Trondhjem.  \nEr du ei glad?  \n\n  \nHun (i en annen gate):  \n  \n\nTrondhjem, ditt klima  \nsynes jeg er prima.  \nNår det er pent vær  \ner det da pent her.  \n\n  \nHan (revet med):  \n  \n\nÅ ja og tenk  \npå Elsterparkens benk,  \nhvor et par øine  \nrendte mig i senk....  \n\n  \nKor av 120 brudepar:  \n  \n\nHver tar nå sin,  \nså tar jeg min;  \nnå får du se å bli klar over din!!  \nKom kun, min snupp,  \nsitt ei og dupp!  \nVær med å heng på i masse-bryllup!  \n\n  \nHan:  \n  \n\nAlt Vi har skrytt av  \nlevner vi her.  \nSamfundet, Hytta...  \nHil være Jer!  \n\n  \nHun (i en annen gate):  \n  \n\nEnn om vi kommer  \ntil Paris i sommer!  \nDrar vi på tredje  \nfår vi råd te´ det.  \n\n  \nHan (revet med):  \n  \n\nHeller i bil  \nvi rusler uten  \nSå kan vi stanse  \nog ta oss nu og da en hvil....  \n\n  \nKor av 120 brudepar:  \n  \n\nHer skal bli fest!  \nHer skal bli blest!  \nFinn dig litt brennfort en brud og en prest!  \nHer skal bli stas,  \nkjempe-kalas!  \nNå er det slutt med eksamen og mas.  \n\n  \n\n\n',
                    'Vestfronten': 'Fra [Studentersamfundet i Trondhjem gjennem 25\når](index.asp?vis=SIT%201910-35): Revyen var rik på ypperlige optrin,\nuforglemmeligst kanskje raden av statuer på Domkirkens vestfront som synger om\ngotisk skulptur.  \n  \nJohannes:  \nHer på Vestfronten har  \ndet vært krig i mange år.  \nD´er et under at den enda står.  \n«Intet nytt», sa han Remarque.  \nHan må vær ´en artig knark,  \nher blir mere nytt hver dag som går.  \n  \nMathæus:  \nArkitektene slåss.  \nKunstens vei er tornefull,  \ndet er mye skrik og lite ull.  \nNogen vil ha fronten bak,  \noktogon med kuppeltak.  \nResultatet er omtrent lik nul.  \n  \nDyre Vå, Nico Schiøll,  \nKvidbergsgård og enda fler,  \nde har brukt op flere tons med ler.  \nDe har hengt i dag og natt,  \nmodelert så leira skvatt.  \nSju apostler og en farisæer.  \n  \nRefr.:  \nJohannes:  \nMen æ  \n\\---  \ne ækt  \n\\---  \n  \nThomas:  \nStakkars Andreas er  \nmodellert av Dyre Vå.  \nSå han er nå bare så som så.  \nHan har bare 8 tær  \nog så har´n e´ vorte der,  \nunder kappa har´n ull trikå.  \n  \nAndreas:  \nHør på Thomas, da De!  \nDu kan bare pass´ dig sjæl!!  \nDu har også din Akolleshæl.  \nHan har skjorta att og bak  \nog så mangler´n skjorteflak,  \nOg på hue har´n potitskræl.  \n  \nThomas:  \nMen Mathæus er fin,  \nhan er polykromerert,  \nellers er´n littegrann genert.  \nHan er SchiølIgjort, som De ser,  \n(sån litt ovenfra og ne´r)  \nbegge skuldra hans er godt vattert.  \n  \nRefr.:  \nKongespeil -- Tore Hund  \nHelge Thiis -- Maeody Lund.  \nAd Quaderaderaderatum.  \n  \nMathæus:  \nMen Johannes er blid,  \nfor han er en heldig gris:  \nHan er kamerat med Helge Thiis.  \n  \nJohannes:  \nSku´n ha hørt på no så frækt.  \nTenk å ikke ha respækt!  \nDem er kopiert, men æ e´ ækt,  \n  \nRefr.:  \nSt. Denis:  \nÆ å ---  \ne ækt ---  \nVi er begge to av gammal gotisk slekt  \n  \nAndreas:  \nHør der ringte klokka to  \nJa, da går vi jaggu n´er  \nD´er påtide vi tar frikvarter.  \nEn blir lemster av å stå  \nSt. Denis ta hue på,  \nfor apostlene skal ut og gå.  \n\n\n',
                    '80-årenes sportsvise': 'Ungdommen like fra Arilds tid,  \nArild, Arild!  \nhiger mot idrett og kappestrid,  \ndet er så mandig, at gid!  \nKrokket, krokket, det er en herlig sport,  \ndertil kreves trening av beste sort.  \nToddy må aldri smakes,  \nog wienervals forsakes.  \nDet nytter knapt  \nå trene slapt  \nnår det gjelder en krokketkamp.  \n  \nLandtur er også en edel sport,  \nlandtur, landtur!  \nBare den ikke blir drevet hårdt -  \nda er den siste sort.  \nVandre, vandre ut i Guds fri natur,  \ndet har gitt oss mandig og fin figur.  \nHver søndag vi mosjonerer,  \ntil Lade vi spaserer,  \nmed energi  \nklarer vi  \nstrabadserne med bravour.  \n  \nSporten er nådd til et høit nivå,  \nheia! heia!  \nAldri må sporten bli plump og rå,  \ni skihopp man aldri må stå.  \nKvinner, kvinner  \nmå ikke slippe til.  \nDe må bare gjøre som mannen vil.  \nog marsjkonkurranser må de  \naldeles ikke gå i.  \nEn kvinnes dyd  \ner hjemmets pryd,  \nog må ikke stå på spill.  \n  \nKuler å klinke og keglespill,  \nkrokket, krokket,  \nhører den riktige sportsmann til,  \nog gjør ham, vennlig og snild.  \nGleden, gleden ved å slå snurrebass  \nbyttes ikke med slappfiskens toddyglass.  \nMen velociped å ride,  \npå isen blank å glide,  \ndet gir en mann,  \nvips på stand,  \nblandt kvinner en første plass.  \n\n\n',
                    'Rasmussens vise': 'Nyinnspilling med Otto Nielsen fra 1967. Han var medlem av forfatterkollegiet\ni 1931. Visa ble også brukt i jubileumsrevyen Gjengangere (1980).  \n\n\n',
                    'Vi har vår egen lille verden': 'Studentens liv er skralt,  \nmen skryt er livets salt.  \nNår verden vil bedrages,  \nså skryter vi av alt. :/:  \n  \nVår fremtids vei er trang,  \nvår læretid er lang,  \nskal sorgene forjages,  \nda skryter vi av alt. :/:  \n  \nVi dypper livet i vår egen fantasi.  \nHvis noen skal beklages  \nda la oss slippe fri.  \n  \n  \nRefr.:  \nVi har vår egen lille verden  \ni et nøtteskall omtrent  \nmed sitt eget firmament.  \nBelyst av fikse stjerner er den,  \ni vår vennekrets er Jomfruen bekjent.  \nVår verdens center er studenter,  \nrundt oss går Trondhjems by i rotasjon.  \nStudenter har sin egen verden,  \nvi står fast i last og brast  \ni kraft av vår gravitasjon.  \n  \n  \nVår ære og vår makt  \nhar svarte dusker bragt,  \nen avgrunn av studerthet  \ner i vårt hode lagt. :/:  \n  \nVi vet naturligvis  \nat Rom er paradis,  \nvi snakker med bornerthet  \nom London og Paris. :/:  \n  \nVi skryter frekt og flott,  \nmen har for lengst forstått  \nat Trondhjems ugenerthet,  \nden gjør studenter godt.  \n  \n  \nRefr.:  \nVi har vår egen lille verden...  \n  \n  \nFra Kapp til Lindesnes  \ngror pikebarn som gress,  \nmed nykker og med griller  \nog nydelige fjes. :/:  \n  \nLa fare hen, la gå,  \ndem kan de andre få.  \nVår trønderpike stiller  \ndem helt i parentes. :/:  \n  \nSi, er det vår kritikk  \nsom sløves, og vårt blikk?  \nMed fantasiens briller  \ner ingen halvt så chic.  \n  \n  \nRefr.:  \nVi har vår egen lille verden...  \n\n\n',
                    'Nu klinger': '',
                    'Drikkevise (Det er liddelig flaut)': '![](uka/1925_bing_bang.jpg)Nyinnspilling fra 1967.  \n  \nTeksten er skrevet av Odd Nansen. Originalen ble framført av Aage P.\nElmenhorst. Visa ble en stor slager på Chat Noir i Oslo med Einar Rose.  \n  \nDa jeg første gang i mit liv var tørst da kom min mor og ga  \nmig litt mjelk og sa  \natte mjelka den var bra.  \nDa hun siden prøvet med vand så sa jeg: Tak, jeg ska´ke ha  \ni vandet det bor  \njo fiskene mor  \nvi kan da´ke drekke det da?  \n  \nRefr.: Det er liddelig flaut da git å drekke bare vand  \nmen blanda med whisky kan det jo til nød gå an  \nmen reneste vare smaker besst  \nog reneste vare fyller mest,  \ndet må til i storm og blest.  \n  \nEngang blev jeg syk og blev lagt ind på en kjempemessig sal  \npå et et hospital,  \ndet var magan, som var skral.  \nDoktor´n skjønte slets ingenting og situationen var fatal  \nMen saken den var  \njo enkel og klar:  \nJeg hadde vært reint for total.  \n  \nRefr.: Det er farlig for magan git å drekke bare vand ---  \n  \nEngang holdt jeg på å krepere i Saharas ørkenland  \nJeg tok det som en mand  \nskjønt jeg lå på gravens rand.  \nHvor jeg snudde hue så så jeg bare himmel, sol og sand  \nJeg skjønte jo sjæl  \njeg trørsta ihjæl. —  \nDa var det jeg ba om litt vand!  \n  \nRefr.: Det er liddelig flaut da git å be om bare vand ---  \n  \nSiden kan jeg tydelig huske at jeg var i nød engang;  \ntenk jeg lå og slang  \nutpå sjø´n i bare tang.  \nSkuta den var sunket tilbunds, jeg syntes tiden faldt litt lang,  \njeg lå der å fløt  \ndet var jo litt bløtt  \njeg svelja og gulpa og sang:  \n  \nRefr.: Det er liddelig flaut da git å gulpe bare vand ---  \n\n\n',
                    'Duet (Det er så mange ting)': '![](uka/1925_bing_bang.jpg)Nyinnspilling fra 1967 med Håkon Sandvik (baryton)\nog Dagfinn Eckhoff (sopran). Teksten er skrevet av Odd Nansen.  \n  \nHan: Det er så mange ting i livet  \nsom jo bør hende før vi dør  \nog under månens blanke skive  \nder er det hendt så ofte før.  \nHun: Å, nei men fy! hvad kan du mene -  \nslikt må du aldrig tenke på!  \nJeg er en pike av de pene  \ndem må du aldrig plukke pa.  \n  \nRefr.:  \nHan: Det er så mange ting man ikke må  \nHun: For ikke alle ting er comme iI faut ...  \nBegge: Hvad dumme folk vil si  \nom dig og mig  \ndet gir vi pokker i  \nbåde du og jeg  \n  \nHan: Tullemor jeg tror jeg våger  \nendskjønt min engstelse er stor  \nå be din bror å bli min svoger  \nog din mama min svigermor.  \nHun: Nei kjære dig det nytter litet  \njeg er så attfor ung syn´s mor  \nog hun må ikke få å vite  \nat jeg alt lenge har vær´t stor  \n  \nRefr.:  \nHan: Det er så mange ting man ikke må  \nHun: For ikke alle ting er comme iI faut ...  \nBegge: Hvad dumme folk vil si  \nom dig og mig  \ndet gir vi pokker i  \nbåde du og jeg  \n  \n\n\n',
                    'Hjemve': '![](uka/1925_bing_bang.jpg)Nyinnspilling med Harald "Pætti" Skagen fra 1968.  \n  \nTeksten er skrevet av Odd Nansen. Fra [Studentersamfundet i Trondhjem gjennem\n25 år](index.asp?vis=SIT%201910-35): Den udødeligste visen av de mange gode\nfra «Bing-Bang» er dog kanskje den hvor en stakkars trønder udi fremmed land\n(Pætti) tolker sin lengsel og hjemvé. Det er ingen overdrivelse å si at dette\nrefreng blev folkevise i Trondhjem.  \n  \nÆ e født i Trondhjem uti Sanden,  \nog siden har æ bodd der al mi ti´,  \nog Trondhjem er en by som ingen anden,  \ndet trur æ ganske trøgt at æ kainn si.  \nAa ja, æ e saa grænselaust taknæmli,  \nforde´ at æ e født i slik en by;  \nder e no alt saa koseli og hjemli´,  \nslik som den ligg der trøgt og godt i ly.  \n  \nRefr.: Trondhjem, Trondhjem, at æ reist ifra dæ,  \nat æ koinne finn paa nokka slekt!  \nNaar æ tænke paa ka godt du ga mæ  \ne de´ som æ læste dekt!  \nTrondhjem, Trondhjem, no æ rætt forstaar dæ,  \ndu min barndoms allerstørste ven!  \nUndres paa korless det gaar dæ  \nka som heinne einn,  \naldri reise æ fra dæ igjen!  \n  \nNei, bættere, æ tar den første baaten  \naa sjer aa kommaa hjæm saa fort æ kainn.  \nÆ længte jo så æ e´ reint paa graaten,  \naa ka æ gjør saa e´ de´ likedan!  \nÆ e´ saa gla i alt som e´ derhjemme  \nfra Ilevolden og til Lade gaard;  \nog Elsterparken kainn æ aildri glemme;  \nden va´ jo ailti leikeplassen vor!  \n  \nRefr.  \n\n\n',
                    'Måkevisen': '![](uka/1925_bing_bang.jpg)Nyinnspilling med Conrad Gärtner fra 1967. Teksten\ner skrevet av Odd Nansen.  \n  \nJeg var engang måker i et fjøs med 86 kjør  \nså de skjønner vel at jeg har måka før  \nDet ern´te småtterier det som slike kuer står og gjør  \nmen det er itno mot Svalbard når det snør  \n  \nRefr.: Det er trist her i nord  \nlike ved den kalle pol,  \nher hvor ikke engang potteplanter gror  \nHer er svart som natta dagstøtt for´e skjinner aldrig sol  \nDerfor lengter jeg hjem til far og mor  \n  \nHan Wedel tørn´te komma hit forsi han veit så væl  \nder han sittet lunt i stua hos seg sjæl  \nat på øiane han skaffa vors er kulda streng og fæl  \nhvis´n kom hitop så fraus´n glugg ihjæl.  \n  \nRefr. ......  \n  \nTenk om Norge hadde fått en øi som lå litt lenger sør  \nder hvor negrane går stasa ut med fjør  \nder hvor pigebarna ikke har så meget som et slør  \nog hvor man får se sola før man dør!  \n  \nRefr. ......  \n  \n\n\n',
                    'Studentervisen (Tenk om jeg var millionær)': '![](uka/1925_bing_bang.jpg)Nyinnspilling fra 1967. Teksten er skrevet av Odd\nNansen.  \n  \nTenk om jeg var millionær og bodde i et slott.  \n(ja det var andre greier det, nå bor jeg i et kott)  \nDundrende fester  \nkjempeorkester  \nsom spiller like flott som Maliniack  \nak ak,  \nog alle slottets kjeIderrum var fyldt med øl og vin  \nog overkokken stod og stegte feite fyllesvin;  \nlekre fasaner,  \nbløte divaner,  \nog en rad med fyldte pengeskrin.  \nha ha ha ha ......  \n  \nRefr.: Her er fest hvor vi har tilhuse  \nSving din dusk la homla få suse  \nLa os nu som før  \njage hver sorg på før  \nfor som bekjendt  \ntar en student  \nætting med godt humør.  \n  \nDengang jeg gik i måneskin til verdens ende hen  \nmøtte jeg en pigelil som vilde bli min ven  \npigen var slank  \nog månen var blank  \net hjerte banket sagte mot min frak  \nak ak,  \nog på et lite figenblad holdt guden Amor vagt  \npasset på at alt som skulde sies nu blev sagt  \nMed ett var det slutt  \nfor som hun var skutt  \nkom mora op av jora. - For et syn  \nha ha ha ha ......  \n  \nRefr.  \n  \nEn vårdag sat jeg blek og svettet ved examensbord  \nog ønsket alle proffene dithen hvor peppern gror,  \nsovnet så ind  \nmed hånd under kind  \nog seilet ut i rummet på min krakk  \nakk — akk —  \nDet gik så spruten stod om os med proffene ombord,  \nden værste av dem alle hang jeg efter i en snor,  \nhevnen er sød  \nog proffer i nød  \ner no´ av det jeg aller helst vil ha  \nha ha ha ha ......  \n  \nRefr.  \n  \nDe´r øvet mangt et storverk her i verden rundt omkring  \nmen mot hvad vi skal gjøre blir det hele ingenting  \nflyvemaskiner  \nkjempeturbiner  \nsom skal døive alt det gamle makk  \nak ak,  \nberømmelsens og lykkens dører åpner sig for os,  \nvi skal spende broer helt fra Peking og til Moss.  \nbygge og tegne  \ntenke og regne  \nkan man når man er fra N. T. H.  \nha ha ha ha ......  \n  \nRefr.  \n  \n\n\n',
                    'Duet - Per og Norma': 'Nyinnspilling med Dagfinn Eckhoff (Norma) og Tore Tønseth (Per) fra 1967.  \n  \nFra [Studenter i den gamle stad](index.asp?vis=SIT%201910-60%20-%201918):\nDuetten mellom studenten Per (iført snibel, dusk, sverd og skjold) og nonnen\nNorma - skrevet av Odd Nansen og brilliant sunget av Aage P. [Elmenhorst] og\nOdd Guttormsen, ble veldig populær. [...] De charmerende ord til en\ninnsmigrende melodi gikk som en farsott på ungdomsballer over hele landet.  \n  \nHan: Lille du - si mig nu  \nom du tør for paven  \nta en tur i Guds natur  \nut i klosterhaven.  \nHun: Gid a´ mig - husk at jeg  \ner en hellig søster,  \ngå din vei, for indi mig  \ntaler dydens røster.  \n  \nRefr.: Hun: Hvad har mamma sagt?  \nHan: Ja hvad har mamma sagt?  \nHun: Ta for mandfolk dig iagt!  \nHan: Så det har mama sagt.  \nSkal det stå ved magt?  \nHun: Ja skal det stå ved magt?  \nBegge: Alt hvad mødrene har sagt  \nvar vi længst i graven lagt.  \n  \nHan: Lille skat - tro ei at  \njeg´ dig vil forføre:  \nkom bli med i busk og krat  \nkast kun nonnesløre´.  \nHun: Kys mig Per - endda mer!  \nGud hvor det var deilig,  \nog så får jeg endda fler  \nnår det blir beleilig.  \n  \nRefr. \n\n',
                    'Olav Styggesens dropa': 'Nyinnspilling med Odd Nansen fra 1967, samme mann framførte originalen.  \n  \nFra [Studentersamfundet i Trondhjem gjennem 25\når](index.asp?vis=SIT%201910-35): Et av glanspunktene var den nye kraft Odd\nNansen som «Olav Styggesønn», en parodi på den nyreiste Olav Tryggvessøn-\nstatue på Trondhjems torv.  \n  \nKargr er Konungrs kår.  \nBedre i Valhall å vera  \nDer drev jeg edel idrett  \nSprang på de utenbords årer  \nKastet med knivskarpe kniver  \nMesket min mage med mjødr  \n  \nUklok var jeg som agtet  \nDyres lokkende løfter,  \nHan som med falske fakter  \nbød mig i Nidaros herske.  \n  \nHit ble i hast jeg hentet  \nlagt på larmende lastebil.  \nSausede skjæggmunde spyttet,  \nline mig lagdes om livet,  \nhårede hænder halte,  \nhastig jeg heistes mot himlen.  \n  \nKonungr Haakonr haler  \nsivgrønne serkr sig senker  \nmundfagre Wallemr vræler.  \nStaselig stund for Kongen.  \n  \nHelvedes høit har jeg hoppet  \n(se side 70 i Snorre).  \nNå er jeg gammel og giktsvak;  \nknærne knaker i knokene,  \nværlagets vonde vetter  \nhårdt har min helse herjet;  \nregnet mig risler i rumpen.  \nKargr er Konungrs kår.  \n  \n\n\n',
                    'Regningsbudets vise': 'Nyinnspilling med Henrik Lassen Kiær fra 1967. «Tit» Kjær var teatersjef i\n1921 og en av de sentrale aktørene på scenen.  \n  \nFor aa faa regningsbudcertifikat  \nmaa man vær jækla smart  \noptræ voksent, det e klart  \naldri gaa ind galt,  \nfor da kan man korn ut saa altfor snart  \naa helst me´ en sabla fart,  \nbakfra faar man et spark saa hart  \nat man bli sjang-sjang malt.  \nMen det værste e — aa faa rekti te´  \nbankinga saa fin — at dem sei: — «Korn ind».  \nE det en person — Vant te aa vær paa mo´n  \ngjør æ bare saa´n 1—2— (bank paa).  \n  \nÆ renne aa trampe fra morra te kvel  \nhar aldrig en time fri  \naa æ faar kjætt for at folk har gjæld  \nsom d´e skylla mi  \nat alt det som finnes har stege saa lideli  \nsiden den gode ti,  \nmen æ e akkurat like bli — samma ka folk kan si.  \nMen det værste e´ aa faa rekti te  \nbankinga saa fin — at dem sei: — «Kom ind».  \nHos ein skibskaptein — slår æ det kjendte tegn  \nsom di veit fra før — 2 glas (bank paa).  \n  \nKjæm æ paa vandring hos ein student  \nflire´n mæ næsten ut  \naa hos ei pie som æ har kjendt  \nrækkes mæ ein trut  \nsom ingen gut har nogensinde set forut  \naa saa e æ kaput.  \nReinsle dit bli aldri slut  \nhvis itj det bli forbutt.  \nMen det værste e — aa faa rekti te  \nbankinga saa fin — at dem sei — korn ind.  \nHos ei peppermø — som bli gla aa rø  \nsei æ pinedø — tak for mæ — adjø  \n\n\n',
                    'Aktiemæglerens vise': 'Nyinnspilling med Ole Christian Johnsen fra 1968 (fra Otto Nielsens\nprogramserie «Nu klinger igjennem den gamle stad»). I 1919 ble visa framført\nav instruktøren, Asbjørn Lindboe. Tekstforfatter er teatersjefen Hans Jacob\n«Rocambole» Nielsen.  \n  \nJeg er en aktiemægler jeg  \ndet kan De vel se paa mig,  \njeg har vær´t en herre,  \nnu er jeg det ei.  \nJeg festet høit med kvin´s og skum  \nindtil en ven fra Sodium  \nmig mindet paa jeg skyldte ham en sum.  \n«Kursen gaar ned, den da-da-daler  \ngi mig besked, om du betaler».  \n«Tull og tøis», sa jeg og ilte,  \njeg mente bilte  \ntil grand soupé.  \nKursen gaar ned, den da-da-daler  \ngi mig besked, om De betaler,  \noveralt man litt mistænksomt smilte  \nkursen gaar ned, den da-da-daler.  \n  \nSøndag var jeg millionær  \nhadde bil og silkeklær,  \nvar en matador, helt i fra top til tær.  \nMandag var det ikke frit  \njeg begyndte skjælve litt,  \nog paa tirsdag var jeg helt fallit.  \nKursen gaar ned, den da-da-daler  \ndet haster ei med, at jeg betaler.  \nMine kreditorer raste  \nde fløi og maste,  \njeg svarte blot:  \n«Kursen gaar ned, den da-da-daler  \ndet haster ei med, at jeg betaler».  \nDe skar tænder saa det skreik og knaste:  \n«Kursen gaar ned, den da-da-daler».  \n  \nMin skriv´maskinedame er  \nnu gaat ind i frelsens hær.  \nJeg har solgt min villa  \nog stampet mine klær.  \nDet eneste jeg ei fik solgt  \nvar aktierne som jeg beholdt,  \nde er bra at ha naar det er koldt.  \nKursen gaar ned, den da-da-daler  \nmit kul og min ved jeg ei betaler,  \naktier jeg i ovnen tænder  \nde herlig brænder  \nog varmer godt.  \nKursen gaar ned, den da-da-daler  \nmit kul og min ved jeg ei betaler,  \nBrænd kun aktier, mine kjære venner,  \nfor kursen gaar ned, den da-da-daler.  \n  \nJeg er falleret fallera,  \nmen endda er jeg likegla´.  \nhausse og baisse notering  \nkan andre overta.  \nNu gaar jeg og venter paa  \nat jeg snart skal selskap faa.  \n«Kolleger kom i mine arme smaa».  \nKursen gaar ned, den da-da-daler  \nstag ei og sved, i angstens kvaler.  \nBrekken er blit meget tynd De,  \nmen det er yndig  \nat følges ad.  \nKursen gaar ned, den da-da-daler  \nstag ei og sved i angstens kvaler.  \nGjør fallit som jeg, og bli umyndig.  \nKursen gaar ned, den da-da-daler  \n\n\n',
                    'Bertin Margs Vise': 'Nyinnspilling med Arve Herrem fra 1968 (fra Otto Nielsens programserie «Nu\nklinger igjennem den gamle stad»). Originalen ble framført av Øyvin Lange (nr.\n2 fra høyre i rollen som Bertin Marg). Utgangspunktet var en aktuell sak om en\nsultestreikende fange som ble tvangsforet.  \n  \nHer kommer jeg fra mit fængsel  \nforbi er nu al min trængsel  \nde proppet og stoppet min mave  \nsaa at den kom helt ut av lave.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nFørst kom dem med vand og brø´ di,  \nda streika æ bætterdø di,  \nfor hvad er vel stomp og vand da  \ntil mat for en fuldvoksen mand da  \n(paa en manda´)  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nDa jeg hadde erklært streiken,  \nsaa kom dem jo straks med steiken,  \nden putta dem i mig med gafler  \ntilsammens med to dusin vafler.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nTil desert æ sku ha lompe,  \nsaa kom dem med brandfolk og pompe,  \ndem sleit saa dem holdt paa aa daane,  \nmen saa fik dem dampsprøita laane.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nMen søndagsbiffen var værre,  \nden nægta æ plent aa fortære,  \nmen tilmed den biffen dem greide,  \nen rambuk fra havna dem leide.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nSaa la dem mig ned paa ryggen  \nog stelte op rambok styggen,  \naa jøss det var nifst ska´ æ si dæ  \nnaar klossen slo´ biffane i mæ.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \nTre okser æ aat sisste torsdag,  \nden tyske revolutions-aarsdag,  \ndet har sin behagelig´ side  \nfor socialismen at lide.  \nAldrig no´ngang fik jeg slikt traktement.  \n  \n\n\n',
                    'Hadjet-Larschens vise': 'Nyinnspilling med Tor Jemtland fra 1968 (fra Otto Nielsens programserie «Nu\nklinger igjennem den gamle stad»).  \n  \nOriginalen ble på premieren framført av Hans Jacob «Rocambole» Nilsen som\nsenere ble profesjonell skuespiller og teatersjef. Han gikk så opp i rollen at\nhan på andre forestilling skjøt seg selv i hånden og ble sengeliggende gjennom\nresten av forestillingsperioden.  \n  \nVisa ble også brukt i jubileumsrevyen Gjengangere i 1980.  \n  \nI Petrograd jeg fødtes, som mit aller første spræl  \njeg slog min far og mor og hele min slægt ihjel.  \nJeg ledte efter mynt rundt i min faders hele hus,  \nda blev jeg sint, den tosken var jo fattig som en lus.  \nJeg fandt en gammel sabel og saa drog jeg da avsted  \nog dannet morderligaen av ligasindede.  \n  \n\nVogt Dem for Hadjet-Larschen  \nnu er han paa færde her.  \nHar De en svigermor  \nom hvem De kanske tror  \nat hun længes væk fra asperinen og massagen,  \n  \nKom blot til Hadjet-Larschen  \nhan hurtig sætter englevinger paa.  \nEt munter blik man sender  \n«Kondolerer kjære venner»,  \nog saa kan De fornøiet atter gaa.  \n\n  \nBlandt Stockholms «upper ten» der var jeg meget vel tilfreds  \njeg fik en stor og svært indbringende kundekreds.  \nMan annoncerte med mit navn, ja se nu bare her:  \n«Av Eskilstunastaal Hadjet-Larschens kniver er ».  \n«Hans strikker er av Petter Carlsens prima hampesnor».  \nJa overalt mit navn man saa og folket sang i kor:  \n  \n\nVogt Dem for Hadjet-Larschen,  \nnu er han paa færde her.  \nEr Deres skrædder tvær,  \ner han Dem til besvær,  \nstaar han med regningen og spærrer Dem passagen:  \n  \nRefr.: Kom blot —  \n\n  \nI Norge har jeg virket blot i nogen ukers tid,  \nmen herregud hvor fint forretningen kom paa glid.  \nFra høires landsforening bud paa Tranmæl støt jeg faar,  \nog Stang har bedt mig sørge for at Gunnar Knudsen gaar.  \nFra alle hold man ber mig hjælpe Abrahamsen til  \nat komme hurtigst dithen hvor en drink nok smake vil.  \n  \n\nVogt Dem for Hadjet-Larschen,  \nnu er han paa færde her.  \nHar De en tante som  \nDem sikkert gjerne kan  \ntil hjælp med arven dersom det er smaat med gagen:  \n  \nRefr.: Kom blot —  \n\n  \nEn dag forsøkte jeg at dolke ned hr. Jelstrup fræk,  \nmen har var mig for tyk min kniv sat sig fast i spæk.  \nAt der skal kule til en trønder var mig ei bekjendt,  \nmen nu jeg straks fik femten revolvere til mig sendt.  \nDa Madsen hørte dette foreslog han fluksens dus,  \nog tilbud strømmet ind fra alle dem som vil ha hus.  \n  \n\nVogt Dem for Hadjet-Larschen,  \nnu er han paa færde her.Har De en leiebo´r  \nom hvem De kanske tror,  \nat han længter vældig væk fra loftsetagen.  \n  \nRefr.: Kom blot —  \n\n  \n\n\n',
                    'Rocamboles vise': 'Nyinnspilling med Bente (Berent A.) Moe fra 1968 (fra Otto Nielsens\nprogramserie «Nu klinger igjennem den gamle stad»). Skrevet av Einar Sissener\n(da jusstudent i Oslo, senere  skuespiller og regissør.)  \n  \nOriginalen ble framført av Hans Jacob Nilsen som senere ble profesjonell\nskuespiller og teatersjef. Kallenavnet Rocambole ble han aldri kvitt. Figuren\nRocambole stammer fra en populær romanserie på 1800-tallet, skrevet av Ponson\ndu Terrail.  \n  \nI et tvetydig budoir, jeg vet min fødsel var,  \nmin mor jeg fant, men hun forsvant,  \nblev drept på Gibraltar.  \nJeg følte meg hadsk og bitter  \nved skjelsord som dengang jeg fikk  \nog samlet en flokk med banditter  \nog dannet en morderisk klikk  \n  \n(Dette var første bind, så kommer 12te bind, det lyder så:)  \n  \nJeg levet nu som gourmand, i «Le Café Chantant»  \nog min maitresse, var fin comtesse  \nog jeg er Don Juan.  \nMen i Bois Eau de Cologne  \njeg hadde en grusom duel  \nmed greven av Bleau de Flakogne  \ncomtessen hun ropte: «farvel!»  \nMit liv er urolig  \nnat er som dag  \nmit eventyr det er utrolig  \nlivet er kort: «Baccarat!»  \nDerfor jeg tømmer et bæger på galgenhumor.  \nLa myrde, la dolke, la brænde på bål  \nRocamboles skål  \n  \nJeg mænget mig i byers skarn, jeg var forbryderbarn  \njeg var var en skurk, som grev Luxburg  \njeg trak i mine garn.  \nMed dolk og gift drog om natten  \njeg myrdende rundt i Paris  \nmine ofre er hundred og atten  \nmeritter i tusindevis.  \n  \n(Dette var 12te bind, så kommer 230te bind, det lyder så:)  \n  \nJeg myrder fræk. med mordertræk og pst! — så er jeg væk  \nHerr Asbjørn Krag er mig for svag  \njeg drukner ham i blæk! —  \nJeg borer ham ind i døden  \nStein Riverton kan si farvel!  \nog Svanstrøm den svenskfødte jøden  \nham ønsker jeg lykke og´ held! —  \nMit liv er urolig  \nnat er som dag  \nmit eventyr det er utrolig  \nlivet er kort: «Bacearat!»  \nDerfor jeg tømmer et bæger på galgenhumør.  \nLa myrde, la dolke, ia brænde på bål!  \nRocamboles skål!  \n  \nJeg kommer ut i nye bind. --- Ha! kjære bind forsvInd!  \ni krones bind, men uten skind  \nog Svaustrøm soper ind.  \nMen jeg likte mig bedre i avisen  \nsom en fængslende lang foljeton. —  \nDa Kittelsen tegnet markisen  \nog mig i en skummel salon.  \nMit liv er urolig  \nnat er som dag  \nmit eventyr det er utrolig  \nlivet er kort: «Baccarat!»  \nDerfor jeg tømmer et bæger på galgenhumør.  \nLa myrde, la dolke, la brænde på bål!  \nRocamboles skål!  \n\n\n',
                    'Trondhjemsvisen (Men det er no´n ganske få detaljer)': 'Nyinnspilling med Per Sjølie fra 1968 (fra Otto Nielsens programserie «Nu\nklinger igjennem den gamle stad»).  \n  \nFra [Studentersamfundet i Trondhjem gjennem 25\når](index.asp?vis=SIT%201910-35%20krigstid): Selv i den obligate Trondhjem-\nsang var det kommet inn en ny tone, krigsstudentenes skepsis og kritikk. Hvert\nvers begynner med det gamle skryt til melodi «Santa Lucia», men så plutselig\nslår det om.  \n  \nI Trondhjems gamle by  \nsøker studenten ly  \nGammel historie  \ngir den sin glorie.  \nGuldet på Domens spir  \nstolthet og glæde gir.  \nI traditionens spor  \nfremgang og trivsel gror  \n  \nMen det er no´n ganske få detaljer  \nsom jeg ofte syn´s er mindre bra:  \nTrondhjemssuppe med svesker i,  \nugemyttlig politi,  \ntøveir når vi skal gå på ski,  \nsølepytter og griseri,  \nmindre moro på Hjorten di,  \nlurveleven og krangleri  \nnår jeg drar av med pia mi,  \nbolignød og optrækkeri,  \ndom lægger på leia så liddeli  \nat slikt er leit,  \ner no´ som alle veit!  \n  \nByens små damer vil  \njeg si no´ vakkert til.  \nMit unge hjerte slår  \nnår de forbi mig går.  \nDe kan vor længsel gi  \nskjønhet og harmoni,  \nog deres øine blå  \nmange forser sig på.  \n  \nMlen det er no´n ganske små detaljer,  \nsom jeg ofte syn´s er mindre bra:  \nGanske fri for koketteri,  \nsvære støvler med spiker i,  \ngriner på næsa når vi er bli´,  \nroper på mor når vi kysser di,  \nkanske litt hjulbent, hvad synes De?  \nGår hele da´n på konditori,  \nspiser kaker og slikkeri,  \nsir aldrig nei når vi når vi vil fri  \nat slikt er leit,  \ner no´ som alle veit!  \n  \nVisdommens tempel  \nsætter sit stempel  \npå den kultur som gror  \nop mot det høie nord.  \nHøiskolens store mål,  \nseir over sten og stål,  \nlokker vort unge sind  \nmot kundskaps høie tind.  \n  \nMen det er no´n ganske små detaljer,  \nsom jeg ofte syn´s er mindre bra:  \nBokholderi fra fire til ti,  \naldrig får vi en time fri,  \neksamener altid i urette tid,  \nslet karakter vil det altid bli,  \nhører i alt som står med petit,  \nkjører os rundt i fysik og kemi,  \ngjemmer bort glassa med spriten i,  \nog endelig er det en svare stri´  \nom hvad vi skal hete og hvad vi skal bli  \nat slikt er leit,  \ner no´ som alle veit!  \n\n\n'}

produksjonstype_dict = {'Radioteateret': ['radio', 'hørespill'], 'Ungdomsforestilling': ['ungdomsteater'],
                        'Ekstern statistjobb': ['eksternt', 'skildring'], 'Revykavalkade': ['revykavalkade', 'revy'],
                        'Musikal, 100 års jubileum': ['musikal', 'skildring'], 'Oppsetning': ['nei'],
                        'Ridderskapsmøte, 31 oktober': ['skildring'], 'sketsj': ['sketsj'],
                        'Revynummer': ['revynummer'], 'Improvisasjonsteater': ['improvisasjonsteater'],
                        '16. mai-picnic': ['skildring'], 'Forestilling med eldre revynummer': ['revykavalkade', 'revy'],
                        'Eksternt arrangement': ['eksternt'], 'Dialog': ['dialog'], 'Storsalsteater': ['nei'],
                        'Revykafé': ['revykafé', 'UKA', 'revy'], 'Trikketeater': ['trikketeater'],
                        'parodi på Heibergs «Balkonen»': ['parodi', 'skildring'],
                        'Aperitiff, immatrikuleringsmøtet': ['aperitiff', 'skildring'], 'parodi': ['parodi'],
                        'Knausteateret': ['intimteater'], 'Teater': ['nei'], 'Musikal': ['musikal'],
                        'en-akter': ['enakter'], 'Aperitiff / Eksternt arrangement.': ['aperitiff', 'eksternt'],
                        'parodi på «Synnøve Solbakken»': ['parodi', 'skildring'],
                        'Aperitiff på immatrikuleringsmøtet': ['aperitiff', 'skildring'],
                        'Tre enaktere': ['enakter', 'skildring'], 'Tambateater': ['tambateater', 'UKA'],
                        'Improvisasjonshappening': ['improvisasjonsteater'],
                        'Nattforestilling': ['nattforestilling', 'UKA'], 'Kunsterisk': ['kunstnerisk'],
                        'Konsert': ['konsert'], 'Eksternt arrangement / Kunstnerisk': ['eksternt', 'kunstnerisk'],
                        'KUP-musikal': ['KUP', 'musikal'], 'UKE-revy': ['revy', 'UKA', 'UKErevy'],
                        'Aperitif': ['aperitiff'], 'Enakter': ['enakter'], 'Eksternt arrangement (?)': ['eksternt'],
                        'Aperitiff': ['aperitiff'], 'B-nummer': ['nei'], 'Rammemøte': ['skildring'],
                        'Intimteater - Komedie': ['intimteater', 'komedie'], 'Korverk med dans': ['kor', 'dans'],
                        'Revy': ['revy'], '3-akter': ['treakter'], 'Dukketeater': ['dukketeater'],
                        'Fysisk teater': ['fysisk teater'], 'Intimteater': ['intimteater'],
                        'operaparodi': ['opera', 'parodi'], 'Kunstnerisk': ['kunstnerisk'],
                        'Innslag på eksternt arrangement': ['eksternt'], 'KUP': ['KUP'],
                        'Barneteater': ['barneteater', 'UKA'], 'Lansering av jubileumsbok': ['skildring'],
                        'parodi på «Vårbrytning» av Wedekind': ['parodi', 'skildring'],
                        'parodi på «Pelikanen»': ['parodi', 'skildring'], 'Rocke-musikal': ['musikal', 'rock'],
                        'Dassteater': ['dassteater'], 'Innslag': ['nei'], 'kabaret': ['kabaret'], 'Turne': ['turné'],
                        'Kupping': ['KUP'], 'Intimrevy (kavalkade)': ['intimteater', 'revykavalkade', 'revy'],
                        'I regi av Kulturutvalget.': ['skildring'], 'aperitiff': ['aperitiff'],
                        'Bestlt AFEI til Lille-UKA': ['UKA', 'Lille-UKA', 'skildring'],
                        'Intimforestilling': ['intimteater'], 'Månedsrevy': ['revy', 'månedsrevy'],
                        'Eksternt arrangement / Kulturutvalget': ['eksternt', 'skildring'], 'AFEI': ['AFEI'],
                        'Devised intimteater for ISFiT-17': ['intimteater', 'ISFiT', 'skildring'],
                        'Studenterkomedie': ['komedie'],
                        'Jubileumsrevy, SIT 70 år': ['revy', 'revykavalkade', 'skildring'], 'Picnic': ['skildring'],
                        'B-nummer (føljetong)': ['nei'], 'Innslag, immatrikuleringsmøte': ['skildring'],
                        'ISFiT-teater': ['ISFiT'], 'Aperitiff?': ['aperitiff'], 'Radio': ['radio'],
                        'Radioprogram med Otto Nielsen': ['radio', 'skildring'], 'Ungdomsteater': ['ungdomsteater'],
                        'Kunstnerisk?': ['kunstnerisk']}

lokale_dict = {'SIT-hybelen': ['SIT-hybelen'], 'Buss': ['Eksternt', 'skildring'],
               'Storsalsgulvet': ['Storsalen', 'skildring'],
               'Klubben, 8 forestilliniger': ['Klubben'],
               'Studentersamfundet': ['Diverse'], 'Selskapssiden/Strossa': ['Selskapssiden', 'Strossa'],
               'Kanalen': ['Eksternt', 'skildring'],
               'Hjorten': ['Eksternt', 'skildring'], 'Storesalen, lørdagsmøte': ['Storsalen'],
               'Mediahuset': ['Eksternt', 'skildring'],
               'Over alt': ['Diverse'],
               'Venstervinds årsmøte': ['Eksternt', 'skildring'], 'Oslo Konsterthus': ['Eksternt', 'skildring'],
               'Trøndelag Teater': ['Eksternt', 'skildring'],
               'Haandværkeren': ['Eksternt', 'skildring'], 'Klæbu': ['Eksternt', 'skildring'],
               'Gråkallen': ['Eksternt', 'skildring'],
               'All over the place': ['Diverse'],
               'Spisesalen (Edgar?)': ['Spisesalen'], 'NRK P2': ['Radio', 'skildring'], 'Biblioteket': ['Biblioteket'],
               'buss': ['Eksternt', 'skildring'],
               'På lerretet': ['Film'], 'Edgar, 8 forestillinger': ['Edgar'],
               'Elgeseter gate 4': ['Eksternt', 'skildring'],
               'Cirkus': ['Cirkus'],
               'Bodegaen': ['Bodegaen'], 'Nors Revyfestival': ['Eksternt', 'skildring'],
               'Tunga kretsfengsel': ['Eksternt', 'skildring'],
               'Storsalen / Kvinneseksjonen i Faglig 1.-maifront': ['Storsalen', 'Eksternt', 'skildring'],
               'Edgar': ['Edgar'],
               'Sanfundet, Storsalen': ['Storsalen'], 'Klubben, 8 forestillinger': ['Klubben'],
               'Storsalen / ?': ['Storsalen'],
               'I friluft': ['Utendørs'], 'Der du minst forventer det': ['Diverse'], 'Samfundet': ['Diverse'],
               'Teaterbygningen Prinsens gate': ['Eksternt', 'skildring'],
               'Storsalen, gulvet': ['Storsalen', 'skildring'],
               'Cirkus?': ['Cirkus'], 'Samfundet/Storsalen': ['Storsalen'],
               'Storsalen, 11 feb 61': ['Storsalen', 'skildring'], 'Levanger': ['Eksternt', 'skildring'],
               'Kartdagene': ['Eksternt', 'skildring'],
               'Knaus': ['Knaus'], 'Reitgjerdet': ['Eksternt', 'skildring'],
               'Herretoalettet ved Rundhallen': ['Herretoalettet ved Rundhallen'],
               'Realistforeningen Oslo': ['Eksternt', 'skildring'], 'Bakscenen': ['Bakscenen'],
               'Knaus og fritidsklubber': ['Knaus', 'Eksternt', 'skildring'],
               'Graakallbanen': ['Eksternt', 'skildring'],
               'Knaus / Radio Revolt': ['Knaus', 'Radio', 'skildring'], 'Storsalen, Samfundet': ['Storsalen'],
               'Sentrum Kino': ['Eksternt', 'skildring'], 'Studentersamfundet, 19.juni': ['Diverse'],
               'Edgar, 6 forestillinger': ['Edgar'], 'UKE-senderen': ['Radio', 'skildring'],
               'Tema88': ['Eksternt', 'skildring'], 'Daglighallen Pub': ['Daglighallen'], 'BUL': ['Eksternt'],
               'lørdagsmøte': ['Storsalen', 'skildring'], 'Sangerhallen': ['Sangerhallen'],
               'Samfundet, Storsalen': ['Storsalen'], 'Samfundet, Knus': ['Knaus'],
               'Estenstadmarka': ['Utendørs', 'skildring'], 'Overalt!': ['Diverse'],
               'Bergen': ['Eksternt', 'skildring'],
               'Intimen': ['Eksternt', 'skildring'], 'Nidarøhallen': ['Eksternt', 'skildring'],
               'Selskapssiden++': ['Selskapssiden', 'Diverse'],
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

verv_dict1 = {'Konsulent, lysreklamen': {0: "lysreklamist", 1: 'konsulent', 2: "annen prod"},
              'Konsulent, kostyme': {0: "kostymesyer", 1: 'konsulent', 2: "annen prod"},
              'Konsulent, kulisse': {0: "kulissebygger", 1: 'konsulent', 2: "annen prod"},
              'Konsulent, FFK': {0: "forfatter", 1: 'konsulent', 2: "annen prod"},
              'Lys, konsulent': {0: "lystekniker", 1: 'konsulent', 2: "annen prod"},
              'Lyd, myggkonsulent': {0: "lydtekniker", 1: 'konsulent', 2: "annen prod"},
              'Lyd, konsulent': {0: "lydtekniker", 1: 'konsulent', 2: "annen prod"},
              'Skuespiller, Guest Star': {0: 'skuespiller', 1: "guest star", 2: "annen prod"},
              'input': {0: 'verv', 1: 'rolle', 2: 'type'}, 'Sjåfør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Musikalsjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'KUPer': {0: 'KUPer', 1: 'ingen', 2: 'annen prod'},
              'Scenografkonsulat': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Bandleder': {0: 'kapellmester', 1: 'ingen', 2: 'annen prod'},
              'Leder forfatterkollegiet': {0: 'forfatter', 1: 'leder', 2: 'annen prod'},
              'Lys': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'konsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'UKE-lege': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Danser': {0: 'danser', 1: 'ingen', 2: 'annen prod'},
              'Markedsføring': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Fotograf': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kullisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'MedKUPkoordinator': {0: 'produsent', 1: 'assistent', 2: 'prodapp'},
              'Scenografiansvarlig': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'},
              'Lysreklamekonsulent': {0: 'lysreklamist', 1: 'konsulent', 2: 'annen prod'},
              'Kost- og losjiansvarlig': {0: 'forpleier', 1: 'leder', 2: 'annen prod'},
              'Kulissesjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Dotcom': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Bandet': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Lydbrigader': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'},
              'Lyddesigner': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'},
              'Trine Skei Grande': {0: 'skuespiller', 1: 'Trine Skei Grande', 2: 'annen prod'},
              'Konsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'kulisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Cocktailsyer': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Koreografassistent': {0: 'koreograf', 1: 'assistent', 2: 'prodapp'},
              'Lysdesigner': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'},
              'Filmarbeider': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Regi-ass.': {0: 'regissør', 1: 'assistent', 2: 'prodapp'},
              'Musikksnupp': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Uspesifisert': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Sufflør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'LYD': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'},
              'Instruktør ': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Visedirektør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Konsulenter lys': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'},
              'FFK-koordinator': {0: 'forfatter', 1: 'forfatterkollegieleder', 2: 'annen prod'},
              'Sminkør': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Kulissearbeidsleder': {0: 'kulissebygger', 1: 'arbeidsleder', 2: 'annen prod'},
              'Musiker': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Produksjonsdesigner': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymeassistent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kulissearbeider': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Kulissebygger': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Lydansvarlig': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'},
              'Sypike': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Musikk': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Oberst': {0: 'oberst', 1: 'ingen', 2: 'prodapp'},
              'Blondiekomiteen': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'VK-revy': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Regiassistent': {0: 'regissør', 1: 'assistent', 2: 'prodapp'},
              'Instruktør/forfatter': {0: 'regissør/forfatter', 1: 'ingen', 2: 'prodapp'},
              'Festivalstyret': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Skodespelar': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Orkesterinspisient': {0: 'musikalsk inspisient', 1: 'ingen', 2: 'prodapp'},
              'Ukelege': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'undefined': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Plakat / Program / Tegning': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'},
              'instruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Kostyme': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Sminkeassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'},
              'Videotekniker': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'},
              'Fittingsassistent': {0: 'fittings', 1: 'assistent', 2: 'annen prod'},
              'Skuespiller/manus': {0: 'skuespiller/forfatter', 1: 'ingen', 2: 'annen prod'},
              'Teknisk inspisient': {0: 'teknisk inspisient', 1: 'ingen', 2: 'prodapp'},
              'Barneteatersjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              '17 mai': {0: 'KUPer', 1: '17. mai', 2: 'annen prod'},
              'Lyssnupp': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Iscenesetter': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sminkeansvarlig': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Publikumsverter': {0: 'publikumsvert', 1: 'ingen', 2: 'annen prod'},
              'Guest 1.assistant director': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lysansvarlig': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'},
              'Følgespotsjef': {0: 'lystekniker', 1: 'følgespot', 2: 'annen prod'},
              'Program': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Leif Ronny': {0: 'skuespiller', 1: 'Leif Ronny', 2: 'annen prod'},
              'Kontentum': {0: 'lyddesigner', 1: 'kontentum', 2: 'prodapp'},
              'NM-ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Komponister': {0: 'komponist', 1: 'ingen', 2: 'prodapp'},
              'Forfatterkollegiekoordinator': {0: 'forfatter', 1: 'leder', 2: 'annen prod'},
              'Regi-assistent': {0: 'regissør', 1: 'assistent', 2: 'prodapp'},
              'Insruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Band (Berits venner)': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Suppelyd': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'},
              'Hår- og sminkestylist': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Scenograf og kostymedesigner': {0: 'scenograf/kostymedesigner', 1: 'ingen', 2: 'ingen'},
              'Billettansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Teatersjef/revysjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'Video v/VK': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Frisør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Forfatterkollegiet': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'},
              'Skuespiller og musiker': {0: 'skuespiller/musiker', 1: 'ingen', 2: 'annen prod'},
              'Lys.1': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Funksjonær': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kursholder': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kulissebygger/scenearbeider': {0: 'kulissebygger/scenearbeider', 1: 'ingen', 2: 'annen prod'},
              'ISFiT ledervalg': {0: 'KUPer', 1: 'ISFiT ledervalg', 2: 'annen prod'},
              'Lydkonsulent': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'},
              'Markedsfører og billettansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Grafisk designer': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Trener': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lys ved Regi': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Orkestersjef v/musikerlåfte': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Revysjef': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'Inspisientassistent': {0: 'inspisient', 1: 'assistent', 2: 'prodapp'},
              'Lysreklamesjef': {0: 'lysreklamist', 1: 'leder', 2: 'annen prod'},
              'Dramaturg': {0: 'dramaturg', 1: 'ingen', 2: 'annen prod'},
              'Video v/ARK': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Konsulent.1': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Forfatterkollegieleder': {0: 'forfatter', 1: 'leder', 2: 'annen prod'},
              'Hår- og sminkeassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'},
              'Manuskript': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'},
              'Helseansvarlig': {0: 'helseansvarlig', 1: 'ingen', 2: 'prodapp'},
              'Kostymedesigner': {0: 'kostymedesigner', 1: 'ingen', 2: 'prodapp'},
              'Skuespiller/forfatter': {0: 'skuespiller/forfatter', 1: 'ingen', 2: 'ingen'},
              'Animatør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Videokonsulent': {0: 'videotekniker', 1: 'konsulent', 2: 'annen prod'},
              'Fysisk trener': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Gnark': {0: 'skuespiller', 1: 'gnark', 2: 'annen prod'},
              'Kulissegjengen': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Lyd': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'},
              'Arbeidsleder': {0: 'kulissebygger', 1: 'arbeidsleder', 2: 'annen prod'},
              'Suppesnupp': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Medinstruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Forpleiningsansvarlig': {0: 'forpleier', 1: 'ingen', 2: 'annen prod'},
              'Lysreklameansvarlig': {0: 'lysreklamist', 1: 'leder', 2: 'annen prod'},
              'Garderobeslusk': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Konsulent i Lysreklamen': {0: 'lysreklamist', 1: 'konsulent', 2: 'annen prod'},
              'Scenograf ': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'},
              'Band': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Myggslusk': {0: 'myggslusk', 1: 'ingen', 2: 'annen prod'},
              'ULYD': {0: 'lydtekniker', 1: 'uLYD', 2: 'annen prod'},
              'Ein slags regi': {0: 'regissør', 1: 'en slags', 2: 'prodapp'},
              'Forfatterkollegiekonsulent': {0: 'forfatter', 1: 'konsulent', 2: 'annen prod'},
              'Sanger': {0: 'sanger', 1: 'ingen', 2: 'annen prod'},
              'Konsulent lys': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'},
              'Lydsnupp': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'},
              'MEDlyd': {0: 'lydtekniker', 1: 'MedLYD', 2: 'annen prod'},
              'Gjesteartist': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Rekvisitørassistent': {0: 'rekvisitør', 1: 'assistent', 2: 'annen prod'},
              'Komponistkollegieleder': {0: 'komponist', 1: 'leder', 2: 'prodapp'},
              'Korrektur': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Seremoniregissør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sang': {0: 'sanger', 1: 'ingen', 2: 'annen prod'},
              'Komponistkollegiet': {0: 'komponist', 1: 'ingen', 2: 'prodapp'},
              'PR': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lyd.1': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'},
              'konsulent.1': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Helseansvarlig/trener': {0: 'helseansvarlig', 1: 'ingen', 2: 'prodapp'},
              'Lys v/Regi': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'},
              'Kostymetegner': {0: 'kostymesyer', 1: 'arbeidsleder', 2: 'annen prod'},
              'Oversetter': {0: 'oversetter', 1: 'ingen', 2: 'prodapp'},
              'VIdeo': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Medlyd': {0: 'lydtekniker', 1: 'MedLYD', 2: 'annen prod'},
              'Kulissekonsulent': {0: 'kulissebygger', 1: 'konsulent', 2: 'annen prod'},
              'Layout': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lyssnopp': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Lyd v. FK': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lysreklamist': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'},
              'KUPkoordinator': {0: 'produsent', 1: 'KUPkoordinator', 2: 'prodapp'},
              'FK': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'},
              'Videokunster': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Scenograf/Rekvisitør': {0: 'scenograf/rekvisitør', 1: 'ingen', 2: 'prodapp'},
              'inspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'},
              'Kostymehospitant': {0: 'kostymesyer', 1: 'hospitant', 2: 'annen prod'},
              'Administrativ assistanse': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sminke- og hårassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'},
              'Suppedirektør': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'Cocktailarbeidsleder': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lyd v/FK': {0: 'lyddesigner', 1: 'LYD', 2: 'prodapp'},
              'Suppelys': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Sminkørassistent': {0: 'sminkør', 1: 'assistent', 2: 'annen prod'},
              'Konsulenter lyd': {0: 'lydtekniker', 1: 'konsulent', 2: 'annen prod'},
              'SIT Revy': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Billett-, økonomi- og sikkerhetsansvarlig': {0: 'økonomiansvarlig', 1: 'billett-/sikkerhetsansvarlig',
                                                            2: 'prodapp'},
              'Sikkerhetsansvarlig': {0: 'sikkerhetsansvarlig', 1: 'ingen', 2: 'annen prod'},
              'Teatersjef': {0: 'teatersjef', 1: 'ingen', 2: 'styret'},
              'Designkonsulent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'SIT Blæst': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Forfatter og skuespiller': {0: 'forfatter/skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Piano': {0: 'musiker', 1: 'piano', 2: 'annen prod'},
              'Sangteknisk instruksjon': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'},
              'Instuktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Kostymeoberst': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'},
              'Forpleiningssjef': {0: 'forpleier', 1: 'leder', 2: 'annen prod'},
              'Publikumsvert': {0: 'publikumsvert', 1: 'ingen', 2: 'annen prod'},
              'Konsulent Lyslaget': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'},
              'Skjermbilde': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Grafisk design': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'UKEsjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'SIT styret': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Deltaker': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sang-instruktør': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'},
              'Manusbearbeidelse': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Bygdefolk': {0: 'statist', 1: 'ingen', 2: 'annen prod'}, 'CD': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Performance på Husfest': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sminke- og hårstylist': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Fittings': {0: 'fittings', 1: 'ingen', 2: 'annen prod'},
              'Kulisser': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Kostymesjef': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Rekvisitør': {0: 'rekvisitør', 1: 'ingen', 2: 'annen prod'},
              'Repetitør': {0: 'repetitør', 1: 'ingen', 2: 'annen prod'},
              'Rekvisittassistent': {0: 'rekvisitør', 1: 'assistent', 2: 'annen prod'},
              'Markedsfører': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Illustratør': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'},
              'Orkestersjef': {0: 'kapellmester', 1: 'ingen', 2: 'annen prod'},
              'Videomester': {0: 'videodesigner', 1: 'ingen', 2: 'prodapp'},
              'Festtale': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lydeffekter': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'},
              'Administrasjon': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Medvirkende': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymemaker': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Økonomiansvarlig': {0: 'økonomiansvarlig', 1: 'ingen', 2: 'prodapp'},
              'Konsulent.2': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'kostyme': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Stemme på intervju': {0: 'skuespiller', 1: 'stemme på intervju', 2: 'annen prod'},
              'Masker': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Dirigent': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymesyer': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Oversettelse': {0: 'oversetter', 1: 'ingen', 2: 'prodapp'},
              'Lyddesign': {0: 'lyddesigner', 1: 'ingen', 2: 'prodapp'},
              'Suppesnuppe': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymekonsulent': {0: 'kostymesyer', 1: 'konsulent', 2: 'annen prod'},
              'Sminke': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Materialforvalter orkester': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Hospitant': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Festdeltaker': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Komponist': {0: 'komponist', 1: 'ingen', 2: 'prodapp'},
              'Scenograf': {0: 'scenograf', 1: 'ingen', 2: 'prodapp'},
              'Kostymeslusk': {0: 'kostymeslusk', 1: 'ingen', 2: 'annen prod'},
              'Teknisk Inspisient': {0: 'teknisk inspisient', 1: 'ingen', 2: 'prodapp'},
              'Sceneteknikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Komponistkonsulent': {0: 'komponist', 1: 'konsulent', 2: 'prodapp'},
              'Ymse': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Sangpedagog og repetitør': {0: 'sangpedagog/repetitør', 1: 'ingen', 2: 'prodapp'},
              'Tribuneansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'skuespiller': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Kommentator': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Statist': {0: 'statist', 1: 'ingen', 2: 'annen prod'},
              'Pianist': {0: 'musiker', 1: 'piano', 2: 'annen prod'},
              'Lystekniker': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Kunstnerisk koordinator': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Instruktør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Kulissegjeng': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Konsulent.3': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'lysreklamen': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'},
              'Produksjonsassistent': {0: 'produsent', 1: 'assistent', 2: 'prodapp'},
              'Manus': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'},
              'Regissør': {0: 'regissør', 1: 'ingen', 2: 'prodapp'},
              'Sangpedagog': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'},
              'Suppesnupp/-snopp': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Produksjonsansvarlig': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'Orkesterleder': {0: 'kapellmester', 1: 'ingen', 2: 'annen prod'},
              'Sekretær': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Koreograf': {0: 'koreograf', 1: 'ingen', 2: 'prodapp'},
              'Revyorkester': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Skuespillerinspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'},
              'Rekvisittansvarlig': {0: 'rekvisitør', 1: 'ingen', 2: 'annen prod'},
              'Kostymekoordinator': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'},
              'Musikksnopp': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Kostymegjeng': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Forpleiningsassistent': {0: 'forpleier', 1: 'assistent', 2: 'annen prod'},
              'Turneleder': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Konsulent video': {0: 'videotekniker', 1: 'konsulent', 2: 'annen prod'},
              'Nød-bærehjelp i tolvte time': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lydsnopp': {0: 'lydtekniker', 1: 'ingen', 2: 'annen prod'},
              'Lydig': {0: 'lydtekniker', 1: 'LYDig', 2: 'annen prod'},
              'Lysbilder v/FG': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymearbeidsleder': {0: 'kostymesyer', 1: 'arbeidsleder', 2: 'annen prod'},
              'Forteller': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Butler': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Grafikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Ouvreuse': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'PR-ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lyslaget': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'},
              'Økonomi': {0: 'økonomiansvarlig', 1: 'ingen', 2: 'prodapp'},
              'Scenearbeider': {0: 'scenearbeider', 1: 'ingen', 2: 'annen prod'},
              'Plakat': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'},
              'Slåssteknikk': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Skuespiller': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Smikør': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Rekvisitørkonsulent': {0: 'rekvisitør', 1: 'konsulent', 2: 'annen prod'},
              'Følgespotlaget': {0: 'lystekniker', 1: 'følgespot', 2: 'annen prod'},
              'Videografiker': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'myggkonsulent': {0: 'myggslusk', 1: 'konsulent', 2: 'annen prod'},
              'Videolaget': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'},
              'Nestleder': {0: 'nestleder', 1: 'ingen', 2: 'prodapp'},
              'Videokomiteen': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'},
              'Oversetter/instruktør/produsent': {0: 'oversetter/regissør/produsent', 1: 'ingen', 2: 'prodapp'},
              'Koreografisk ass.': {0: 'koreograf', 1: 'assistent', 2: 'prodapp'},
              'Stemmepedagog': {0: 'sangpedagog', 1: 'ingen', 2: 'prodapp'},
              'FFK': {0: 'forfatter', 1: 'konsulent', 2: 'annen prod'},
              'Innbildt suppedirektør': {0: 'produsent', 1: 'innbilt', 2: 'prodapp'},
              'Skuespiller ': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Musikalsk ansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Konferansier': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Inspisient': {0: 'inspisient', 1: 'ingen', 2: 'prodapp'},
              'Eva Person': {0: 'skuespiller', 1: 'Eva Person', 2: 'annen prod'},
              'Musikalsk leder': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kulissesnekker': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Instruktørveileder': {0: 'regissør', 1: 'konsulent', 2: 'prodapp'},
              'Kommandør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymekommandør': {0: 'kostymekommandør', 1: 'ingen', 2: 'prodapp'},
              'Kostymesyere': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Sminke/parykk': {0: 'sminkør', 1: 'ingen', 2: 'annen prod'},
              'Orkesteret': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Noteskriver': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Film': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Publikumsinspisient': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Orkester': {0: 'musiker', 1: 'ingen', 2: 'annen prod'},
              'Forfatter': {0: 'forfatter', 1: 'ingen', 2: 'annen prod'},
              'Kostymeskredder': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Pr-gjeng': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kulisse': {0: 'kulissebygger', 1: 'ingen', 2: 'annen prod'},
              'Produsentassistent': {0: 'produsent', 1: 'assistent', 2: 'prodapp'},
              'Musikkarrangement': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Diverse': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymegjengen': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Systemtekniker': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Suppesnopp': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kostymer': {0: 'kostymesyer', 1: 'ingen', 2: 'annen prod'},
              'Verkstedansvarlig': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lysreklamen': {0: 'lysreklamist', 1: 'ingen', 2: 'annen prod'},
              'Video': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'},
              'Regiveileder': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'},
              'Byfolk': {0: 'statist', 1: 'ingen', 2: 'annen prod'},
              'Arrangementskomité': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lysmester': {0: 'lysdesigner', 1: 'ingen', 2: 'prodapp'},
              'Jazz på dass': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Personal- og innkjøpsansvarlig - kostyme': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Artist': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Lyskonsulent': {0: 'lystekniker', 1: 'konsulent', 2: 'annen prod'},
              'Kapellmester': {0: 'kapellmester', 1: 'ingen', 2: 'annen prod'},
              'Produksjonskonsulent': {0: 'produsent', 1: 'konsulent', 2: 'prodapp'},
              'Dovrefarer': {0: 'tittel', 1: 'ingen', 2: 'ingen'}, 'Regi': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Bilderedaktør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Kupper': {0: 'KUPer', 1: 'ingen', 2: 'annen prod'},
              'Lys- og sceneinspisient': {0: 'teknisk inspisient', 1: 'ingen', 2: 'prodapp'},
              'Jørgen Person': {0: 'skuespiller', 1: 'Jørgen Person', 2: 'annen prod'},
              'Direktør': {0: 'tittel', 1: 'ingen', 2: 'ingen'},
              'Produsent': {0: 'produsent', 1: 'ingen', 2: 'prodapp'},
              'Skuespillere': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Gjendiktning sangtekster': {0: 'gjendikter', 1: 'ingen', 2: 'annen prod'},
              'VK': {0: 'videotekniker', 1: 'ingen', 2: 'annen prod'},
              'Plakattegner': {0: 'grafiker', 1: 'ingen', 2: 'annen prod'},
              'Forpleining': {0: 'forpleier', 1: 'ingen', 2: 'annen prod'},
              'Skuespiller.1': {0: 'skuespiller', 1: 'ingen', 2: 'annen prod'},
              'Lyslag': {0: 'lystekniker', 1: 'ingen', 2: 'annen prod'}}

arsverv_dict = {'input': {0: 'Verv', 1: 'Rolle', 2: 'Type'},
                'Barneteatersjef': {0: 'Barneteatersjef', 1: 'ingen', 2: 'styre'},
                'Sekretær': {0: 'nestleder', 1: 'ingen', 2: 'styre'},
                'Hybelassistent': {0: 'hybelassistent', 1: 'ingen', 2: 'intern-gjeng'},
                'VK-sjef Teater-UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Teaterkontakt': {0: 'teaterkontakt', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Nestleder Teater-UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Nestleder Revy Teater-UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Kunstnersik råd': {0: 'medlem av Kunstnerisk råd', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Klubbens Fortjenestemedalje i Stål': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'FK-sjef Teater-UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Filmgjengen': {0: 'filmgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Kunstnerisk Råd': {0: 'medlem av Kunstnerisk råd', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Web-gjengen': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Kulissesjef': {0: 'kulissesjef', 1: 'ingen', 2: 'styre'},
                'Repertoiransvarlig': {0: 'kunstnerisk ansvarlig', 1: 'ingen', 2: 'styre'},
                'Hybelgjengen': {0: 'hybelgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'WEB-gjeng': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'PR-gjengen': {0: 'PR-gjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Julefestkomitéen (JFK)': {0: 'medlem av Julefestkomiteen', 1: 'ingen', 2: 'intern-gjeng'},
                'Nestleder': {0: 'nestleder', 1: 'ingen', 2: 'styre'},
                'REGI-sjef Teater-UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Kunstneriskansvarlig': {0: 'Tittel', 1: 'ansvar for kunstnerisker', 2: 'ingen'},
                'Idrettsoppkvinne': {0: 'idrettsoppkvinne', 1: 'ingen', 2: 'intern-gjeng'},
                'SIT-Web': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Teatersjef UKA-11': {0: 'UKEteatersjef', 1: 'ingen', 2: 'styre'},
                'Hybelgjeng': {0: 'hybelgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Baksidakontakt ': {0: 'baksidekontakt', 1: 'ingen', 2: 'intern-gjeng'},
                'Rekvisittgjengen': {0: 'rekvisittansvarlig', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Økonomisjef': {0: 'økonomisjef', 1: 'ingen', 2: 'styre'},
                'Ballsjef': {0: 'ballerina', 1: 'ingen', 2: 'intern-gjeng'},
                'Rekvisittansvarlig': {0: 'rekvisittansvarlig', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Idrettsoppkvinner': {0: 'idrettsoppkvinne', 1: 'ingen', 2: 'intern-gjeng'},
                'PR- og produksjonskoordinator': {0: 'PR- og produksjonskoordinator', 1: 'ingen', 2: 'styre'},
                'Videogjeng': {0: 'filmgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Web-gjeng': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Kulturutvalget': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Videogjengen': {0: 'filmgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Repertoirutvalg': {0: 'medlem av Kunstnerisk råd', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Ballerina': {0: 'ballerina', 1: 'ingen', 2: 'intern-gjeng'},
                'SIT-web': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'PR-gjeng': {0: 'PR-gjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Styremedlem': {0: 'styremedlem', 1: 'ingen', 2: 'styre'},
                'SOS-kontakt': {0: 'veldedighetskontakt', 1: 'ingen', 2: 'ekstern-gjeng'},
                'SIT-arkivet': {0: 'arkivar', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Hybelsjef': {0: 'hybelsjef', 1: 'ingen', 2: 'styre'},
                'Idrettsoppmann': {0: 'idrettsoppkvinne', 1: 'ingen', 2: 'intern-gjeng'},
                'Seksjonsassistent UKA': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Webgjengen': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Plateselskapet': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'SIT Brannmann': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Økonomiansvarlig': {0: 'økonomisjef', 1: 'ingen', 2: 'styre'},
                'Kosymearkivar': {0: 'kostymearkivar', 1: 'ingen', 2: 'intern-gjeng'},
                'Arkivar': {0: 'arkivar', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Soddgjengen': {0: 'soddgjengis', 1: 'ingen', 2: 'intern-gjeng'},
                'Kunstnerisk koordinator': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Kasserer': {0: 'økonomisjef', 1: 'ingen', 2: 'styre'},
                'Baksidekontakt': {0: 'baksidekontakt', 1: 'ingen', 2: 'intern-gjeng'},
                'Kostymesjef': {0: 'kostymesjef', 1: 'ingen', 2: 'styre'},
                'WEB-gjengen': {0: 'webgjengis', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Ukeplakattegner': {0: 'Tittel', 1: 'ingen', 2: 'ingen'},
                'Teatersjef': {0: 'teatersjef', 1: 'ingen', 2: 'styre'},
                'Sminkeansvarlig': {0: 'sminkeansvarlig', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Kunstnerisk råd': {0: 'medlem av Kunstnerisk råd', 1: 'ingen', 2: 'ekstern-gjeng'},
                'NATF-kontakt': {0: 'teaterkontakt', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Veldedighetskontakt': {0: 'veldedighetskontakt', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Kunstnerisk Ansvarlig': {0: 'kunstnerisk ansvarlig', 1: 'ingen', 2: 'styre'},
                'PR og Produksjonskoordinator': {0: 'PR- og produksjonskoordinator', 1: 'ingen', 2: 'styre'},
                'Skuespillerkontakt': {0: 'skuespillerkontakt', 1: 'ingen', 2: 'ekstern-gjeng'},
                'Teaterkomite': {0: 'styremedlem', 1: 'Teaterkomiteen', 2: 'styre'},
                'Kostymearkivar': {0: 'kostymearkivar', 1: 'ingen', 2: 'intern-gjeng'},
                'Kunstnerisk ansvarlig': {0: 'kunstnerisk ansvarlig', 1: 'ingen', 2: 'styre'},
                'PR- og produksjonsansvarlig': {0: 'PR- og produksjonskoordinator', 1: 'ingen', 2: 'styre'}}


# nummer_dict = {'Rocamboles vise': {'produksjon': '1917_baccarat', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1917_rocamboles_vise.mp3.flv'}, 'Trondhjemsvisen (Men det er no´n ganske få detaljer)': {'produksjon': '1917_baccarat', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1917_trondhjemsvisen.mp3.flv'}, 'Hadjet-Larschens vise': {'produksjon': '1919_jazz', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1919_hadjet-larschens_vise.mp3.flv'}, 'Bertin Margs Vise': {'produksjon': '1919_jazz', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1919_bertin_margs_vise.mp3.flv'}, 'Aktiemæglerens vise': {'produksjon': '1919_jazz', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1919_aktiemeglerens_vise.mp3.flv'}, 'Regningsbudets vise': {'produksjon': '1921_rah-ta-tah', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1921_regningsbudets_vise.mp3.flv'}, 'Olav Styggesens dropa': {'produksjon': '1921_rah-ta-tah', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1921_olav_styggesens_dropa.mp3.flv'}, 'Duet - Per og Norma': {'produksjon': '1923_charivari', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1923_duet.mp3.flv'}, 'Drikkevise (Det er liddelig flaut)': {'produksjon': '1925_bing_bang', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1925_drikkevise.mp3.flv'}, 'Duet (Det er så mange ting)': {'produksjon': '1925_bing_bang', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1925_duet.mp3.flv'}, 'Hjemve': {'produksjon': '1925_bing_bang', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1925_hjemve.mp3'}, 'Måkevisen': {'produksjon': '1925_bing_bang', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1925_maakevisen.mp3.flv'}, 'Studentervisen (Tenk om jeg var millionær)': {'produksjon': '1925_bing_bang', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1925_studentervisen.mp3.flv'}, 'Nu klinger': {'produksjon': '1929_cassa_rossa', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1929_nu_klinger.mp3'}, '80-årenes sportsvise': {'produksjon': '1931_mammon_ra', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1931_80-aarenes_sportsvise.mp3.flv'}, 'Rasmussens vise': {'produksjon': '1931_mammon_ra', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1931_rasmussens_vise.mp3.flv'}, 'Vi har vår egen lille verden': {'produksjon': '1931_mammon_ra', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1931_vaar_egen_lille_verden.mp3.flv'}, 'Den musikalske trikkefører': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_den_musikalske_trikkeforer.mp3.flv'}, 'Hu og hei': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_hu_og_hei.mp3.flv'}, 'Sang ved typisk massebryllup': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_massebryllup.mp3.flv'}, 'Psykoanalytisk vuggevise': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_psykoanalytisk_vuggevise.mp3.flv'}, 'Vestfronten': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_vestfronten.mp3.flv'}, 'En vise om Munkholmen': {'produksjon': '1933_namesis', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1933_munkholmen.mp3.flv'}, 'Studentervise 1935': {'produksjon': '1935_dek-e-du', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1935_studentervise.mp3.flv'}, 'Missing links vise': {'produksjon': '1937_var-i-tass', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1937_missing_link.mp3.flv'}, 'Vise ved innvielse av Trondhjems bombesikre kjeller': {'produksjon': '1937_var-i-tass', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1937_bombesikre_rom.mp3.flv'}, 'Barbereren fra Ila': {'produksjon': '1937_var-i-tass', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1937_barbereren_fra_ila.mp3.flv'}, 'Drikkevise (La det gå som det vil)': {'produksjon': '1939_tempora', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1939_drikkevise.mp3.flv'}, 'Duett': {'produksjon': '1939_tempora', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1939_duett.mp3.flv'}, 'Gerd og Ottos vise': {'produksjon': '1939_tempora', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1939_gerd_og_otto.mp3.flv'}, 'Holberg-monolog': {'produksjon': '1939_tempora', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1939_holberg-monolog.mp3.flv'}, 'Åpningssang': {'produksjon': '1945_go-a-head', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1945_aapningssang.mp3.flv'}, 'Jakob på drømmestigen': {'produksjon': '1945_go-a-head', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1945_jakob_paa_drommestigen.mp3.flv'}, 'Mannjevning': {'produksjon': '1945_go-a-head', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1945_mannjevning.mp3.flv'}, 'Pia og soldaten': {'produksjon': '1945_go-a-head', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1945_pia_og_soldaten.mp3.flv'}, 'Skapelsen': {'produksjon': '1947_fandango', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1947_skapelsen.mp3.flv'}, 'Regnværsserenade': {'produksjon': '1947_fandango', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1947_regnvarsserenade.mp3.flv'}, 'Kontiki-song': {'produksjon': '1947_fandango', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1947_romantiki.mp3.flv'}, 'Brannmannssprøyt': {'produksjon': '1947_fandango', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1947_brannmannssproyt.mp3.flv'}, 'Drikkevise (Oppe i et juletre)': {'produksjon': '1949_domino', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1949_drikkevise.mp3.flv'}, 'Duett på Baklandet': {'produksjon': '1949_domino', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1949_duett_paa_baklandet.mp3.flv'}, 'Kroverten': {'produksjon': '1949_domino', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1949_kroverten.mp3.flv'}, 'Morgenvise': {'produksjon': '1949_domino', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1949_morgenvise.mp3.flv'}, 'Talekoret (Brede seil)': {'produksjon': '1949_domino', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1949_talekoret.mp3.flv'}, 'Ouverture': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_ouverture.mp3.flv'}, 'Byggstudent Havre': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_byggstudent_havre.mp3.flv'}, 'Hybelvisa (I et bittelite rom oppå loftet)': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_hybelvisa.mp3.flv'}, 'Flathundens sang': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_flathundens_sang.mp3.flv'}, 'Hatten': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_hatten.mp3.flv'}, 'Morgenhymne': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_morgenhymne.mp3.flv'}, 'Vosserull (Gutane frå Voss)': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_vosserull.mp3.flv'}, 'Professormonolog': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_professormonolog.mp3.flv'}, 'Velkomstsang (med tale)': {'produksjon': '1951_akk-a-mei', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1951_velkomstsang.mp3.flv'}, 'Åpningsvise (Lille meg)': {'produksjon': '1953_gustibus', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1953_aapningsvise.mp3.flv'}, 'Debutantenes vise': {'produksjon': '1953_gustibus', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1953_debutantenes_vise.mp3.flv'}, 'Utrøndersk virksomhet': {'produksjon': '1953_gustibus', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1953_utrondersk_virksomhet.mp3.flv'}, 'Multeplukkeren': {'produksjon': '1953_gustibus', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1953_multeplukkeren.mp3.flv'}, 'Kaldflir': {'produksjon': '1953_gustibus', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1953_kaldflir.mp3.flv'}, 'Mohrens sista suck 1. akt (1954)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1954_mohren_1.mp3'}, 'Mohrens sista suck 2. akt (1954)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1954_mohren_2.mp3'}, 'Mohrens sista suck 3. akt (1954)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1954_mohren_3.mp3'}, 'Veteraner (Det var i 1905)': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_veteraner.mp3.flv'}, 'Vuggevise': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_vuggevise.mp3.flv'}, 'Den gamle sang': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_den_gamle_sang.mp3.flv'}, 'Sportsfiskeren': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_sportsfiskeren.mp3.flv'}, 'Dagdrøm': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_dagdrom.mp3.flv'}, 'Presten': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_presten.mp3.flv'}, 'Kossemos': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_kossemos.mp3.flv'}, 'O-la-la': {'produksjon': '1955_vau-de-ville', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1955_o-la-la.mp3.flv'}, 'Et annet sted': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_et_annet_sted.mp3.flv'}, 'Glad og fri': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_glad_og_fri.mp3.flv'}, 'Kalson (fra renholdsverket)': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_kalson.mp3.flv'}, 'Kjøp bil': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_kjop_bil.mp3.flv'}, 'Det store spill (Golf)': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_det_store_spill.mp3.flv'}, 'Calypso': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_calypso.mp3.flv'}, 'Krussedull': {'produksjon': '1957_krussedull', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1957_krussedull.mp3.flv'}, 'Mohrens sista suck 1. akt (1958)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1958_mohren_1.mp3'}, 'Mohrens sista suck 2. akt (1958)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1958_mohren_2.mp3'}, 'Mohrens sista suck 3. akt (1958)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1958_mohren_3.mp3'}, 'Duell': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_duell.mp3.flv'}, 'Munke-liv': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_munke-liv.mp3.flv'}, 'Munke-øl': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_munke-ol.mp3.flv'}, 'Memoirer': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_memoirer.mp3.flv'}, 'Ælg': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_alg.mp3.flv'}, 'The Cnayp brothers': {'produksjon': '1959_krakatitt', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1959_the_cnayp_brothers.mp3.flv'}, 'Mohrens sista suck 1. akt (1961)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1961_mohren_1.mp3'}, 'Mohrens sista suck 2. akt (1961)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1961_mohren_2.mp3'}, 'Mohrens sista suck 3. akt (1961)': {'produksjon': '', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1961_mohren_3.mp3'}, 'Justitia': {'produksjon': '1963_kissmett', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1963_justitia.flv'}, 'Delikat': {'produksjon': '1963_kissmett', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1963_delikat.flv'}, 'Graverne': {'produksjon': '1963_kissmett', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1963_graverne.flv'}, 'The brothers safe': {'produksjon': '1965_jo_ser_du', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1965_the_brothers_safe.mp3'}, 'Skilsmissesladder': {'produksjon': '1967_jarragakk', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1967_skilsmissesladder.mp3'}, 'MS Goddagen': {'produksjon': '1967_jarragakk', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1967_ms_goddagen.mp3'}, 'To pils': {'produksjon': '1967_jarragakk', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1967_to_pils.mp3'}, 'Gullkvartetten': {'produksjon': '1967_jarragakk', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1967_gullkvartetten.mp3'}, 'Ouvertyre': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_1_ouvertyre.mp3'}, 'Mutasjon': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_2_mutasjon.mp3'}, 'Livets fjær': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_3_livets_fjar.mp3'}, 'Bunny': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_4_bunny.mp3'}, 'Månen': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_5_maanen.mp3'}, 'Gullkalven': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_6_gullkalven.mp3'}, 'Evolusjonsetyde': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_7_evolusjonsetyde.mp3'}, 'Pyroman': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_8_pyroman.mp3'}, 'Norway fair': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_9_norway_fair.mp3'}, 'Gjengangere': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_10_gjengangere.mp3'}, 'Amors piller': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_11_amors_piller.mp3'}, 'Finale': {'produksjon': '1969_prinkipo', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1969_12_finale.mp3'}, 'Åja (åpning)': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_1_aaja.mp3'}, 'Farevise': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_11_farevise.mp3'}, 'Navnevise': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_3_navnevise.mp3'}, 'Jænsn å æ': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_4_jansn_aa_a.mp3'}, 'Skitt i by´n': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_5_skitt_i_byn.mp3'}, 'Solidaritet I': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_solidaritet_i.mp3'}, 'Tygge grus': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_tygge_grus.mp3'}, 'Et argument for det bestående': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_et_argument_for_det_bestaaende.mp3'}, 'Gi et svar': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_gi_et_svar.mp3'}, 'Prostituert': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_10_prostituert.mp3'}, 'Solidaritet II': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_12_solidaritet_ii.mp3'}, 'Det er de fleste som dør': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_13_det_er_de_fleste_som_dor.mp3'}, 'Lænsmainn i Nyårk': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_14_lansmainn_i_nyaark.mp3'}, 'Skapt for å bile': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_15_skapt_for_aa_bile.mp3'}, 'Og byen skrek': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_16_og_byen_skrek.mp3'}, 'Vi skal rehabilitere': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_17_vi_skal_rehabilitere.mp3'}, 'Du svever fritt omkring': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_18_du_svever_fritt_omkring.mp3'}, 'Sterke røde hender': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_19_sterke_rode_hender.mp3'}, 'Du skal sprøytes full av buljong': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_20_du_skal_sproytes_full_av_buljong.mp3'}, 'Alle har respekt for meg': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_21_alle_har_respekt_for_meg.mp3'}, 'Når du er fire år': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_22_naar_du_er_fire_aar.mp3'}, 'Åja (finale)': {'produksjon': '1971_aja', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1971_23_aaja.mp3'}, 'Ouvertyre (Skubidi)': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_1_ouvertyre.mp3'}, 'Automater': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_2_automater.mp3'}, 'Tango sympatie': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_3_tango_sympatie.mp3'}, 'Ansettelsesvise': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_4_ansettelsesvise.mp3'}, 'Trondhjæm, Trondhjæm': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_5_trondhjem,_trondhjem.mp3'}, 'Eg har ei trøye': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_6_eg_har_ei_troye.mp3'}, 'Speil': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_7_speil.mp3'}, 'Dobbeltrensa': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_8_dobbeltrensa.mp3'}, 'Kjære gamle Basse': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_9_kjare_gamle_basse.mp3'}, 'Skubidi': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_10_skubidi.mp3'}, 'Det er deg jeg vil ha': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_11_det_er_deg_jeg_vil_ha.mp3'}, 'Trafikkvise': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_12_trafikkvise.mp3'}, 'Kjære lille scene': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_13_kjare_lille_scene.mp3'}, 'Orden og system fallera': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_14_orden_og_system_fallera.mp3'}, 'Det var meg': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_15_det_var_meg.mp3'}, 'Livets gåte': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_16_livets_gaate.mp3'}, 'Nær demokrati': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_17_nar_demokrati.mp3'}, 'Smile pent': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_18_smile_pent.mp3'}, 'Sørensens marsj': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_19_sorensens_marsj.mp3'}, 'Ekspert(v)ise': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_20_ekspert(v)ise.mp3'}, 'Krokus': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_21_krokus.mp3'}, 'Hundre blomstrar': {'produksjon': '1973_skubidi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1973_22_hundre_blomstrar.mp3'}, 'Ouverture (Sirkuss)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_1_ouverture.mp3'}, 'Brainnsprøyt': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_2_brainnsproyt.mp3'}, 'Presseduett': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_3_presseduett.mp3'}, 'Ryktevise': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_4_ryktevise.mp3'}, 'Skillingsvise (Halmrast)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_5_skillingsvise_*(halmrast).mp3'}, 'Studentersang': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_6_studentersang.mp3'}, 'Hei Skolebakken 8': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_7_hei_skolebakken_8.mp3'}, 'Chipssang': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_8_chipssang.mp3'}, 'Gratulasjonssang': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_9_gratulasjonssang.mp3'}, 'Kronelegi': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_10_kronelegi.mp3'}, 'Munkgata': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_11_munkgata.mp3'}, 'Skillingsvise (Historien går sin gang)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_12_skillingsvise_(historien_gaar_sin_gang).mp3'}, 'Da-i-tida': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_13_da-i-tida.mp3'}, 'Skillingsvise (Historien gikk sin gang)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_14_skillingsvise_(historien_gikk_sin_gang).mp3'}, 'Visa om fettet': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_15_visa_om_fettet.mp3'}, 'Politidamas entré': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_16_politidamas_entre.mp3'}, 'Plattfodblues': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_17_plattfodblues.mp3'}, 'Tragisk vise': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_18_tragisk_vise.mp3'}, 'Grønne enger': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_19_gronne_enger.mp3'}, 'Smilende offiserer': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_20_smilende_offiserer.mp3'}, 'Trøndelag (Sirkuss)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_21_trondelag.mp3'}, 'Skillingsvise (Moral)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_22_skillingsvise_(moral).mp3'}, 'Sirkussmusikk (Finale)': {'produksjon': '1975_sirkuss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1975_23_skillingsvise_(finale).mp3'}, 'Ouverture (Laugalaga)': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_1.mp3'}, 'Jubileumsvelkomst': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_2.mp3'}, 'Trondheim by': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_3.mp3'}, 'Drømmeby - Fiskefarse': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_4.mp3'}, 'Hun og han': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_5.mp3'}, 'Nidvise': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_6.mp3'}, 'Agent theme': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_7.mp3'}, 'Herodes´ disipler': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_8.mp3'}, 'Blyg æ, nei?': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_9.mp3'}, 'Regla': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_10.mp3'}, 'Sur & blå': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_11.mp3'}, 'Blue jeans': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_12.mp3'}, 'Siste skrik': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_13.mp3'}, 'Skrap': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_14.mp3'}, 'Flosshattenes inntogsmarsj': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_15.mp3'}, 'Tid-vise': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_16.mp3'}, 'Nøkken': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_17.mp3'}, 'Vals': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_18.mp3'}, 'Mørk ballade': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_19.mp3'}, 'Laugalaga': {'produksjon': '1977_laugalaga', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1977_20.mp3'}, 'Rødhettes vise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-1-1.m4a'}, 'Ulvens vise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-1-2.m4a'}, 'Revens første vise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-1-3.m4a'}, 'Harens vise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-1-4.m4a'}, 'Tannfilevise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-2-1.m4a'}, 'Revens andre vise': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-2-2.m4a'}, 'Jakten er slutt': {'produksjon': '1977_rodhette_og_ulven_barneteater_uka_1977', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP775-2-3.m4a'}, 'Cassa Rossa': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_1.mp3'}, 'Las Vegas': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_2.mp3'}, 'Joggerock': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_3.mp3'}, 'Prinsens gate': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_4.mp3'}, 'Erichsen': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_5.mp3'}, 'Rødhette': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_6.mp3'}, 'Tamburinrock': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_7.mp3'}, 'Kassa': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_8.mp3'}, 'Ayatollahs lullaby': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_9.mp3'}, 'Den hydrauliske rhododendron': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_10.mp3'}, 'Reimgjerdet hopsasa': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_11.mp3'}, 'Vampyrvise': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_12.mp3'}, 'Akk og hjemve': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_13.mp3'}, 'Ræggeti': {'produksjon': '1979_raggeti', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1979_14.mp3'}, 'Fossen': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-1-1.m4a'}, 'Skogsang': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-1-2.m4a'}, 'Rørsang': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-1-3.m4a'}, 'Tristesang': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-2-2.m4a'}, 'Hikkedrikkesang': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-2-1.m4a'}, 'Pianostemmerlåt': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-2-3.m4a'}, 'Festsang': {'produksjon': '1979_ikke_ror_barneteater_uka_79', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/BUEP794-2-4.m4a'}, 'Nu Klinger - Debutantenes vise (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_1.mp3'}, 'Hadjet-Larchens vise (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_2.mp3'}, 'Hjemve - Tramp (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_3.mp3'}, 'Farvel Cirkus (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_4.mp3'}, 'Veteraner (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_5.mp3'}, 'Rasmussens vise (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_6.mp3'}, 'Reimgjerdet hopsasa (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_7.mp3'}, 'Pyromanvisa (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_8.mp3'}, 'Klovna og sjela (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_9.mp3'}, 'Livets fjær (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_10.mp3'}, 'Vi har vår egen lille Verden (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_11.mp3'}, 'En tradisjonell forestilling i Lilleby (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_12.mp3'}, 'Trikkeførerrumba (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_13.mp3'}, 'Kaldflir (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_14.mp3'}, 'The Cnayp brothers (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_15.mp3'}, 'Karlson fra reinholdsverket (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_16.mp3'}, 'Blokkens ansikt (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_17.mp3'}, 'Juryen - Han skal dømmes (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_18.mp3'}, 'Klubbaften (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_19.mp3'}, 'Dagdrøm - (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_20.mp3'}, 'Calypso (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_21.mp3'}, 'Velkomstsangen - Krokus (Gjengangere)': {'produksjon': '1980_gjengangere_1980', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1970_gjengangere_22.mp3'}, 'Ouvertyre (Fan Tutte)': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_1.mp3'}, 'Det blomstrende parkometer': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_2.mp3'}, 'Pils og slips og politikk': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_3.mp3'}, 'Trivelige Trondhjem': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_4.mp3'}, 'Ei dopa ei': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_5.mp3'}, 'I hagen': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_6.mp3'}, 'His way': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_7.mp3'}, 'Frelserens veger': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_8.mp3'}, 'Dyrenes tema': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_9.mp3'}, 'Gamle hus': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_10.mp3'}, 'Lech Walesa': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_11.mp3'}, 'F-16': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_12.mp3'}, 'Finale (Fan Tutte)': {'produksjon': '1981_fan_tutte', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1981_13.mp3'}, 'Åpningssang (E-de-ber)': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_1.mp3'}, 'Reisebrev frå Flå': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_2.mp3'}, 'Opp og ned': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_3.mp3'}, 'Vignett': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_12.mp3'}, 'Hjemmekos': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_5.mp3'}, 'Sterke mennesker': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_6.mp3'}, 'Hagebruk': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_6.mp3'}, 'Terrific Trondheim': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_8.mp3'}, 'Otto': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_9.mp3'}, 'Trønderrock': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_10.mp3'}, 'Dårlig kvinne': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_11.mp3'}, 'På UKA': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_13.mp3'}, 'Bomberomrumba': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_14.mp3'}, 'Finale (E-de-ber)': {'produksjon': '1983_e_de_ber', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1983_15.mp3'}, 'Ouverture (Narr-i-ciss)': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_1.mp3'}, 'Narr-i-ciss': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_2.mp3'}, 'Sammen på Tinget': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_3.mp3'}, 'Happy jippi': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_4.mp3'}, 'Trønderbart': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_5.mp3'}, 'Å Å Å Å': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_6.mp3'}, 'Musikk': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_7.mp3'}, 'Ligger vi sammen': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_8.mp3'}, 'Snusen': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_9.mp3'}, 'En gang bare en': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_10.mp3'}, 'Treningsvise': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_11.mp3'}, 'Du og æ og by´n': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_12.mp3'}, 'Trappa': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_13.mp3'}, 'Finale (Narr-i-ciss)': {'produksjon': '1985_narr-i-ciss', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1985_14.mp3'}, 'De-cha-vi': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_1.mp3'}, 'Rio på Rye': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_8.mp3'}, 'Olav Trygvesøns vise': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_2.mp3'}, 'Pingwienervals': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_3.mp3'}, 'Marilyn': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_4.mp3'}, 'Sleipe Johan': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_5.mp3'}, 'Hjæmbrygga': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_6.mp3'}, 'Det va´ den vår´n...': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_7.mp3'}, 'Pompel og Pilt': {'produksjon': '1987_de-cha-vi', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1987_pompel_og_pilt.flv'}, 'Kaffe og vaffel': {'produksjon': '1987_de-cha-vi', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1987_kaffe_og_vaffel.flv'}, 'Kaffe og Vaffel (lyd)': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_9.mp3'}, 'Ænkeltvindu': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_10.mp3'}, 'En innflytters vise': {'produksjon': '1987_de-cha-vi', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1987_en_innflytters_vise.flv'}, 'En innflytters vise (lyd)': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_11.mp3'}, 'Kardemomme by': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_12.mp3'}, 'Kom og se!': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_13.mp3'}, 'En spennende dag': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_14.mp3'}, 'Romantikk': {'produksjon': '1987_de-cha-vi', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1987_romantikk_.flv'}, 'Romantikk (lyd)': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_15.mp3'}, 'Det umulige er mulig': {'produksjon': '1987_de-cha-vi', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1987_det_umulige_er_mulig.flv'}, 'Det umulige er mulig (lyd)': {'produksjon': '1987_de-cha-vi', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1987_16.mp3'}, 'Anna og jeg og Ole Jonny': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_anna_og_jeg_og_ole_jonny.flv'}, 'Vårres vesle vei': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_varres_vesle_vei.flv'}, 'Trondhjæm midt i hjertet': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_trondhjam_midt_i_hjertet.flv'}, 'Dåmkoret': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_damkoret.flv'}, 'Ska det vera, ska det vera': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_ska_det_vera_ska_det_vera.flv'}, 'Surfer´n': {'produksjon': '1989_jagguma', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1989_surfern.flv'}, 'Er det sant': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_01.mp3'}, 'Køfri': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_02.mp3'}, 'Laks': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_03.mp3'}, 'Plingfæst': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_04.mp3'}, 'Trægost': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_05.mp3'}, 'Rockeprinsen': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_06.mp3'}, 'Ut på by´n': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_07.mp3'}, 'Munken': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_08.mp3'}, 'Teletorg': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_09.mp3'}, 'Turist i egen by': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_10.mp3'}, 'Kjappe krigers tango': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_11.mp3'}, 'God natt': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_12.mp3'}, 'Helse frelse': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_13.mp3'}, 'Gråt min balalaika': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_14.mp3'}, 'Bom-T-Bom/Ett skritt tilbake, to skritt fram': {'produksjon': '1991_bom-t-bom', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1991_15.mp3'}, 'Åpning (Fabula)': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-1.m4a'}, 'Drittsekk': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-2.m4a'}, 'Blainnalag': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-3.m4a'}, 'Juan Antonio': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-4.m4a'}, 'Hvalvise': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-5.m4a'}, 'Virtual reality': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-6.m4a'}, 'Frokost': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-7.m4a'}, 'Kjøssekurs i Frausundvær': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-8.m4a'}, 'Die Bobilferie': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-9.m4a'}, 'Siste vakt på Fyret': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-10.m4a'}, 'Bare burger': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-11.m4a'}, 'Bill the kid': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-12.m4a'}, 'Fattigtrondhjem': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-13.m4a'}, 'Refrenget': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-15.m4a'}, 'For støgg for OL': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-14.m4a'}, 'Finale (Fabula)': {'produksjon': '1993_Fabula', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-16.m4a'}, 'Gjemselsangen': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-17.m4a'}, 'Slimkongesangen': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-18.m4a'}, 'Rimesang': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-19.m4a'}, 'Bergliots sang': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-20.m4a'}, 'Timeplansangen': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-21.m4a'}, 'En arm for mye': {'produksjon': '1993_hallo_lille_pyse_barneteater_uka_-93', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/UKACD93-22.m4a'}, 'Åpning (Skjer-mer-@)': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_01.m4a'}, 'Petter Gevær': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_02.m4a'}, 'Tør vi mene noe om muslimer': {'produksjon': '1995_skjer-mer-a', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1995_tor_vi_mene_noe_om_muslimer.flv'}, 'Tør vi mene noe om muslimer (lyd)': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_03.m4a'}, 'Hva er kjærlighet, hva er sex': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_04.m4a'}, 'Det det va og DDE': {'produksjon': '1995_skjer-mer-a', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1995-det_det_va.flv'}, 'Det det va og DDE (lyd)': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_05.m4a'}, 'Veita': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_06.m4a'}, 'Buran-spelet': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_07.m4a'}, 'Hjørdis´ siste jul': {'produksjon': '1995_skjer-mer-a', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/1995_hjordis.flv'}, 'Hjørdis´ siste jul (lyd)': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_08.m4a'}, 'Jynarn': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_09.m4a'}, 'Var-hattkaill': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_10.m4a'}, 'En liten sang om engasjement': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_11.m4a'}, 'Maria': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_12.m4a'}, 'Gjør det på TV': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_13.m4a'}, 'Finale (Skjer-mer-@)': {'produksjon': '1995_skjer-mer-a', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_14.m4a'}, 'Drikkevise koral': {'produksjon': '1995_vi_kjente_ham_igrunnen_ganske_godt_nattforestilling_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_15.m4a'}, 'Takk bare bra': {'produksjon': '1995_vi_kjente_ham_igrunnen_ganske_godt_nattforestilling_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_16.m4a'}, 'Beep': {'produksjon': '1995_vi_kjente_ham_igrunnen_ganske_godt_nattforestilling_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_17.m4a'}, 'Fix & Alexa gjør rent bord': {'produksjon': '1995_slottet_ritarandora_barneteater_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_18.m4a'}, 'Den slemme sangen': {'produksjon': '1995_slottet_ritarandora_barneteater_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_19.m4a'}, 'Georgsangen': {'produksjon': '1995_slottet_ritarandora_barneteater_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_20.m4a'}, 'Dette kan vi kalle happy ending': {'produksjon': '1995_slottet_ritarandora_barneteater_uka_1995', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1995_21.m4a'}, 'Trondheimsvise (Alt-er-sex)': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_01.m4a'}, 'Why I speak': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_02.m4a'}, 'Drikkevise (Alt-er-sex)': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_03.m4a'}, 'Ut av skapet': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_04.m4a'}, 'Mona & Fiona': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_05.m4a'}, 'Om morran': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_06.m4a'}, 'Frivillig': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_07.m4a'}, 'Alt er sex': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_08.m4a'}, 'Skj': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_09.m4a'}, 'Kor ska vi bo': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_10.m4a'}, 'Alt er sex II': {'produksjon': '1997_alt_er_sex', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_11.m4a'}, 'Tante på Tustna': {'produksjon': '1997_virak_i_vrakvika_barneteater_uka_-97', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_12.m4a'}, 'Tuba i nesen': {'produksjon': '1997_virak_i_vrakvika_barneteater_uka_-97', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_13.m4a'}, 'Storhavets pris': {'produksjon': '1997_virak_i_vrakvika_barneteater_uka_-97', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_14.m4a'}, 'Jeg er fri': {'produksjon': '1997_sa_det_svir_kjare_nabo_nattforestilling_uka_97', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1997_15.m4a'}, 'HKH Kronprinsen ankommer Storsalen': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_02.m4a'}, 'Åpning (,kåMMa,)': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_03.m4a'}, 'Ode til nyhetene': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_04.m4a'}, 'Skål!': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_05.m4a'}, 'Tusenårsbaby': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_06.m4a'}, 'Kicker på katter': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_07.m4a'}, 'Hvem er jeg?': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_08.m4a'}, 'Dansen': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_09.m4a'}, 'Girl I love you (studioversjon)': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_01.m4a'}, 'Girl I love you (liveversjon)': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_10.m4a'}, 'Trondheim, Trøndelag': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_11.m4a'}, 'Adolf Hitler parodierer Jan Eggum': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_12.m4a'}, 'Bare en drøm': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_13.m4a'}, 'Dama på Bunnpris': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_14.m4a'}, ',kåMMa,': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_15.m4a'}, 'Fly avsted': {'produksjon': '1999_kamma', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_16.m4a'}, 'Butlerballetten': {'produksjon': '1999_botlerballett_i_villa_violett_barneteater_uka_1999', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_17.m4a'}, 'Butlerboka/Oppskriften': {'produksjon': '1999_botlerballett_i_villa_violett_barneteater_uka_1999', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_18.m4a'}, 'Tango Maria': {'produksjon': '1999_botlerballett_i_villa_violett_barneteater_uka_1999', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_19.m4a'}, 'Samfundets Støtter': {'produksjon': '1999_botlerballett_i_villa_violett_barneteater_uka_1999', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/1999_20.m4a'}, 'Åpning (Paradoks)': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_02.m4a'}, 'Let the water flow': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_01.m4a'}, 'Bikini girls': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_03.m4a'}, 'Trine-Lises sang': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_04.m4a'}, 'Satans sang': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_05.m4a'}, 'Drikkevise': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_06.m4a'}, 'Dans og paljetter': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_07.m4a'}, 'Finale 1. akt': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_08.m4a'}, 'Designet liv': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_09.m4a'}, 'Trondheimsvise': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_10.m4a'}, 'Tenk hvis jeg var neger': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_11.m4a'}, 'Til ungdommen': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_12.m4a'}, 'Takk til alle': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_13.m4a'}, 'Finale 2. akt': {'produksjon': '2001_paradoks', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_14.m4a'}, 'Milles drømmesang': {'produksjon': '2001_kraftkarameller_og_kranglekompott_barneteater_uka_2001', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_15.m4a'}, 'Blanderegle': {'produksjon': '2001_kraftkarameller_og_kranglekompott_barneteater_uka_2001', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_16.m4a'}, 'Lea Loff og Dora Mirakles heltesang': {'produksjon': '2001_kraftkarameller_og_kranglekompott_barneteater_uka_2001', 'type': 'lyd', 'fil': 'http://sit-media.samfundet.no/media/lyd/2001_17.m4a'}, 'Kjærlighetsvise til byen': {'produksjon': '2003_glasur', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/lyd/2003_kjarlighetsvise_til_byen.flv'}, 'Jubileumsbokslepp, romantikk': {'produksjon': '', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/2010_bokslepp_romantikk.flv'}, 'Jubileumsbokslepp, utdeling av forfatterkatt': {'produksjon': '', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/2010_bokslepp_katt.flv'}, 'Naar vi døde vaagner - X': {'produksjon': '2015_supperevyen_-_naar_vi_dode_vaagner_-_x', 'type': 'video', 'fil': 'http://sit-media.samfundet.no/media/video/2015_supperevyen.flv'}}

# nummer_functions

# hendelse_transfer
def create_hendelse(location, filename):
    if filename[:6] == "SIT-19":
        try:
            aar = int(filename[4:])
            tittel = "Hendelser " + str(aar)
        except:
            aar = 1943
            tittel = "Hendelser 1940-45"
        mnd = 6
        dag = 15

    elif filename[:5] == "SIT-H":
        aar = int(filename[9:])
        mnd = 10
        dag = 15
        tittel = "Hendelser høst" + str(aar)
    elif filename[:5] == "SIT-V":
        aar = int(filename[8:])
        mnd = 3
        dag = 15
        tittel = "Hendelser " + str(aar)
    else:
        print("Lagde IKKE hendelse av " + filename)
        return

    file = open(location + filename + ".asp", 'r', encoding='cp1252')
    h = h2t.HTML2Text()
    h.convert_charrefs = True
    h.drop_white_space = 1
    tekst = file.read()
    beskrivelse = h.handle(tekst[tekst.find('<sidetekst'):]).replace('%>', '')
    file.close()
    shutil.move(location + filename + ".asp", location + 'hendelser/' + filename + ".asp")

    dato = datetime.date(aar, mnd, dag)
    new_hendelse = models.Hendelse.objects.create(tittel=tittel, beskrivelse=beskrivelse, dato=dato)
    new_hendelse.save()

    print("Laget hendelse " + tittel)


def transfer_all_hendelser(location):
    os.mkdir(location + 'hendelser')
    directory = os.fsencode(location)
    for file in os.listdir(directory):
        create_hendelse(location, os.fsdecode(file).replace(".asp", ""))


# nummer_transfer
def get_lydfil_dicts(url='http://skrift.no/sit/index.asp?vis=lyd',
                     location='/Users/jacob/OneDrive/Skrivebord/Fra_skrift/'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='lxml')
    # file = open("./soup.txt", 'w')
    # file.write(soup.prettify())
    # print(soup.prettify())
    nummere = soup.find_all('p')[8]
    # print(nummere.prettify())
    dict_of_lydfil_dicts = {}
    imgs = {}
    number_refs = {}
    prod_refs = {}
    files = {}

    lydfil_file = open(location + "lydfiler.asp", 'r', encoding='cp1252')
    lydfil_lines = lydfil_file.readlines()
    for i in range(len(lydfil_lines)):
        if lydfil_lines[i].find('mp3.flv') != -1:
            files[i] = lydfil_lines[i][lydfil_lines[i].find("http"):lydfil_lines[i].find(".mp3") + 4]
            url, fname = get_url_filename(
                lydfil_lines[i][lydfil_lines[i].find("http"):lydfil_lines[i].find(".flv") + 4])
            try:
                r = requests.get(url.replace("*", ""), allow_redirects=True, stream=True)
                shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/temp/flv_lydopptak/' + fname, 'wb'))
            except:
                url = url.replace("http://localhost/skrift.no", "").replace("//sit", "").replace("/sit", "")
                shutil.copyfileobj(open(location + url, 'rb'),
                                   open(settings.MEDIA_ROOT + '/temp/flv_lydopptak/' + fname, 'wb'))
        elif lydfil_lines[i].find('mp3') != -1:
            files[i] = lydfil_lines[i][lydfil_lines[i].find("http"):lydfil_lines[i].find(".mp3") + 4]
        elif lydfil_lines[i].find('.flv') != -1:
            files[i] = lydfil_lines[i][lydfil_lines[i].find("http"):lydfil_lines[i].find(".flv") + 4]
        elif lydfil_lines[i].find('m4a') != -1:
            files[i] = lydfil_lines[i][lydfil_lines[i].find("http"):lydfil_lines[i].find(".m4a") + 4]

    i = -1
    for tag in nummere.find_all():
        if tag.name == 'img':
            i += 1
            imgs[i] = tag['src']
        if tag.name == 'a':
            if tag['href'][:5] == "?lyd=":
                number_refs[i] = tag['href'][5:]
            elif tag['href'][:5] == "?prod":
                prod_refs[i] = tag['href'][12:]

    for j in range(len(imgs) - 1):
        number = number_refs[j]
        this_number_dict = {}

        l_or_v = ''
        if imgs[j] == 'img/video.jpg':
            l_or_v = 'video'
        elif imgs[j] == 'img/lyd.jpg':
            l_or_v = 'lyd'

        this_number_dict['produksjon'] = prod_refs.get(j, "")
        this_number_dict['type'] = l_or_v
        this_number_dict['fil'] = files[j]
        dict_of_lydfil_dicts[number] = this_number_dict

    return dict_of_lydfil_dicts


def create_nummer(nummer, nummer_dict, location, prod_for_opptak):
    tittel = nummer.replace(" (lyd)", "")
    try:
        # pdb.set_trace()
        file = open(location + tittel + ".asp", 'r', encoding='cp1252')
        h = h2t.HTML2Text()
        h.convert_charrefs = True
        h.drop_white_space = 1
        tekst = file.read()
        manus = h.handle(tekst[tekst.find('<sidetekst'):]).replace('%>', '')
        file.close()
        shutil.move(location + tittel + ".asp", location + 'numre/' + tittel + ".asp")
    except:
        manus = ""
    produksjon_input = nummer_dict['produksjon']

    if produksjon_input:
        try:
            produksjon = models.Produksjon.objects.get(premieredato__year=produksjon_input.split("_")[0],
                                                       tittel__icontains=" ".join(
                                                           produksjon_input.split("_")[1:]).replace(
                                                           'sa det svir kjare nabo nattforestilling uka 97',
                                                           'så det svir'))
        except:
            try:
                produksjon = models.Produksjon.objects.get(premieredato__year=produksjon_input.split("_")[0],
                                                           tittel__icontains="-".join(produksjon_input.split("_")[1:]))
            except:
                try:
                    produksjon = models.Produksjon.objects.get(premieredato__year=produksjon_input.split("_")[0],
                                                               tittel__icontains="E´De´Ber")
                except:
                    # pdb.set_trace()
                    produksjon = models.Produksjon.objects.get(premieredato__year=produksjon_input.split("_")[0],
                                                               tittel__icontains=produksjon_input.split("_")[1].replace(
                                                                   'nam', 'næm').replace('var', 'vær').replace('aja',
                                                                                                               'Åja').replace(
                                                                   'rod', 'rød').replace('rag', 'ræg').replace('uma',
                                                                                                               'umæ').replace(
                                                                   'kam', 'kåm').replace('botl', 'bøtl').replace('-a',
                                                                                                                 '-@'))
    else:
        produksjon = prod_for_opptak
    try:
        new_nummer = models.Nummer.objects.get(tittel=tittel)
    except:
        new_nummer = models.Nummer.objects.create(tittel=tittel, manus=manus, produksjon=produksjon)

    new_nummer.save()
    url, fname = get_url_filename(nummer_dict['fil'])
    url = url.replace('*', '')
    fname = fname.replace('*', '')

    try:
        r = requests.get(url.replace("*", ""), allow_redirects=True, stream=True)
        shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/opptak/' + fname, 'wb'))

    except:
        url = url.replace("http://localhost/skrift.no", "").replace("//sit", "").replace("/sit", "")
        shutil.copyfileobj(open(location + url, 'rb'),
                           open(settings.MEDIA_ROOT + '/opptak/' + fname, 'wb'))

    if url[-3:] == 'flv':
        # pdb.set_trace()
        inputfile = os.path.join(settings.MEDIA_ROOT, 'opptak', fname)
        outputfile = os.path.join(settings.MEDIA_ROOT, 'opptak', fname.replace('.flv', '.mp4'))
        subprocess.call(['ffmpeg', '-i', inputfile, outputfile])
        fname = fname.replace('.flv', '.mp4')

    fil = '/opptak/' + fname

    if nummer_dict['type'] == 'lyd':
        opptakstype = 2
    else:
        opptakstype = 1

    kontekst = "Opptak av nummeret " + new_nummer.tittel + " fra produksjonen " + produksjon.tittel

    new_opptak = models.Opptak.objects.create(fil=fil, nummer=new_nummer, opptakstype=opptakstype, kontekst=kontekst)
    new_opptak.save()
    print(new_nummer)


def get_manus_from_local_db():
    nummers_queryset = models.Nummer.objects.all()
    manus_dict = {}
    for nummer in nummers_queryset:
        manus_dict[nummer.tittel] = nummer.manus

    # file_path = location+"manus_dict.pkl"
    # pickle_file =open(file_path, 'wb')
    # pickle.dump(manus_dict)
    return manus_dict


def update_manus_in_live_db():
    nummers_queryset = models.Nummer.objects.all()
    # local_file = open(settings.MEDIA_ROOT + '/temp/manus_local_dict.txt', 'r', encoding="cp1252")
    # manus_local_dict = dict(local_file.read())
    for nummer in nummers_queryset:
        print(nummer.tittel)
        nummer.manus = local_manus_dict[nummer.tittel]
        nummer.save()


# div
def wipe_members():
    models.Medlem.objects.filter(opptaksar__lte=2019).delete()
    models.Medlem.objects.filter(opptaksar__isnull=True).delete()
    models.Foto.objects.all().delete()
    models.Arrangement.objects.all().delete()
    models.Lokale.objects.all().delete()


def replace_empty_tags(location, medlem=False):
    # pdb.set_trace()
    try:
        file = open(location, 'r', encoding='cp437')
        content = file.read().replace(";¥", "")
        file.close()
        w_file = open(location, 'w', encoding='cp437')
        w_file.write(content)
        w_file.close()
    except:
        pass

    file = open(location, 'r', encoding='cp1252')

    lines = file.readlines()
    i = 0
    while i < len(lines):
        if medlem:
            b = lines[i].find("><")
        else:
            b = lines[i].find("></karakter")
        if b != -1:
            print(lines[i])
            lines.pop(i)
        else:
            i += 1

    a_file = open(location, "w", encoding='cp1252')
    a_file.writelines(lines)
    a_file.close()


# data collection
def getMedlemDict(location):
    soup = BeautifulSoup(open(location, encoding='cp1252'), features="lxml")
    # print(soup.prettify())
    h = h2t.HTML2Text()
    h.convert_charrefs = True
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
        if open(location, 'r', encoding='cp1252').readlines().index('%>') < 5:
            return data_dict
        replace_empty_tags(location, medlem=True)
        return getMedlemDict(location)

    try:
        navn = data_dict['fornamn']
    except:
        f = open(location, encoding='cp1252')
        tekst = f.read()
        data_dict['fornamn'] = h.handle(tekst[tekst.find('fornamn') + 8:tekst.find('</fornamn')]).replace("\n", "")

        if data_dict['fornamn'] == '':
            if location.count("_") > 1:
                fornavn = location[(location.find("_") + 1):location.find("_", location.find("_") + 1)]
            else:
                fornavn = location[(location.find("_") + 1):-4]

            for i in range(len(fornavn)):
                if fornavn[i] == 'ø':
                    fornavn[i] = 'å'
                elif fornavn[i] == 'å':
                    fornavn[i] = 'ø'

            data_dict['fornamn'] = fornavn.title()

    # print(data_dict)
    return data_dict


def getForestillingDict(location):
    soup = BeautifulSoup(open(location, encoding='cp1252'), features="lxml")
    h = h2t.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.convert_charrefs = True

    # print(soup.prettify())
    data_dict = {}
    for tag in soup.find_all():
        try:
            tag_name = tag.name
            if tag_name == 'sidetekst':

                tag_str = ""
                link_dict = {}
                for atag in tag.find_all('a', href=True):
                    link_dict[atag.string] = "[" + atag['href'] + "]"

                for sidetekst_tag in tag.find_all(text=True):
                    tag_str += sidetekst_tag.string + " "
                    tag_str += link_dict.get(sidetekst_tag.string, "")
                # tag_str = h.handle(str(tag)).replace("  \n","").replace("\n", " ").replace("  ", " f")
                # test = " ".join(tag.find_all(text=True))
                images = []
                for imgtag in tag.find_all('img'):
                    images.append(imgtag['src'])
                data_dict['images'] = images
                tag_str = tag_str.replace("  ", " ").replace("\xa0", "").replace("**", "")
            else:
                tag_str = tag.string
            data_dict[tag_name] = tag_str
        except:
            continue
    f = open(location, encoding='cp1252')
    tekst = f.read()
    data_dict['produksjonsnamn'] = h.handle(
        tekst[tekst.find('produksjonsnamn') + 16:tekst.find('</produksjonsnamn')]).replace("\n", "").replace('\.', "")

    if data_dict['produksjonsnamn'] == "" or tekst.find('produksjonsnamn') == -1:
        try:
            data_dict['produksjonsnamn'] = data_dict['overskrift']
        except:
            data_dict['produksjonsnamn'] = h.handle(
                tekst[tekst.find('overskrift') + 11:tekst.find('</overskrift')]).replace("\n", "").replace('\.', "")

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
            elif type == 'arsverv':
                list_of_dicts.append(get_arverv_dict(filename))
        except:
            replace_empty_tags(filename)
            try:
                if type == 'forestilling':
                    list_of_dicts.append(getForestillingDict(filename))
                elif type == 'medlem':
                    list_of_dicts.append(getMedlemDict(filename))
                elif type == 'arsverv':
                    list_of_dicts.append(get_arverv_dict(filename))
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
        try:
            dict_of_sets[key] = set(value)
            # print(key, len(dict_of_sets[key]))
            # print(dict_of_sets[key])
        except:
            pass

    return list_of_dicts, dict_of_lists, dict_of_sets, errors


def get_arverv_dict(location):
    soup = BeautifulSoup(open(location, encoding='cp1252'), features="lxml")
    # print(soup.prettify())
    h = h2t.HTML2Text()
    h.convert_charrefs = True
    data_dict = {}
    for tag in soup.find_all():
        try:
            tag_name = tag.name
            tag_str = tag.string
            data_dict[tag_name] = tag_str
        except:
            continue
    try:
        v = data_dict['verv_0']
    except:
        f = open(location, encoding='cp1252')
        tekst = f.read()
        data_dict['verv_0'] = h.handle(tekst[tekst.find('verv_0') + 7:tekst.find('</verv_0')]).replace("\n",
                                                                                                       "").replace('\.',
                                                                                                                   "")
    try:
        v = data_dict['person_0']
    except:
        f = open(location, encoding='cp1252')
        tekst = f.read()
        data_dict['person_0'] = h.handle(tekst[tekst.find('person_0') + 9:tekst.find('</person_0')]).replace("\n",
                                                                                                             "").replace(
            '\.', "")

    data_dict['ar'] = location.split("/")[-1].replace(".asp", "")

    return data_dict


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


# medlemsfunksjoner
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
    gjeng_medlemstype_dict = {'skuespiller': 1, 'Regi': 2, 'Kostyme': 1, 'Ekstern': 21, 'UKE-funk': 9,
                              'UKEfunk/Låftet': 5,
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
                kontekst = medlem_dict[key.replace('_', 'txt_')]
            except:
                kontekst = ""
            url = value.replace("""\\""", "/")

            if medlem_dict.get(key.replace('galleri_', 'galleriFG_'), ""):
                FG = medlem_dict.get(key.replace('galleri_', 'galleriFG_'), "")
            elif medlem_dict.get(key.replace('galleri_', 'gallerifg_'), ""):
                FG = medlem_dict.get(key.replace('galleri_', 'gallerifg_'), "")
            else:
                FG = ""

            if FG in {"ja", "Ja"}:
                fotograf = 'Fotogjengen'
            else:
                fotograf = ""

            if url.split("/")[-2] in {"TG-bilder", "bilder"}:
                fname = url.split("/")[-1]
            else:
                fname = "_".join(url.split("/")[-2:])
            try:
                old_foto = models.Foto.objects.get(fil='/bilder/' + fname, kontekst=kontekst)
                old_foto.medlemmer.add(new_medlem)
                old_foto.save()
            except:
                try:
                    r = requests.get(url, allow_redirects=True, stream=True)
                    shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                except:
                    shutil.copyfileobj(open(location + url, 'rb'),
                                       open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))

                fil = '/bilder/' + fname
                try:
                    if medlem_dict[key.replace("_", "fg_")] == "ja":
                        kontekst += "(foto.samfundet.no)"
                except:
                    pass
                new_foto = models.Foto(fil=fil, kontekst=kontekst, arrangement=arr, fototype=1, fotograf=fotograf)
                new_foto.save()
                new_foto.medlemmer.add(new_medlem)
                new_foto.save()


# produksjonsfunksjoner
def create_produksjon(data_dict, location):
    # 'p'- div tekst, sjekk om det er i sidetekst et sted --> beskrivelse
    # 'semester' - semester, --> premieredato
    # 'aar'- år satt opp, --> premieredato
    # 'overskrift' - overskrift på siden, vanligvis det samme som produksjonsnavnet --> beskrivelse?
    # 'sidetekst' - mesteparten av innholdet på siden, -->beskrivelse
    # 'a'- sjekk om det er i sidetekst, -->beskrivelse
    # 'b' - sjekk om det er i sidetekst, -->beskrivelse
    # 'skildring' - kort beskrivelse av forestillingen, -->beskrivelse
    # 'spelestad' - spillested, mye forskjellig her --> create lokale og link til forestillingen
    # 'opphavsmenn' - forfatter(e), replace "av " --> forfatter
    # 'uka' - ukeproduksjon? ja hvis tagen fins --> produksjonstype = 4
    # 'plakat' - plakat(bildelink) --> plakat
    # 'galleri_i' og 'galleritxt_i' --> lag Foto og link til produksjonen
    # 'verv_i', 'person_i' + 'karakter_i' --> lag erfaring knyttet til medlem og produksjon, lag medlem om medlem ikke finnes, bruk dict for å få riktige verv
    # 'produksjonstype' lag produksjonstags, kjør gjennom filter, inneholder også AFEI og KUP --> produksjonstype, enkelte kan kanskje gå som skildring også
    # 'produksjonsnamn' - kommer ikke med, men det er egentlig her tittel ligger -->tittel

    tittel = try_get2('produksjonsnamn', data_dict, "Ikke funnet")
    forfatter = try_get2('opphavsmenn', data_dict, "").replace("av ", "")

    aar = int(data_dict.get('aar', 1985))
    try:
        if data_dict['semester'] in {'Hosø', 'Hørt', 'høst', 'Høst'}:
            premieredato = datetime.date(aar, 12, 24)
        else:
            premieredato = datetime.date(aar, 1, 1)
    except:
        premieredato = datetime.date(aar, 7, 1)

    produksjonstype = 0
    produksjonstag_list = []
    lokale_list = []

    beskrivelse = ""
    beskrivelse += try_get('overskrift', data_dict)

    try:
        produksjonstype_is_skildring, produksjonstype, produksjonstag_list = create_produksjonstags(
            produksjonstype_dict[data_dict['produksjonstype']])
        if produksjonstype_is_skildring:
            beskrivelse += try_get('produksjonstype', data_dict)
    except:
        pass

    try:
        lokale_is_skildring, lokale_list = create_lokale(lokale_dict[data_dict['spelestad']])
        if lokale_is_skildring:
            beskrivelse += try_get('spelestad', data_dict)
    except:
        pass

    try:
        a = data_dict['uka']
        produksjonstype = 4
    except:
        if produksjonstype == 0:
            produksjonstype = 1

    beskrivelse += try_get('skildring', data_dict)

    beskrivelse += data_dict.get("sidetekst", "")

    beskrivelse += check_sidetekst('p', data_dict)

    beskrivelse += check_sidetekst('a', data_dict)

    beskrivelse += check_sidetekst('b', data_dict)

    try:
        if data_dict['produksjonstype'] == 'UKE-revy' and forfatter == "":
            forfatter = "Forfatterkollegiet"
    except:
        pass

    plakat = None
    try:
        url, fname = get_url_filename(data_dict['plakat'])
        r = requests.get(url, allow_redirects=True, stream=True)
        fname = url.split("/")[-1]
        if r.status_code == 200:
            shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/plakater/' + fname, 'wb'))
            plakat = '/plakater/' + fname
    except:
        pass

    new_produksjon = models.Produksjon(tittel=tittel, forfatter=forfatter, premieredato=premieredato, plakat=plakat,
                                       beskrivelse=beskrivelse, produksjonstype=produksjonstype)
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
        return ""


def check_sidetekst(data, data_dict, data_check='sidetekst'):
    try:
        if data_dict[data_check].find(data_dict[data]) == -1:
            return data + ":    " + data_dict[data] + "\n\n"
        else:
            return ""
    except:
        return ""


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
        elif tag != 'nei':
            try:
                produksjonstag = models.Produksjonstag.objects.get(tag=tag)
            except:
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
            try:
                lok = models.Lokale.objects.get(navn=tag)
            except:
                lok = models.Lokale(navn=tag)
                lok.save()
            lokale_list.append(lok)
    return is_skildring, lokale_list


# produksjonsbilder
def update_old_produksjon_foto(fname, new_produksjon):
    old_foto = models.Foto.objects.get(fil='/bilder/' + fname)
    old_foto.arrangement = None
    old_foto.produksjon = new_produksjon
    old_foto.save()


def create_new_produksjon_foto(fname, new_produksjon, url, kontekst, location, fotograf):
    try:
        r = requests.get(url, allow_redirects=True, stream=True)
        shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
    except:
        url = url.replace("http://localhost/skrift.no", "").replace("//sit", "").replace("/sit", "")
        shutil.copyfileobj(open(location + url, 'rb'),
                           open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
    fil = '/bilder/' + fname

    new_foto = models.Foto(fil=fil, kontekst=kontekst, produksjon=new_produksjon, fototype=1, fotograf=fotograf)
    new_foto.save()


def get_url_filename(value):
    url = value.replace("\\", "/").replace("1929_cassa_rossa-visehefte", "1929_cassa-rossa-visehefte")

    if url.split("/")[-2] in {"TG-bilder", "bilder"}:
        fname = url.split("/")[-1]
    else:
        fname = "_".join(url.split("/")[-2:])
    return url, fname


def update_produksjon_gallery(produksjon_dict, new_produksjon, location):
    banner = '/default/katter.png'
    for key, value in produksjon_dict.items():
        if key[:8] == 'galleri_':
            try:
                kontekst = produksjon_dict[key.replace('_', 'txt_')]
            except:
                kontekst = ""

            if produksjon_dict.get(key.replace('galleri_', 'galleriFG_'), ""):
                FG = produksjon_dict.get(key.replace('galleri_', 'galleriFG_'), "")
            elif produksjon_dict.get(key.replace('galleri_', 'gallerifg_'), ""):
                FG = produksjon_dict.get(key.replace('galleri_', 'gallerifg_'), "")
            else:
                FG = ""

            if FG in {"ja", "Ja"}:
                fotograf = 'Fotogjengen'
            else:
                fotograf = ""

            url, fname = get_url_filename(value)
            # medlemmer[]
            # try:
            #     person_list = produksjon_dict[key.replace("galleri", "persongalleri"].split(",")
            #     for person in person_list:
            #         fornavn = person[:person.find(" ")]
            try:
                update_old_produksjon_foto(fname, new_produksjon)

            except:

                create_new_produksjon_foto(fname, new_produksjon, url, kontekst, location, fotograf)

            if key[-1] == '0' and open(settings.MEDIA_ROOT + '/bilder/' + fname, 'rb'):
                shutil.copyfileobj(open(settings.MEDIA_ROOT + '/bilder/' + fname, 'rb'),
                                   open(settings.MEDIA_ROOT + '/bannere/' + fname, 'wb'))
                banner = '/bannere/' + fname

    for img in produksjon_dict.get('images', []):
        if img == "" or img[:20] == "file:///Users/afsso/":
            continue
        url, fname = get_url_filename(img)
        try:
            update_old_produksjon_foto(fname, new_produksjon)
        except:
            create_new_produksjon_foto(fname, new_produksjon, url, "", location, "")

        if banner == '/default/katter.png':
            shutil.copyfileobj(open(settings.MEDIA_ROOT + '/bilder/' + fname, 'rb'),
                               open(settings.MEDIA_ROOT + '/bannere/' + fname, 'wb'))
            banner = '/bannere/' + fname

    return banner


# lage erfaringer & verv
def create_erfaringer(data_dict, produksjon=False, verv_dict=verv_dict1, arsverv=False):
    for key, value in data_dict.items():
        if key[:7] == 'person_':
            navn = value
            navn_lst = navn.split(" ")
            fornavn = navn_lst[0]
            etternavn = navn_lst[-1]
            # mellomnavn = ' '.join([str(elem) for elem in navn_lst[1:-1]])
            verv_input = data_dict[key.replace('person_', 'verv_')]
            verv_name = verv_dict[verv_input][0]
            # ar = data_dict['aar']
            try:
                medlem = models.Medlem.objects.get(fornavn=fornavn, etternavn=etternavn)
            except:
                try:
                    medlem = models.Medlem.objects.get(fornavn=fornavn + " " + navn_lst[1], etternavn=etternavn)
                except:
                    medlem = False
            if arsverv:
                create_arsverv_erfaring(verv_name, key, data_dict, verv_input, navn, medlem)
            else:
                create_erfaring(verv_name, key, data_dict, produksjon, verv_input, navn, medlem)


def create_erfaring(verv_name, key, data_dict, produksjon, verv_input, navn, medlem, verv_dict=verv_dict1):
    rolle = verv_dict[verv_input][1]
    if rolle == "LYD":
        U = True
        for ptag in produksjon.produksjonstags.all():
            if ptag.tag == 'UKErevy':
                U = False
        if U:
            rolle = 'ingen'
    if rolle == 'ingen':
        try:
            rolle = data_dict[key.replace('person', 'karakter')]
            if rolle == None:
                rolle = ""
        except:
            rolle = ""
    else:
        try:
            rolle += ", " + data_dict[key.replace('person', 'karakter')]
        except:
            pass

    if verv_name == "tittel":
        if medlem:
            erfaring = models.Erfaring(medlem=medlem,
                                       tittel=verv_input, produksjon=produksjon, rolle=rolle)
        else:
            erfaring = models.Erfaring(navn=navn, tittel=verv_input,
                                       produksjon=produksjon, rolle=rolle)
        erfaring.save()
    else:
        typ = verv_dict[verv_input][2]
        verv_lst = verv_name.split("/")
        for i in range(len(verv_lst)):
            verv = update_verv(verv_lst[i], typ)
            if i == 0:
                if verv_lst[i].lower() != verv_input.split("/")[i].lower():
                    update_uttrykk(verv_input.split("/")[i], verv_lst[i], rolle)
            if medlem:
                erfaring = models.Erfaring(medlem=medlem, rolle=rolle, produksjon=produksjon)
            else:
                erfaring = models.Erfaring(navn=navn, rolle=rolle, produksjon=produksjon)
            erfaring.save()
            erfaring.verv = verv
            erfaring.save()


def create_arsverv_erfaring(verv_name, key, data_dict, verv_input, navn, medlem, verv_dict=arsverv_dict):
    rolle = verv_dict[verv_input][1]
    periode = data_dict.get(key.replace('person', 'periode'), "")
    if periode in {'hele', 'Hele'}:
        periode = ""
    if periode == None:
        periode = ""
    if rolle == 'ingen':
        rolle = periode
    elif periode:
        rolle += ", " + periode

    typ = verv_dict[verv_input][2]
    styre = data_dict.get(key.replace('person', 'styre'), "")
    if styre in {"ja", "Ja"}:
        typ = 'styre'
    elif styre in {'nei', 'Nei'} and typ == 'styre':
        typ = 'intern-gjeng'

    if verv_name in {"tittel", "Tittel"} and typ != 'styre':
        if medlem:
            erfaring = models.Erfaring(medlem=medlem,
                                       tittel=verv_input, ar=data_dict['ar'], rolle=rolle)
        else:
            erfaring = models.Erfaring(navn=navn, tittel=verv_input,
                                       ar=data_dict['ar'], rolle=rolle)
        erfaring.save()

    else:
        if verv_name in {"tittel", "Tittel"}:
            verv_name = verv_input
        verv_lst = verv_name.split("/")
        for i in range(len(verv_lst)):
            verv = update_verv(verv_lst[i], typ)
            if i == 0:
                if verv_lst[i].lower() != verv_input.split("/")[i].lower():
                    update_uttrykk(verv_input.split("/")[i], verv_lst[i], rolle)
            if medlem:
                erfaring = models.Erfaring(medlem=medlem, rolle=rolle, ar=data_dict['ar'])
            else:
                erfaring = models.Erfaring(navn=navn, rolle=rolle, ar=data_dict['ar'])
            erfaring.save()
            erfaring.verv = verv
            erfaring.save()


def update_uttrykk(verv_input, verv_cleaned, rolle):
    try:
        uttrykk = models.Uttrykk.objects.get(tittel=verv_input)
    except:
        beskrivelse = "En annen betegnelse på [[" + verv_cleaned + "]]"
        if rolle:
            beskrivelse += " med rolle som " + rolle
        uttrykk = models.Uttrykk(tittel=verv_input, beskrivelse=beskrivelse)
        uttrykk.save()


def update_verv(tittel, type, prod=True):
    if type in {'styre', 'ekstern-gjeng', 'intern-gjeng'}:
        vtype_dict = {'styre': 1, 'ekstern-gjeng': 2, 'intern-gjeng': 3}
        vtype = vtype_dict[type]
    else:
        vtype = 4
    try:
        return models.Verv.objects.get(tittel=tittel, vervtype=vtype)
    except:
        if type == 'prodapp':
            vervtag = update_vervtag('produksjonsapparat')
            new_verv = models.Verv.objects.create(tittel=tittel, erfaringsoverforing=True, vervtype=vtype)
            new_verv.save()
            new_verv.vervtags.add(vervtag)
            new_verv.save()
            return new_verv
        elif type == 'styre':
            new_verv = models.Verv.objects.create(tittel=tittel, erfaringsoverforing=True, vervtype=vtype)
            new_verv.save()
            return new_verv
        else:
            new_verv = models.Verv.objects.create(tittel=tittel, vervtype=vtype, erfaringsoverforing=False)
            new_verv.save()
            return new_verv


def update_vervtag(tittel):
    try:
        return models.Vervtag.objects.get(tag=tittel)
    except:
        vervtag = models.Vervtag.objects.create(tag=tittel)
        vervtag.save()
        return vervtag


# arsverv


# main functions
def transfer_all_medlemmer(location):
    try:
        os.mkdir(settings.MEDIA_ROOT + '/bilder')
        os.mkdir(settings.MEDIA_ROOT + '/portretter')
    except:
        pass
    wipe_members()
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


def transfer_all_arsverv(location):
    list_of_dicts, dict_of_lists, dict_of_sets, errors = getAll(location + 'verv/', 'arsverv')
    print("Errors: ", errors)

    for dict in list_of_dicts:
        create_erfaringer(dict, verv_dict=arsverv_dict, arsverv=True)
        print(dict['ar'])

    print("Errors: ", errors)


def transfer_all_numre():
    try:
        os.mkdir(settings.MEDIA_ROOT + '/temp')
        os.mkdir(settings.MEDIA_ROOT + '/temp/flv_lydopptak')
        os.mkdir(location + 'numre')
        os.mkdir(settings.MEDIA_ROOT + '/opptak')
    except:
        pass

    dict_of_lydfil_dicts = get_lydfil_dicts(location=location)
    # for line in lydfil_file.readlines():
    prod = models.Produksjon.objects.create(tittel="Opptak fra skrift", premieredato=datetime.date(2020, 12, 31))
    prod.save()

    for nummer, nummer_dict in dict_of_lydfil_dicts.items():
        create_nummer(nummer, nummer_dict, location, prod)

def get_nummer_pictures():
     # pdb.set_trace()
    all_numre = models.Nummer.objects.all()
    for nummer in all_numre:
        if nummer.manus.find("]") != -1:
            # print(nummer.manus)
            manus = nummer.manus
            # print(manus.find("]"))
            skrift_url = manus[manus.find("]")+2:manus.find(")", manus.find("]"))]
            print(skrift_url)
        

def img_pictures(skrift_path):
    for file in os.listdir(skrift_path+"img/"):
        if file not in os.listdir(settings.MEDIA_ROOT + '/bilder/'):
            shutil.copyfileobj(open(file, 'rb'), open(settings.MEDIA_ROOT + '/bilder/' + file, 'wb'))
            fil = '/bilder/' + file
            new_foto = models.Foto(fil=fil, kontekst=file, produksjon=new_produksjon, fototype=1, fotograf=fotograf)
            new_foto.save()
            
def fixtext(s):
    if s[0].isupper() and s[1:].islower():
        return s.lower()
    else:
        return s


if __name__ == "__main__":
    # FYLL INN DIN LOKALE FILSTI TIL SKRIFTDATA HER:
    Skriftdata_path = '/Users/jacob/Downloads/sit skrift/sit/'
    # transfer_all_medlemmer(Skriftdata_path)
    # transfer_all_produksjoner(Skriftdata_path)
    # transfer_all_arsverv(Skriftdata_path)
    # transfer_all_numre(Skriftdata_path)
    # update_manus_in_live_db()
    # print(get_manus_from_local_db())
    # transfer_all_hendelser(Skriftdata_path)
    get_nummer_pictures()
