from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

from SITdata import models, forms

from bs4 import BeautifulSoup
import os
import pdb
import datetime


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
        navn = data_dict['fornamn']
    except:
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
    pdb.set_trace()

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


def create_medlem(medlem_dict, arr_for_bilder):
    fornavn = try_get2('fornamn', medlem_dict, '')
    mellomnavn = try_get2('mellomnamn', medlem_dict, '')
    etternavn = try_get2('etternamn', medlem_dict, '')
    studium = try_get2('studerer', medlem_dict, '')

    fodselsdato = None
    try:
        fodselsdato = hent_fodsel(medlem_dict)
    except:
        pass

    opptaksar = try_get2('opptak_aar', medlem_dict)

    # ['fodt_dto', 'fodt_mnd', 'fodt_aar', 'gjeng', 'status', 'opptak_aar', 'e_post', 'mobil', 'foto', 'dgk_ridder']

    telefon = try_get2('mobil', medlem_dict, '')
    kallenavn = try_get2('tidligare_namn', medlem_dict, '')

    epost = ''
    try:
        epost = medlem_dict['e_post'].replace(" (a) ", "@")
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
    except:
        pass

    portrett = '/default/katt.png'
    try:
        if os.path.isfile(medlem_dict['foto']):
            portrett = medlem_dict['foto']
    except:
        pass

    new_medlem = models.Medlem(mtype=mtype, fornavn=fornavn, mellomnavn=mellomnavn, etternavn=etternavn,
                               fodselsdato=fodselsdato,
                               opptaksar=opptaksar, undergjeng=undergjeng, status=status, portrett=portrett,
                               telefon=telefon,
                               epost=epost, studium=studium, kallenavn=kallenavn)
    new_medlem.save()

    create_utmerkelser(medlem_dict, new_medlem)

    update_gallery(medlem_dict, new_medlem, arr_for_bilder)

    print(new_medlem)


def hent_fodsel(medlem_dict):
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
    return datetime.date(f_år, f_mnd, f_dto)


def create_utmerkelser(medlem_dict, new_medlem):
    try:
        ridder_ar = medlem_dict['dgk_ridder']
        utmerkelser = [models.Utmerkelse(utype=1, orden=1, ar=ridder_ar, medlem=new_medlem)]
        try:
            kommandor_ar = medlem_dict['dgk_kommandor']
            utmerkelser.append(models.Utmerkelse(utype=1, orden=1, ar=kommandor_ar, medlem=new_medlem))
            try:
                storkors_ar = medlem_dict['dgk_storkors']
                utmerkelser.append(models.Utmerkelse(utype=1, orden=1, ar=storkors_ar, medlem=new_medlem))
            except:
                pass
        except:
            pass
        for utmerkelse in utmerkelser:
            utmerkelse.save()
    except:
        pass


def update_gallery(medlem_dict, new_medlem, arr):
    print(medlem_dict)
    for key, value in medlem_dict.items():
        if key[:10] == 'galleritxt':
            try:
                old_foto = models.Foto.objects.get(fil=medlem_dict[key.replace('txt', '')], )
                old_foto.medlemmer.add(new_medlem)
            except:
                new_foto = models.Foto(fil=medlem_dict[key.replace('txt', '')], kontekst=value, arrangement=arr, ftype=1)
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


def transfer_all_medlemmer(location):
    list_of_dicts, dict_of_lists, dict_of_sets, errors = getAll(location)
    skrift = models.Lokale(navn='skrift.no')
    skrift.save()
    arr_for_pictures = models.Arrangement(atype=1, tittel='Bilder fra skrift knyttet til medlemmer',
                                          tidspunkt=datetime.date(2020, 12, 31), lokale=skrift)
    arr_for_pictures.save()

    for dict in list_of_dicts:
        create_medlem(dict, arr_for_pictures)


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


def view_hoved(request):
    transfer_all_medlemmer("/Users/jacob/Desktop/Fra skrift/medlem/")
    return render(request, 'hoved.html')


def view_info(request):
    return render(request, 'info.html')


def view_opptak(request):
    return render(request, 'opptak.html')


def view_kontakt(request):
    return render(request, 'kontakt.html')


def view_medlemmer(request):
    return render(request, 'medlemmer/medlemmer.html', {'mliste': models.Medlem.objects.all()})


@permission_required('SITdata.add_medlem')
def view_medlem_ny(request):
    if request.method == 'POST':
        mform = forms.MedlemAdminForm(request.POST, request.FILES)
        if mform.is_valid():
            medlem = mform.save()
            if 'opprett_brukerkonto' in request.POST:
                brukerkonto = User.objects.create_user(medlem.brukernavn(), medlem.epost, 'ta-de-du!')
                medlem.brukerkonto = brukerkonto
                medlem.save()
            return redirect('medlem_info', medlem.id)
    else:
        mform = forms.MedlemAdminForm()
    return render(request, 'medlemmer/medlem_ny.html', {'mform': mform})


def view_medlem_info(request, mid):
    medlem = get_object_or_404(models.Medlem, id=mid)
    if request.user.has_perm('SITdata.change_medlem'):
        access = 'admin'
    elif request.user == medlem.brukerkonto:
        access = 'own'
    else:
        access = 'other'
    return render(request, 'medlemmer/medlem_info.html', {'access': access, 'medlem': medlem})


@login_required
def view_medlem_redi(request, mid):
    medlem = get_object_or_404(models.Medlem, id=mid)
    if request.user.has_perm('SITdata.change_medlem'):
        MedlemForm = forms.MedlemAdminForm
    elif request.user == medlem.brukerkonto:
        MedlemForm = forms.MedlemOwnForm
    else:
        MedlemForm = forms.MedlemOtherForm
    if request.method == 'POST':
        mform = MedlemForm(request.POST, instance=medlem)
        eform = forms.ErfaringMedForm(request.POST, request.FILES)
        uform = forms.UtmerkelseForm(request.POST)
        if mform.is_valid():
            mform.save()
            if 'opprett_brukerkonto' in request.POST:
                brukerkonto = User.objects.create_user(medlem.brukernavn(), medlem.epost, 'ta-de-du!')
                medlem.brukerkonto = brukerkonto
                medlem.save()
            elif 'fjern_brukerkonto' in request.POST:
                brukerkonto = medlem.brukerkonto
                brukerkonto.delete()
            return redirect('medlem_info', medlem.id)
        elif uform.is_valid():
            utmerkelse = uform.save(commit=False)
            utmerkelse.medlem = medlem
            utmerkelse.save()
            return redirect('medlem_redi', medlem.id)
        elif eform.is_valid():
            erfaring = eform.save(commit=False)
            erfaring.medlem = medlem
            erfaring.save()
            return redirect('medlem_redi', medlem.id)
    else:
        mform = MedlemForm(instance=medlem)
        eform = forms.ErfaringMedForm()
        uform = forms.UtmerkelseForm()
    return render(request, 'medlemmer/medlem_redi.html',
                  {'medlem': medlem, 'mform': mform, 'uform': uform, 'eform': eform})


@permission_required('SITdata.delete_medlem')
def view_medlem_slett(request, mid):
    medlem = get_object_or_404(models.Medlem, id=mid)
    if (request.method == 'POST'):
        medlem.delete()
        return redirect('medlemmer')
    return render(request, 'medlemmer/medlem_slett.html', {'medlem': medlem})


@permission_required('SITdata.delete_utmerkelse')
def view_utmerkelse_fjern(request, uid):
    utmerkelse = get_object_or_404(models.Utmerkelse, id=uid)
    if (request.method == 'POST'):
        medlem = utmerkelse.medlem
        utmerkelse.delete()
        return redirect('medlem_info', medlem.id)
    return render(request, 'medlemmer/utmerkelse_fjern.html', {'utmerkelse': utmerkelse})


def view_produksjoner(request):
    return render(request, 'produksjoner/produksjoner.html', {'pliste': models.Produksjon.objects.all()})


@permission_required('SITdata.add_produksjon')
def view_produksjon_ny(request):
    if request.method == 'POST':
        pform = forms.ProduksjonAdminForm(request.POST, request.FILES)
        if pform.is_valid():
            produksjon = pform.save()
            return redirect('produksjon_info', produksjon.id)
    else:
        pform = forms.ProduksjonAdminForm()
    return render(request, 'produksjoner/produksjon_ny.html', {'pform': pform})


def view_produksjon_info(request, pid):
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.user.has_perm('SITdata.change_produksjon'):
        access = 'admin'
    elif request.user.is_authenticated \
            and request.user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent"):
        access = 'own'
    else:
        access = 'other'
    verv_list = produksjon.erfaringer.all().values_list("verv", flat=True).distinct()
    verv_dict = {}
    for verv_key in verv_list:
        erfaringer = produksjon.erfaringer.filter(verv__exact=verv_key)
        if erfaringer.count() == 1:
            verv_dict[models.Verv.objects.get(pk=verv_key).tittel] = erfaringer
        else:
            verv_dict[models.Verv.objects.get(pk=verv_key).plural()] = erfaringer
    return render(request, 'produksjoner/produksjon_info.html',
                  {'access': access, 'produksjon': produksjon, 'verv_dict': verv_dict})


@login_required
def view_produksjon_redi(request, pid):
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.user.has_perm('SITdata.change_produksjon'):
        ProduksjonForm = forms.ProduksjonAdminForm
    elif request.user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent"):
        ProduksjonForm = forms.ProduksjonOwnForm
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    if request.method == 'POST':
        pform = ProduksjonForm(request.POST, request.FILES, instance=produksjon)
        fform = forms.ForestillingForm(request.POST)
        eform = forms.ErfaringProdForm(request.POST, request.FILES)
        if pform.is_valid():
            pform.save()
            return redirect('produksjon_info', produksjon.id)
        elif fform.is_valid():
            forestilling = fform.save(commit=False)
            forestilling.produksjon = produksjon
            forestilling.save()
            return redirect('produksjon_redi', produksjon.id)
        elif eform.is_valid():
            erfaring = eform.save(commit=False)
            erfaring.produksjon = produksjon
            erfaring.save()
            return redirect('produksjon_redi', produksjon.id)
    else:
        pform = ProduksjonForm(instance=produksjon)
        fform = forms.ForestillingForm()
        eform = forms.ErfaringProdForm()
    return render(request, 'produksjoner/produksjon_redi.html',
                  {'produksjon': produksjon, 'pform': pform, 'fform': fform, 'eform': eform})


@permission_required('SITdata.delete_produksjon')
def view_produksjon_slett(request, pid):
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.method == 'POST':
        produksjon.delete()
        return redirect('produksjoner')
    return render(request, 'produksjoner/produksjon_slett.html', {'produksjon': produksjon})


@login_required
def view_forestilling_fjern(request, fid):
    forestilling = get_object_or_404(models.Forestilling, id=fid)
    if request.user.has_perm('SITdata.delete_forestilling') \
            or request.user.medlem.erfaringer.all() & forestilling.produksjon.erfaringer.filter(
        verv__tittel="produsent"):
        if request.method == 'POST':
            produksjon = forestilling.produksjon
            forestilling.delete()
            return redirect('produksjon_info', forestilling.produksjon.id)
        return render(request, 'produksjoner/forestilling_fjern.html', {'forestilling': forestilling})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_verv(request):
    return render(request, 'verv.html')


@login_required
def view_erfaring_fjern(request, eid):
    erfaring = get_object_or_404(models.Erfaring, id=eid)
    if request.user.has_perm('SITdata.delete_erfaring') \
            or erfaring.produksjon \
            and request.user.medlem.erfaringer.all() & erfaring.produksjon.erfaringer.filter(verv__tittel="produsent"):
        if request.method == 'POST':
            medlem = erfaring.medlem
            erfaring.delete()
            return redirect('medlem_info', medlem.id)
        return render(request, 'medlemmer/erfaring_fjern.html', {'erfaring': erfaring})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_uttrykk(request):
    return render(request, 'uttrykk.html')


@login_required
def view_dokumenter(request):
    return render(request, 'dokumenter.html')


@login_required
def view_arkiv(request):
    return render(request, 'arkiv.html')
