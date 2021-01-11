
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

from SITdata import models, forms


from django.conf import settings
from bs4 import BeautifulSoup
import os
import pdb
import datetime
import requests
import shutil

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
    soup = BeautifulSoup(open(location), features="lxml")
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

    print(data_dict)
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
    print(list_of_dicts)
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

    telefon = try_get2('mobil', medlem_dict, '')
    kallenavn = try_get2('tidligare_namn', medlem_dict, '')

    epost = ''
    try:
        epost = medlem_dict['e_post'].replace(" (a) ", "@")
        epost.replace("(a)", "@")
        epost.replace("(a)", "@")
    except:
        pass

    mtype = 1
    undergjeng = None
    gjeng_mtype_dict = {'skuespiller': 1, 'Regi': 2, 'Kostyme': 1, 'Ekstern': 21, 'UKE-funk': 9, 'UKEfunk/Låftet': 5,
                        'Kulisse': 1, 'Skuespiller': 1}
    gjeng_undergjeng_dict = {'skuespiller': 3, 'Kostyme': 1, 'Kulisse': 2, 'Skuespiller': 3}
    try:
        mtype = gjeng_mtype_dict[medlem_dict['gjeng']]
        if mtype == 1:
            undergjeng = gjeng_undergjeng_dict[medlem_dict['gjeng']]
    except:
        pass

    status = None
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
            shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT+'/portretter/'+fname, 'wb'))
            portrett = '/portretter/'+fname
    except:
        pass

    new_medlem = models.Medlem(mtype=mtype, fornavn=fornavn, mellomnavn=mellomnavn, etternavn=etternavn,
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
        f_år = medlem_dict['fodt_aar']
        if len(f_år) < 4:
            f_år = '19' + f_år

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

        return datetime.date(int(f_år), int(f_mnd), int(f_dto))
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
    print(medlem_dict)
    for key, value in medlem_dict.items():
        if key[:10] == 'galleritxt':
            try:
                url = medlem_dict[key.replace('txt', '')]
                fname = url.split("/")[-1]

                old_foto = models.Foto.objects.get(fil='/bilder/'+fname, kontekst=value)
                old_foto.medlemmer.add(new_medlem)
            except:
                url = medlem_dict[key.replace('txt', '')].replace("\\","/")
                fname = url.split("/")[-1]
                try:
                    r = requests.get(url, allow_redirects=True, stream=True)
                    shutil.copyfileobj(r.raw, open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                except:
                    shutil.copyfileobj(open(location+medlem_dict[key.replace('txt', '')],'rb'), open(settings.MEDIA_ROOT + '/bilder/' + fname, 'wb'))
                fil = '/bilder/' + fname
                new_foto = models.Foto(fil=fil, kontekst=value, arrangement=arr, ftype=1)
                new_foto.save()
                new_foto.medlemmer.add(new_medlem)
                new_foto.save()


def get_forestilling(data_dict):
    # ['p', 'semester', 'aar', 'overskrift', 'sidetekst', 'span', 'br', 'a', 'skildring', 'spelestad',
    # 'img', 'font', 'opphavsmenn', 'uka', 'strong', 'div', 'h1', 'o:p', 'i', 'em', 'u', 'td', 'b', 'link']

    ptype = 1

    try:
        if data_dict['uka'] == 'Ja':
            ptype = 4
    except:
        pass

    info = ""
    info += try_get('p', data_dict)
    info += "\n\n"
    info += try_get('sidetekst', data_dict)
    info += "\n\n"
    info += try_get('span', data_dict)
    info += "\n\n"
    info += try_get('br', data_dict)
    info += "\n\n"
    info += try_get('skildring', data_dict)
    info += "\n\n"
    info += try_get('a', data_dict)
    info += "\n\n"
    info += try_get('strong', data_dict)
    info += "\n\n"
    info += try_get('div', data_dict)
    info += "\n\n"
    info += try_get('o:p', data_dict)
    info += "\n\n"
    info += try_get('i', data_dict)
    info += "\n\n"
    info += try_get('em', data_dict)
    info += "\n\n"
    info += try_get('u', data_dict)
    info += "\n\n"
    info += try_get('td', data_dict)
    info += "\n\n"
    info += try_get('link', data_dict)
    info += "\n\n"
    info += try_get('produksjonstype', data_dict)

    tittel = try_get2('overskrift', data_dict, "Ikke funnet")

    forfatter = try_get2('opphavsmenn', data_dict, "Ikke funnet")

    revy = False

    try:
        if data_dict['produksjonstype'] == 'UKE-revy':
            revy = True
            forfatter = "Forfatterkollegiet"
    except:
        pass

    lokale = try_get2('spelestad', data_dict, "Ikke spesifisert")

    if data_dict['semester'] in {'Hosø', 'Hørt', 'høst', 'Høst'}:
        premieredato = datetime.date(data_dict['aar'], 10, 15)
    else:
        premieredato = datetime.date(data_dict['aar'], 3, 15)

    for key, value in data_dict:
        if key[:4] == 'verv':
            num = key[5:]
            navn_lst = data_dict['person_' + num].split(" ")
            fornavn = navn_lst[0]
            etternavn = navn_lst[-1]
            mellomnavn = ' '.join([str(elem) for elem in navn_lst[1:-1]])

            verv = value  # TODO
            ar = data_dict['aar']
            try:
                rolle = data_dict['karakter_' + num]
            except:
                rolle = None

            erfaring = models.Erfaring(
                medlem=models.Medlem.objects.get(fornavn=fornavn, etternavn=etternavn, mellomnavn=mellomnavn),
                verv=verv, ar=ar, rolle=rolle)
            erfaring.save()


def try_get2(data, data_dict, default=None):
    try:
        return data_dict[data]
    except:
        return default


def try_get(data, data_dict):
    try:
        return data + ":    " + data_dict[data]
    except:
        return data + ":    "


def transfer_all_medlemmer(location):
    try:
        os.mkdir('/Users/jacob/sit-web/SITnett/files/bilder')
        os.mkdir('/Users/jacob/sit-web/SITnett/files/portretter')
    except:
        pass
    list_of_dicts, dict_of_lists, dict_of_sets, errors = getAll(location+'medlem/')
    skrift = models.Lokale(navn='skrift.no')
    skrift.save()
    arr_for_pictures = models.Arrangement(atype=1, tittel='Bilder fra skrift knyttet til medlemmer',
                                          tidspunkt=datetime.date(2020, 12, 31), lokale=skrift)
    arr_for_pictures.save()

    for dict in list_of_dicts:
        create_medlem(dict, arr_for_pictures, location)

    print("Errors: ", errors)
