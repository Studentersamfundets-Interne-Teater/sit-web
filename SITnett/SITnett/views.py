from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

import datetime

from SITdata import models, forms

features = settings.FEATURES


def get_ar(arstall: int) -> models.Ar:
    # finner et gitt år, eller oppretter det hvis det ikke ligger inne i databasen.
    if ar := models.Ar.objects.filter(pk=arstall).first():
        return ar
    ar = models.Ar(pk=arstall)
    ar.save()
    return ar


def get_blesteliste(dag: datetime.date):
    # henter ei liste over produksjoner som skal blæstes på forsida.
    blesteliste = models.Produksjon.objects.filter(blestestart__isnull=False,blestestart__lte=dag)
    pids = [produksjon.id for produksjon in blesteliste if produksjon.blestestopp() >= dag]
    blesteliste = blesteliste.filter(id__in=pids).order_by("premieredato")
    return blesteliste


def get_infotekst() -> str:
# henter ut infotekst fra et eventuelt uttrykk med tittel "Studentersamfundets Interne Teater" i uttrykksdatabasen.
    if info := models.Uttrykk.objects.filter(tittel="Studentersamfundets Interne Teater").first():
        return info.beskrivelse
    return ""

def view_hoved(request):
    dag = datetime.datetime.now().date()
    ar = get_ar(dag.year)
    blesteliste = get_blesteliste(dag)
    infotekst = get_infotekst()
    return render(request, 'hoved.html', {'FEATURES': features,
        'ar': ar, 'infotekst': infotekst, 'dag': dag, 'blesteliste': blesteliste})


def view_info(request):
    arstall = datetime.datetime.now().year
    ar = get_ar(arstall)
    infotekst = get_infotekst()
    return render(request, 'info.html', {'FEATURES': features,
        'ar': ar, 'infotekst': infotekst})


def view_opptak(request):
    klokke = datetime.datetime.now().time()
    dag = datetime.datetime.now().date()
    ar = get_ar(dag.year)
    if ar.opptaksstart and ar.soknadsfrist:
        if ar.opptaksstart <= dag and ar.soknadsfrist.date() >= dag and ar.soknadsfrist.time() >= klokke:
            opptak = True
        else:
            opptak = False
    else:
        opptak = False
    return render(request, 'opptak.html', {'FEATURES': features,
        'ar': ar, 'opptak': opptak})


def make_styrevervoppslag(ar):
    # lager et oppslag på formen {verv: [erfaring, erfaring, ...], ...} over styrevervene et gitt år, sortert etter verv-id.
    styreerfaringer = models.Erfaring.objects.filter(ar=ar).filter(verv__vervtype=1)
    if styreerfaringer.count():
        vids = styreerfaringer.values_list('verv', flat=True).distinct().order_by('verv__id')
        vervoppslag = {}
        for vid in vids:
            if vid == None:
                continue
            verv = models.Verv.objects.get(id=vid)
            erfaringer = models.Erfaring.objects.filter(ar=ar).filter(verv__id=vid).order_by('rolle')
            vervoppslag[verv] = erfaringer
    else:
        vervoppslag = None
    return vervoppslag


def make_gjengvervoppslag(ar,authenticated):
    # lager et oppslag på formen {verv: [erfaring, erfaring, ...], ...} over gjengvervene et gitt år, sortert etter verv-id.
    # Hvis man er logga inn får man opp både intern- og ekstern-gjengverv; ellers bare ekstern-.
    if not authenticated:
        gjengerfaringer = models.Erfaring.objects.filter(ar=ar).filter(verv__vervtype=2)
    else:
        gjengerfaringer = models.Erfaring.objects.filter(ar=ar).filter(verv__vervtype__in=[2,3])
    if gjengerfaringer.count():
        vids = gjengerfaringer.values_list('verv', flat=True).distinct().order_by('verv__id')
        vervoppslag = {}
        for vid in vids:
            if vid == None:
                continue
            verv = models.Verv.objects.get(id=vid)
            erfaringer = models.Erfaring.objects.filter(ar=ar).filter(verv__id=vid).order_by('rolle')
            vervoppslag[verv] = erfaringer
    else:
        vervoppslag = None
    return vervoppslag

def make_gjengtitteloppslag(ar,authenticated):
# lager et oppslag på formen {tittel: [erfaring, erfaring, ...], ...} over titler et gitt år som ikke er registrerte verv.
# Hvis man ikke er logga inn får man ikke opp noen titler.
    titler = models.Erfaring.objects.filter(ar=ar).values_list('tittel', flat=True).distinct()
    titteloppslag = {}
    if not authenticated:
        return titteloppslag
    for tittel in titler:
        if tittel == "":
            continue
        erfaringer = models.Erfaring.objects.filter(ar=ar).filter(tittel=tittel).order_by('rolle')
        if erfaringer.count() > 1:
            if tittel[-2:] == "er" or tittel[-3:] == "lig":
                titteloppslag[tittel+"e"] = erfaringer
            elif tittel[-1:] == "e":
                titteloppslag[tittel+"r"] = erfaringer
            else:
                titteloppslag[tittel+"er"] = erfaringer
        else:
            titteloppslag[tittel] = erfaringer
    return titteloppslag


def view_kontakt(request):
    if not features.TOGGLE_KONTAKT:
        return redirect('hoved')
    arstall = datetime.datetime.now().year
    styreoppslag = make_styrevervoppslag(arstall)
    vervoppslag = make_gjengvervoppslag(arstall,request.user.is_authenticated)
    return render(request, 'kontakt.html', {'FEATURES': features,
        'styreoppslag': styreoppslag, 'vervoppslag': vervoppslag})

@login_required
def view_Lommelista(request):
    if not features.TOGGLE_KONTAKT:
        return redirect('hoved')
    arstall = datetime.datetime.now().year
    lommeliste = models.Medlem.objects.filter(status__in=[1,2]).order_by('etternavn')
    return render(request, 'Lommelista.html', {'FEATURES': features,
        'lommeliste': lommeliste})


def view_medlemmer(request):
    if not features.TOGGLE_MEDLEMMER:
        return redirect('hoved')
    medlemsliste = models.Medlem.objects.all()
    if request.GET:
        medlemsform = forms.MedlemSearchForm(request.GET)

        if navn := request.GET.get('navn'):
            individual_names = navn.strip().split()
            for name in individual_names:
                medlemsliste = medlemsliste.filter(
                    Q(fornavn__icontains=name)
                    | Q(mellomnavn__icontains=name)
                    | Q(etternavn__icontains=name)
                    | Q(kallenavn__icontains=name)
                )

        if undergjenger := request.GET.getlist('undergjeng'):
            if '0' in undergjenger:
                ukjentliste = medlemsliste.filter(undergjeng__isnull=True)
            else:
                ukjentliste = medlemsliste.none()
            medlemsliste = (medlemsliste.filter(undergjeng__in=undergjenger) | ukjentliste)

        if statuser := request.GET.getlist('status'):
            if '0' in statuser:
                ukjentliste = medlemsliste.filter(status__isnull=True)
            else:
                ukjentliste = medlemsliste.none()
            medlemsliste = (medlemsliste.filter(status__in=statuser) | ukjentliste)

        if 'ukjent_ar' in request.GET:
            ukjentliste = medlemsliste.filter(opptaksar__isnull=True)
            if not request.GET.get('fra_ar') and not request.GET.get('til_ar'):
                medlemsliste = ukjentliste
        else:
            ukjentliste = medlemsliste.none()

        if fra_ar := request.GET.get('fra_ar'):
            medlemsliste = (medlemsliste.filter(opptaksar__gte=fra_ar) | ukjentliste)

        if til_ar := request.GET.get('til_ar'):
            medlemsliste = (medlemsliste.filter(opptaksar__lte=til_ar) | ukjentliste)

        if medlemstyper := request.GET.getlist('medlemstype'):
            medlemsliste = medlemsliste.filter(medlemstype__in=medlemstyper)
            for medlemstype in medlemstyper: # inkluderer andre medlemmer enn SITere, selv om de ikke har undergjeng, status eller opptaksår.
                if medlemstype != '1':
                    medlemsliste = (medlemsliste | models.Medlem.objects.filter(medlemstype=medlemstype))

        if titler := request.GET.getlist('tittel'):
            ordner = request.GET.getlist('orden')
            utmerkelsesliste = models.Utmerkelse.objects.filter(tittel__in=titler).filter(orden__in=ordner)
            mids = utmerkelsesliste.values_list('medlem',flat=True).distinct()
            medlemsliste = medlemsliste.filter(id__in=mids)

    else:
        arstall = datetime.datetime.now().year
        medlemsform = forms.MedlemSearchForm()
        medlemsliste = medlemsliste.filter(undergjeng__in=[1,2,3]).filter(status__in=[1,2,3]).filter(medlemstype=1)
        medlemsliste = medlemsliste.filter(opptaksar__gte=(arstall-10))
            # filtrerer ut SITere fra de siste 10 årene som utgangspunkt.
    return render(request, "medlemmer/medlemmer.html", {'FEATURES': features,
        'medlemsliste': medlemsliste, 'medlemsform': medlemsform})


@permission_required('SITdata.add_medlem')
def view_medlem_ny(request):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    if request.method == 'POST':
        medlemsform = forms.MedlemAdminForm(request.POST, request.FILES)
        if medlemsform.is_valid():
            medlem = medlemsform.save()
            if 'opprett_brukerkonto' in request.POST:
                brukerkonto = User.objects.create_user(medlem.brukernavn(), medlem.epost, 'ta-de-du!')
                medlem.brukerkonto = brukerkonto
                medlem.save()
            return redirect('medlem_info', medlem.id)
    else:
        medlemsform = forms.MedlemAdminForm()
    return render(request, 'medlemmer/medlem_ny.html', {'FEATURES': features,
        'medlemsform': medlemsform})


def make_gjengerfaringsoppslag(medlem,authenticated):
    # lager et oppslag på formen {årstall: [erfaring, erfaring, ...], ...} over gjengerfaringene til et medlem,
    # sortert etter år og verv-id.
    # Hvis man er logga inn får man opp både styre-, ekstern- og intern-gjengverv; ellers bare styre- og ekstern-.
    gjengerfaringer = medlem.erfaringer.filter(produksjon__isnull=True)
    if not authenticated:
        gjengerfaringer = gjengerfaringer.filter(verv__vervtype__in=[1,2])
    if gjengerfaringer.count():
        ar = gjengerfaringer.values_list('ar', flat=True).distinct().order_by('-ar')
        erfaringsoppslag = {}
        for arstall in ar:
            if arstall == None:
                continue
            erfaringer = gjengerfaringer.filter(ar=arstall).order_by('verv__id')
            erfaringsoppslag[arstall] = erfaringer
    else:
        erfaringsoppslag = None
    return erfaringsoppslag


def make_produksjonserfaringsoppslag(medlem):
    # lager et oppslag på formen {produksjon: [erfaring, erfaring, ...], ...} over produksjonserfaringene til et medlem,
    # sortert etter premieredato og verv-id.
    produksjonserfaringer = medlem.erfaringer.filter(produksjon__isnull=False)
    if produksjonserfaringer.count():
        pids = produksjonserfaringer.values_list('produksjon', flat=True).distinct().order_by('-produksjon__premieredato')
        erfaringsoppslag = {}
        for pid in pids:
            if pid == None:
                continue
            produksjon = models.Produksjon.objects.get(id=pid)
            erfaringer = produksjonserfaringer.filter(produksjon=produksjon).order_by('verv__id')
            erfaringsoppslag[produksjon] = erfaringer
    else:
        erfaringsoppslag = None
    return erfaringsoppslag


def view_medlem_info(request, mid):
    if not features.TOGGLE_MEDLEMMER:
        return redirect('hoved')
    medlem = get_object_or_404(models.Medlem, id=mid)
    if request.user.has_perm('SITdata.change_medlem'):
        access = 'admin'
    elif request.user == medlem.brukerkonto:
        access = 'own'
    else:
        access = 'other'
    gjengerfaringsoppslag = make_gjengerfaringsoppslag(medlem,request.user.is_authenticated)
    produksjonserfaringsoppslag = make_produksjonserfaringsoppslag(medlem)
    return render(request, 'medlemmer/medlem_info.html', {'FEATURES': features, 'access': access,
        'medlem': medlem, 'gjengerfaringsoppslag':gjengerfaringsoppslag, 'produksjonserfaringsoppslag':produksjonserfaringsoppslag})


@login_required
def view_medlem_endre(request, mid):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    medlem = get_object_or_404(models.Medlem, id=mid)
    if request.user.has_perm('SITdata.change_medlem'):
        MedlemForm = forms.MedlemAdminForm
    elif request.user == medlem.brukerkonto:
        MedlemForm = forms.MedlemOwnForm
    else:
        MedlemForm = forms.MedlemOtherForm
    gjengerfaringsoppslag = make_gjengerfaringsoppslag(medlem,True)
    produksjonserfaringsoppslag = make_produksjonserfaringsoppslag(medlem)
    if request.method == 'POST':
        medlemsform = MedlemForm(request.POST, request.FILES, instance=medlem)
        erfaringsform = forms.ErfaringMedForm(request.POST,request.FILES)
        utmerkelsesform = forms.UtmerkelseForm(request.POST)
        if 'lagre_medlem' in request.POST and medlemsform.is_valid():
            medlemsform.save()
            if 'opprett_brukerkonto' in request.POST:
                brukerkonto = User.objects.create_user(medlem.brukernavn(), medlem.epost, 'ta-de-du!')
                medlem.brukerkonto = brukerkonto
                medlem.save()
            elif 'fjern_brukerkonto' in request.POST:
                brukerkonto = medlem.brukerkonto
                brukerkonto.delete()
            return redirect('medlem_info', medlem.id)
        elif 'lagre_utmerkelse' in request.POST and utmerkelsesform.is_valid():
            utmerkelse = utmerkelsesform.save(commit=False)
            utmerkelse.medlem = medlem
            utmerkelse.save()
            return redirect('medlem_endre', medlem.id)
        elif 'lagre_erfaring' in request.POST and erfaringsform.is_valid():
            erfaring = erfaringsform.save(commit=False)
            erfaring.medlem = medlem
            erfaring.save()
            return redirect('medlem_endre', medlem.id)
    else:
        medlemsform = MedlemForm(instance=medlem)
        erfaringsform = forms.ErfaringMedForm()
        utmerkelsesform = forms.UtmerkelseForm()
    return render(request, 'medlemmer/medlem_endre.html', {'FEATURES': features,
        'medlem': medlem, 'gjengerfaringsoppslag':gjengerfaringsoppslag, 'produksjonserfaringsoppslag':produksjonserfaringsoppslag,
        'medlemsform': medlemsform, 'utmerkelsesform': utmerkelsesform, 'erfaringsform': erfaringsform})


@permission_required('SITdata.delete_medlem')
def view_medlem_slett(request, mid):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    medlem = get_object_or_404(models.Medlem, id=mid)
    gjengerfaringsoppslag = make_gjengerfaringsoppslag(medlem,True)
    produksjonserfaringsoppslag = make_produksjonserfaringsoppslag(medlem)
    if (request.method == 'POST'):
        medlem.delete()
        return redirect('medlemmer')
    return render(request, 'medlemmer/medlem_slett.html', {'FEATURES': features,
        'medlem': medlem, 'gjengerfaringsoppslag':gjengerfaringsoppslag, 'produksjonserfaringsoppslag':produksjonserfaringsoppslag})


@permission_required('SITdata.delete_utmerkelse')
def view_utmerkelse_fjern(request, uid):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    utmerkelse = get_object_or_404(models.Utmerkelse, id=uid)
    if (request.method == 'POST'):
        medlem = utmerkelse.medlem
        utmerkelse.delete()
        return redirect('medlem_info', medlem.id)
    return render(request, 'medlemmer/utmerkelse_fjern.html', {'FEATURES': features,
        'utmerkelse': utmerkelse})


def view_produksjoner(request):
    if not features.TOGGLE_PRODUKSJONER:
        return redirect('hoved')
    produksjonsliste = models.Produksjon.objects.all()
    if request.GET:
        produksjonsform = forms.ProduksjonSearchForm(request.GET)
        if request.GET['tittel']:
            tittel = request.GET['tittel']
            produksjonsliste = produksjonsliste.filter(tittel__icontains=tittel)
        if 'produksjonstags' in request.GET and request.GET['produksjonstags'] != '':
            produksjonstags = request.GET.getlist('produksjonstags')
            produksjonsliste = produksjonsliste.filter(produksjonstags__id__in=produksjonstags)
        if request.GET['forfatter']:
            forfatter = request.GET['forfatter']
            produksjonsliste = produksjonsliste.filter(forfatter__icontains=forfatter)
        if 'lokale' in request.GET and request.GET['lokale'] != '':
            lokaler = request.GET.getlist('lokale')
            produksjonsliste = produksjonsliste.filter(lokale__id__in=lokaler)
        if request.GET['fra_ar']:
            fra_ar = request.GET['fra_ar']
            produksjonsliste = produksjonsliste.filter(premieredato__year__gte=fra_ar)
        if request.GET['til_ar']:
            til_ar = request.GET['til_ar']
            produksjonsliste = produksjonsliste.filter(premieredato__year__lte=til_ar)
        if 'produksjonstype' in request.GET and request.GET['produksjonstype'] != '':
            produksjonstyper = request.GET.getlist('produksjonstype')
            produksjonsliste = produksjonsliste.filter(produksjonstype__in=produksjonstyper)
        if request.GET['fritekst']:
            fritekst = request.GET['fritekst']
            produksjonsliste = (produksjonsliste.filter(beskrivelse__icontains=fritekst) |
                produksjonsliste.filter(anekdoter__icontains=fritekst) |
                produksjonsliste.filter(reklame__icontains=fritekst))
    else:
        arstall = datetime.datetime.now().year
        produksjonsform = forms.ProduksjonSearchForm()
        produksjonsliste = produksjonsliste.filter(premieredato__year__gte=(arstall-10))
            # filtrerer ut produksjoner fra de siste 10 årene som utgangspunkt.
    return render(request, 'produksjoner/produksjoner.html', {'FEATURES': features,
        'produksjonsliste': produksjonsliste, 'produksjonsform': produksjonsform})


@permission_required('SITdata.add_produksjon')
def view_produksjon_ny(request):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    if request.method == 'POST':
        produksjonsform = forms.ProduksjonAdminForm(request.POST, request.FILES)
        if produksjonsform.is_valid():
            produksjon = produksjonsform.save()
            return redirect('produksjon_info', produksjon.id)
    else:
        produksjonsform = forms.ProduksjonAdminForm()
    return render(request, 'produksjoner/produksjon_ny.html', {'FEATURES': features,
        'produksjonsform': produksjonsform})


def get_produsenterfaring(user,produksjon):
# sjekker om en bruker har produsenterfaring i en gitt produksjon, og returnerer den eventuelle erfaringa.
    if not user.is_authenticated:
        return None
    if models.Medlem.objects.filter(brukerkonto=user):
        return (user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent")).first()
    else:
        return None


def make_produksjonsvervoppslag(produksjon):
# lager et oppslag på formen {verv: [erfaring, erfaring, ...], ...} over vervene i en gitt produksjon, sortert etter verv-id.
    vids = produksjon.erfaringer.all().values_list('verv', flat=True).distinct().order_by('verv__id')
    vervoppslag = {}
    for vid in vids:
        if vid == None:
            continue
        verv = models.Verv.objects.get(id=vid)
        erfaringer = produksjon.erfaringer.filter(verv=vid).order_by('rolle')
        vervoppslag[verv] = erfaringer
    return vervoppslag

def make_produksjonstitteloppslag(produksjon):
# lager et oppslag på formen {tittel: [erfaring, erfaring, ...], ...} over titler i en gitt produksjon som ikke er registrerte verv.
    titler = produksjon.erfaringer.all().values_list('tittel', flat=True).distinct()
    titteloppslag = {}
    for tittel in titler:
        if tittel == "":
            continue
        erfaringer = produksjon.erfaringer.filter(tittel=tittel).order_by('rolle')
        if erfaringer.count() > 1:
            if tittel[-2:] == "er":
                titteloppslag[tittel+"e"] = erfaringer
            elif tittel[-1:] == "e":
                titteloppslag[tittel+"r"] = erfaringer
            else:
                titteloppslag[tittel+"er"] = erfaringer
        else:
            titteloppslag[tittel] = erfaringer
    return titteloppslag


def view_produksjon_info(request, pid):
    if not features.TOGGLE_PRODUKSJONER:
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    dag = datetime.datetime.now().date()
    if produksjon.forestillinger.count() and produksjon.forestillinger.last().tidspunkt.date() >= dag:
        ferdig = False
    elif produksjon.premieredato > dag:
        ferdig = False
    else:
        ferdig = True
    produsenterfaring = get_produsenterfaring(request.user,produksjon)
    if request.user.has_perm('SITdata.change_produksjon'):
        access = 'admin'
    elif produsenterfaring:
        access = 'own'
    else:
        access = 'other'
    produksjonstags = produksjon.produksjonstags.all()
    if produksjonstags.filter(tag="UKErevy") or produksjonstags.filter(tag="supperevy"):
        produksjonstags = produksjonstags.exclude(tag="revy")
    vervoppslag = make_produksjonsvervoppslag(produksjon)
    titteloppslag = make_produksjonstitteloppslag(produksjon)
    if models.Foto.objects.filter(nummer__produksjon=produksjon):
        nummerbilder = True
    else:
        nummerbilder = False
    if models.Opptak.objects.filter(nummer__produksjon=produksjon):
        nummeropptak = True
    else:
        nummeropptak = False
    return render(request, 'produksjoner/produksjon_info.html', {'FEATURES': features, 'access': access,
        'produksjon': produksjon, 'produksjonstags': produksjonstags,
        'vervoppslag': vervoppslag, 'titteloppslag': titteloppslag,
        'nummerbilder': nummerbilder, 'nummeropptak': nummeropptak, "ferdig":ferdig})


@login_required
def view_produksjon_endre(request, pid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    produsenterfaring = get_produsenterfaring(request.user,produksjon)
    if request.user.has_perm('SITdata.change_produksjon'):
        ProduksjonForm = forms.ProduksjonAdminForm
    elif produsenterfaring:
        ProduksjonForm = forms.ProduksjonOwnForm
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    produksjonstags = produksjon.produksjonstags.all()
    if produksjonstags.filter(tag="UKErevy") or produksjonstags.filter(tag="supperevy"):
        produksjonstags = produksjonstags.exclude(tag="revy")
    vervoppslag = make_produksjonsvervoppslag(produksjon)
    titteloppslag = make_produksjonstitteloppslag(produksjon)
    if request.method == 'POST':
        produksjonsform = ProduksjonForm(request.POST, request.FILES, instance=produksjon)
        forestillingsform = forms.ForestillingForm(request.POST)
        anmeldelsesform = forms.AnmeldelseForm(request.POST, request.FILES)
        erfaringsform = forms.ErfaringProdForm(request.POST, request.FILES)
        if 'lagre_produksjon' in request.POST and produksjonsform.is_valid():
            produksjonsform.save()
            return redirect('produksjon_info', produksjon.id)
        elif 'lagre_forestilling' in request.POST and forestillingsform.is_valid():
            forestilling = forestillingsform.save(commit=False)
            forestilling.produksjon = produksjon
            forestilling.save()
            return redirect('produksjon_endre', produksjon.id)
        elif 'lagre_anmeldelse' in request.POST and anmeldelsesform.is_valid():
            anmeldelse = anmeldelsesform.save(commit=False)
            anmeldelse.produksjon = produksjon
            anmeldelse.save()
            return redirect('produksjon_endre', produksjon.id)
        elif 'lagre_erfaring' in request.POST and erfaringsform.is_valid():
            erfaring = erfaringsform.save(commit=False)
            erfaring.produksjon = produksjon
            erfaring.save()
            return redirect('produksjon_endre', produksjon.id)
    else:
        produksjonsform = ProduksjonForm(instance=produksjon)
        forestillingsform = forms.ForestillingForm()
        anmeldelsesform = forms.AnmeldelseForm()
        erfaringsform = forms.ErfaringProdForm()
    return render(request, 'produksjoner/produksjon_endre.html', {'FEATURES': features,
        'produksjon': produksjon, 'produksjonstags': produksjonstags,
        'vervoppslag': vervoppslag, 'titteloppslag': titteloppslag,
        'produksjonsform': produksjonsform, 'forestillingsform': forestillingsform,
        'anmeldelsesform': anmeldelsesform, 'erfaringsform': erfaringsform})


@permission_required('SITdata.delete_produksjon')
def view_produksjon_slett(request, pid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    produksjonstags = produksjon.produksjonstags.all()
    if produksjonstags.filter(tag="UKErevy") or produksjonstags.filter(tag="supperevy"):
        produksjonstags = produksjonstags.exclude(tag="revy")
    vervoppslag = make_produksjonsvervoppslag(produksjon)
    titteloppslag = make_produksjonstitteloppslag(produksjon)
    if request.method == 'POST':
        produksjon.delete()
        return redirect('produksjoner')
    return render(request, 'produksjoner/produksjon_slett.html', {'FEATURES': features,
        'produksjon': produksjon, 'produksjonstags': produksjonstags,
        'vervoppslag': vervoppslag, 'titteloppslag': titteloppslag,})


@login_required
def view_forestilling_fjern(request, fid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    forestilling = get_object_or_404(models.Forestilling, id=fid)
    produsenterfaring = get_produsenterfaring(request.user,forestilling.produksjon)
    if request.user.has_perm('SITdata.delete_forestilling') or produsenterfaring:
        if request.method == 'POST':
            produksjon = forestilling.produksjon
            forestilling.delete()
            return redirect('produksjon_info', produksjon.id)
        return render(request, 'produksjoner/forestilling_fjern.html', {'FEATURES': features,
            'forestilling': forestilling})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_anmeldelse_fjern(request, aid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    anmeldelse = get_object_or_404(models.Anmeldelse, id=aid)
    produsenterfaring = get_produsenterfaring(request.user,anmeldelse.produksjon)
    if request.user.has_perm('SITdata.delete_anmeldelse') or produsenterfaring:
        if request.method == 'POST':
            produksjon = anmeldelse.produksjon
            anmeldelse.delete()
            return redirect('produksjon_info', produksjon.id)
        return render(request, 'produksjoner/anmeldelse_fjern.html', {'FEATURES': features,
            'anmeldelse': anmeldelse})
    else:
        return redirect('/konto/login?next=%s' % request.path)


def view_numre(request):
    if not features.TOGGLE_NUMRE:
        return redirect("hoved")
    search_query = request.GET.get("query", "")
    if search_query == "":
        nummerliste = models.Nummer.objects.all()
    else:
        nummerliste = (
            models.Nummer.objects.filter(tittel__icontains=search_query)
            | models.Nummer.objects.filter(produksjon__tittel__icontains=search_query)
            | models.Nummer.objects.filter(manus__icontains=search_query)
            | models.Nummer.objects.filter(beskrivelse__icontains=search_query)
            | models.Nummer.objects.filter(anekdoter__icontains=search_query)
        )

    return render(
        request,
        "numre/numre.html",
        {
            "FEATURES": features,
            "nummerliste": nummerliste,
            "search_query": search_query,
        },
    )


def view_nummer_info(request, nid):
    if not features.TOGGLE_NUMRE:
        return redirect('hoved')
    nummer = get_object_or_404(models.Nummer, id=nid)
    return render(request, 'numre/nummer_info.html', {'FEATURES': features,
        'nummer': nummer})


@login_required
def view_verv(request):
    if not features.TOGGLE_VERV:
        return redirect('hoved')
    vervliste = models.Verv.objects.all()
    return render(request, 'verv/verv.html', {'FEATURES': features, 'vervliste': models.Verv.objects.all()})


@permission_required('SITdata.add_verv')
def view_verv_ny(request):
    if not (features.TOGGLE_VERV and features.TOGGLE_EDIT):
        return redirect('hoved')
    if request.method == 'POST':
        vervform = forms.VervAdminForm(request.POST)
        if vervform.is_valid():
            verv = vervform.save()
            return redirect('verv_info', verv.id)
    else:
        vervform = forms.VervAdminForm()
    return render(request, 'verv/verv_ny.html', {'FEATURES': features,
        'vervform': vervform})


def get_ververfaring(user,verv):
# sjekker om en bruker har erfaring fra et gitt verv, og returnerer den eventuelle erfaringa.
    if not user.is_authenticated:
        return None
    if models.Medlem.objects.filter(brukerkonto=user):
        return (user.medlem.erfaringer.all() & verv.erfaringer.all()).first()
    else:
        return None


@login_required
def view_verv_info(request, vid):
    if not features.TOGGLE_VERV:
        return redirect('hoved')
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    ververfaring = get_ververfaring(request.user,verv)
    if request.user.has_perm('SITdata.change_verv'):
        access = 'admin'
    elif ververfaring:
        access = 'own'
    else:
        access = 'other'
    return render(request, 'verv/verv_info.html', {'FEATURES': features, 'access':access,
        'verv': verv})


@login_required
def view_verv_endre(request, vid):
    if not (features.TOGGLE_VERV and features.TOGGLE_EDIT):
        return redirect('hoved')
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    ververfaring = get_ververfaring(request.user,verv)
    if request.user.has_perm('SITdata.change_verv'):
        VervForm = forms.VervAdminForm
        access = 'admin'
    elif ververfaring:
        VervForm = forms.VervOwnForm
        access = 'own'
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    if request.method == 'POST':
        vervform = VervForm(request.POST, instance=verv)
        if access == 'admin':
            erfaringsform = forms.ErfaringVervForm(request.POST, request.FILES)
        else:
            erfaringsform = None
        if ververfaring:
            erfaringsskrivform = forms.ErfaringsskrivForm(request.POST, request.FILES, instance=ververfaring)
        else:
            erfaringsskrivform = None
        if 'lagre_verv' in request.POST and vervform.is_valid():
            vervform.save()
            return redirect('verv_info', verv.id)
        elif 'lagre_erfaring' in request.POST and erfaringsform.is_valid():
            erfaring = erfaringsform.save(commit=False)
            erfaring.verv = verv
            erfaring.save()
            return redirect('verv_endre', verv.id)
        elif 'lagre_erfaringsskriv' in request.POST and erfaringsskrivform.is_valid():
            erfaringsskrivform.save()
            return redirect('verv_endre', verv.id)
    else:
        vervform = VervForm(instance=verv)
        if access == 'admin':
            erfaringsform = forms.ErfaringVervForm()
        else:
            erfaringsform = None
        if ververfaring:
            erfaringsskrivform = forms.ErfaringsskrivForm(instance=ververfaring)
        else:
            erfaringsskrivform = None
    return render(request, 'verv/verv_endre.html', {'FEATURES': features,
        'verv': verv, 'vervform': vervform, 'erfaringsform': erfaringsform,
        'erfaringsskrivform': erfaringsskrivform})


@permission_required('SITdata.delete_verv')
def view_verv_slett(request, vid):
    if not (features.TOGGLE_VERV and features.TOGGLE_EDIT):
        return redirect('hoved')
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    if request.method == 'POST':
        verv.delete()
        return redirect('verv')
    return render(request, 'verv/verv_slett.html', {'FEATURES': features,
        'verv': verv})


@login_required
def view_erfaring_fjern(request, eid):
    if not ((features.TOGGLE_MEDLEMMER or features.TOGGLE_PRODUKSJONER or features.TOGGLE_VERV)
        and features.TOGGLE_EDIT):
        return redirect('hoved')
    erfaring = get_object_or_404(models.Erfaring, id=eid)
    if erfaring.produksjon:
        produsenterfaring = get_produsenterfaring(request.user,erfaring.produksjon)
    else:
        produsenterfaring = None
    if request.user.has_perm('SITdata.delete_erfaring') or produsenterfaring:
        if request.method == 'POST':
            if erfaring.medlem:
                medlem = erfaring.medlem
                erfaring.delete()
                return redirect('medlem_info', medlem.id)
            elif erfaring.produksjon:
                produksjon = erfaring.produksjon
                erfaring.delete()
                return redirect('produksjon_info', produksjon.id)
            elif erfaring.verv:
                verv = erfaring.verv
                erfaring.delete()
                return redirect('verv_info', verv.id)
            else:
                erfaring.delete()
                return redirect('hoved')
        return render(request, 'medlemmer/erfaring_fjern.html', {'FEATURES': features,
            'erfaring': erfaring})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_uttrykk(request):
    if not features.TOGGLE_UTTRYKK:
        return redirect('hoved')
    return render(request, 'uttrykk.html', {'FEATURES': features})


@login_required
def view_arkiv(request):
    if not features.TOGGLE_ARKIV:
        return redirect('hoved')
    return render(request, 'arkiv.html', {'FEATURES': features})


@login_required
def view_dokumenter(request):
    if not features.TOGGLE_DOKUMENTER:
        return redirect('hoved')
    return render(request, 'dokumenter.html', {'FEATURES': features})


def get_styreerfaring(user,arstall):
# sjekker om en bruker har styreerfaring fra et gitt år, og returnerer den eventuelle erfaringa.
    if not user.is_authenticated:
        return None
    if models.Medlem.objects.filter(brukerkonto=user):
        return (user.medlem.erfaringer.all() & models.Erfaring.objects.filter(ar=arstall).filter(verv__vervtype=1)).first()
    else:
        return None


def view_ar_info(request, arstall):
    if not features.TOGGLE_AR:
        return redirect('hoved')
    if arstall < 1910 or arstall > datetime.datetime.now().year:
        return redirect('hoved')
    ar = get_ar(arstall)
    styreerfaring = get_styreerfaring(request.user,ar.arstall)
    if request.user.has_perm('SITdata.change_ar'):
        access = 'admin'
    elif styreerfaring:
        access = 'own'
    else:
        access = 'other'
    styreoppslag = make_styrevervoppslag(arstall)
    vervoppslag = make_gjengvervoppslag(arstall,request.user.is_authenticated)
    titteloppslag = make_gjengtitteloppslag(arstall,request.user.is_authenticated)
    produksjonsliste = models.Produksjon.objects.filter(premieredato__year=arstall)
    return render(request, 'ar/ar_info.html', {'FEATURES': features, 'access': access,
        'ar': ar, 'styreoppslag': styreoppslag, 'vervoppslag': vervoppslag, 'titteloppslag': titteloppslag,
        'produksjonsliste': produksjonsliste})


@login_required
def view_ar_endre(request, arstall):
    if not (features.TOGGLE_AR and features.TOGGLE_EDIT):
        return redirect('hoved')
    ar = get_object_or_404(models.Ar, pk=arstall)
    styreerfaring = get_styreerfaring(request.user,ar.arstall)
    if request.user.has_perm('SITdata.change_ar'):
        access = 'admin'
    elif styreerfaring:
        access = 'own'
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    styreoppslag = make_styrevervoppslag(arstall)
    vervoppslag = make_gjengvervoppslag(arstall,request.user.is_authenticated)
    titteloppslag = make_gjengtitteloppslag(arstall,request.user.is_authenticated)
    produksjonsliste = models.Produksjon.objects.filter(premieredato__year=arstall)
    if request.method == 'POST':
        arsform = forms.ArForm(request.POST, request.FILES, instance=ar)
        erfaringsform = forms.ErfaringArForm(request.POST, request.FILES)
        if 'lagre_ar' in request.POST and arsform.is_valid():
            arsform.save()
            return redirect('ar_info', ar.arstall)
        elif 'lagre_erfaring' in request.POST and erfaringsform.is_valid():
            erfaring = erfaringsform.save(commit=False)
            erfaring.ar = ar.arstall
            erfaring.save()
            return redirect('ar_endre', ar.arstall)
    else:
        arsform = forms.ArForm(instance=ar)
        erfaringsform = forms.ErfaringArForm()
    return render(request, 'ar/ar_endre.html', {'FEATURES': features,
        'ar': ar, 'styreoppslag': styreoppslag, 'vervoppslag': vervoppslag, 'titteloppslag': titteloppslag,
        'produksjonsliste': produksjonsliste, 'arsform': arsform, 'erfaringsform': erfaringsform})


@permission_required('SITdata.add_medlem')
def view_ar_nyttkull(request, arstall):
    if not features.TOGGLE_EDIT:
        return redirect('hoved')
    ar = get_object_or_404(models.Ar, pk=arstall)
    return render(request, 'ar/ar_nyttkull.html', {'FEATURES': features,
        'ar': ar})
