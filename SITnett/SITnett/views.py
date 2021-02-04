
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

import os
import datetime

from SITdata import models, forms
from SITdata import skrift_transfers

features = settings.FEATURES

def view_hoved(request):
    # Legg inn riktig URL i anførselstegnene for å laste over følgende Skrift-data: 
    # skrift_transfers.transfer_all_medlemmer("/Users/jonas/Desktop/Skriftdata/")
    return render(request, 'hoved.html', {'FEATURES': features})


def view_info(request):
    return render(request, 'info.html', {'FEATURES': features})


def view_opptak(request):
    return render(request, 'opptak.html', {'FEATURES': features})


def make_soppslag(ar):
# lager et styre-oppslag (en dict over styreverv dette året) på formen {verv:[medlem, ...], ...}.
    serfaringer = models.Erfaring.objects.filter(verv__vtype=1).filter(ar=ar)
    if serfaringer.count():
        vids = serfaringer.values_list('verv', flat=True).distinct().order_by()
        soppslag = {}
        for vid in vids:
            if vid == None:
                continue
            verv = models.Verv.objects.get(pk=vid)
            erfaringer = models.Erfaring.objects.filter(verv__id=vid).filter(ar=ar)
            soppslag[verv] = erfaringer
    else:
        soppslag = None
    return soppslag

def make_goppslag(ar,authenticated):
# lager et gjeng-oppslag (en dict over gjengverv dette året) på formen {verv:[medlem, medlem, ...], ...}.
    if not authenticated:
        gerfaringer = models.Erfaring.objects.filter(verv__vtype=2).filter(ar=ar)
    else:
        gerfaringer = models.Erfaring.objects.filter(verv__vtype__in=[2,3]).filter(ar=ar)
    if gerfaringer.count():
        vids = gerfaringer.values_list('verv', flat=True).distinct().order_by()
        goppslag = {}
        for vid in vids:
            if vid == None:
                continue
            verv = models.Verv.objects.get(pk=vid)
            erfaringer = models.Erfaring.objects.filter(verv__id=vid).filter(ar=ar)
            goppslag[verv] = erfaringer
    else:
        goppslag = None
    return goppslag


def view_kontakt(request):
    if not features.TOGGLE_KONTAKT:
        return redirect('hoved')
    ar = datetime.datetime.now().year
    soppslag = make_soppslag(ar)
    goppslag = make_goppslag(ar,request.user.is_authenticated)
    mliste = models.Medlem.objects.filter(status__in=[1,2]).order_by('etternavn')
    return render(request, 'kontakt.html', {'FEATURES': features,
        'soppslag': soppslag, 'goppslag': goppslag, 'mliste': mliste})


def view_medlemmer(request):
    if not features.TOGGLE_MEDLEMMER:
        return redirect('hoved')
	# Lazy evelation of query sets ensure the database isn't queried before the
	# members variable is evaluated
	members = models.Medlem.objects.all()
	name = ""
	admission_year_from = ""
	admission_year_to = ""
	groups = [1, 2, 3]
	statuses = [1, 2, 3, 4]

	if request.GET:
		if request.GET.get("name", False):
			name = request.GET["name"]
			members = (
				members.filter(fornavn__icontains=name)
				| members.filter(mellomnavn__icontains=name)
				| members.filter(etternavn__icontains=name)
				| members.filter(kallenavn__icontains=name)
			)
		if request.GET.get("admission_year_from", False):
			admission_year_from = int(request.GET["admission_year_from"])
			members = members.filter(opptaksar__gte=admission_year_from)
		if request.GET.get("admission_year_to", False):
			try:
				admission_year_to = int(request.GET["admission_year_to"])
				members = members.filter(opptaksar__lte=admission_year_to)
			except ValueError:
				pass
		try:
			groups = [int(x) for x in request.GET.getlist("group")]
			if len(groups) < 3:
				members = members.filter(undergjeng__in=groups)
		except ValueError:
			pass

		try:
			statuses = [int(x) for x in request.GET.getlist("status")]
			if len(statuses) < 4:
				members = members.filter(status__in=statuses)
		except ValueError:
			pass

	return render(
		request,
		"medlemmer/medlemmer.html",
		{
            'FEATURES': features,
			"mliste": members,
			"name": name,
			"admission_year_from": admission_year_from,
			"admission_year_to": admission_year_to,
			"groups": groups,
			"statuses": statuses,
		},
	)


@permission_required('SITdata.add_medlem')
def view_medlem_ny(request):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
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
    return render(request, 'medlemmer/medlem_ny.html', {'FEATURES': features,
        'mform': mform})


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
    return render(request, 'medlemmer/medlem_info.html', {'FEATURES': features, 'access': access,
        'medlem': medlem})


@login_required
def view_medlem_redi(request, mid):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    medlem = get_object_or_404(models.Medlem, id=mid)
    if request.user.has_perm('SITdata.change_medlem'):
        MedlemForm = forms.MedlemAdminForm
    elif request.user == medlem.brukerkonto:
        MedlemForm = forms.MedlemOwnForm
    else:
        MedlemForm = forms.MedlemOtherForm
    if request.method == 'POST':
        mform = MedlemForm(request.POST, request.FILES, instance=medlem)
        eform = forms.ErfaringMedForm(request.POST,request.FILES)
        uform = forms.UtmerkelseForm(request.POST)
        if 'lagre_medlem' in request.POST and mform.is_valid():
            mform.save()
            if 'opprett_brukerkonto' in request.POST:
                brukerkonto = User.objects.create_user(medlem.brukernavn(), medlem.epost, 'ta-de-du!')
                medlem.brukerkonto = brukerkonto
                medlem.save()
            elif 'fjern_brukerkonto' in request.POST:
                brukerkonto = medlem.brukerkonto
                brukerkonto.delete()
            return redirect('medlem_info', medlem.id)
        elif 'lagre_utmerkelse' in request.POST and uform.is_valid():
            utmerkelse = uform.save(commit=False)
            utmerkelse.medlem = medlem
            utmerkelse.save()
            return redirect('medlem_redi', medlem.id)
        elif 'lagre_erfaring' in request.POST and eform.is_valid():
            erfaring = eform.save(commit=False)
            erfaring.medlem = medlem
            erfaring.save()
            return redirect('medlem_redi', medlem.id)
    else:
        mform = MedlemForm(instance=medlem)
        eform = forms.ErfaringMedForm()
        uform = forms.UtmerkelseForm()
    return render(request, 'medlemmer/medlem_redi.html', {'FEATURES': features,
        'medlem': medlem, 'mform': mform, 'uform': uform, 'eform': eform})


@permission_required('SITdata.delete_medlem')
def view_medlem_slett(request, mid):
    if not (features.TOGGLE_MEDLEMMER and features.TOGGLE_EDIT):
        return redirect('hoved')
    medlem = get_object_or_404(models.Medlem, id=mid)
    if (request.method == 'POST'):
        medlem.delete()
        return redirect('medlemmer')
    return render(request, 'medlemmer/medlem_slett.html', {'FEATURES': features,
        'medlem': medlem})


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
    pliste = models.Produksjon.objects.all()
    return render(request, 'produksjoner/produksjoner.html', {'FEATURES': features,
        'pliste': pliste})


def make_voppslag(produksjon):
# lager et verv-oppslag (en dict over verv i denne produksjonen) på formen {verv:[medlem, medlem, ...], ...}.
    vids = produksjon.erfaringer.all().values_list('verv', flat=True).distinct().order_by()
    voppslag = {}
    for vid in vids:
        if vid == None:
            continue
        verv = models.Verv.objects.get(pk=vid)
        erfaringer = produksjon.erfaringer.filter(verv=vid)
        voppslag[verv] = erfaringer
    return voppslag

def make_toppslag(produksjon):
# lager et tittel-oppslag (en dict over grunne verv i denne produksjonen) på formen {tittel:[medlem, medlem, ...], ...}.
    titler = produksjon.erfaringer.all().values_list('tittel', flat=True).distinct().order_by()
    toppslag = {}
    for tittel in titler:
        if tittel == "":
            continue
        erfaringer = produksjon.erfaringer.filter(tittel=tittel)
        if erfaringer.count() > 1:
            if tittel[-2:] == "er":
                toppslag[tittel+"e"] = erfaringer
            else:
                toppslag[tittel+"er"] = erfaringer
        else:
            toppslag[tittel] = erfaringer
    return toppslag


@permission_required('SITdata.add_produksjon')
def view_produksjon_ny(request):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    if request.method == 'POST':
        pform = forms.ProduksjonAdminForm(request.POST, request.FILES)
        if pform.is_valid():
            produksjon = pform.save()
            return redirect('produksjon_info', produksjon.id)
    else:
        pform = forms.ProduksjonAdminForm()
    return render(request, 'produksjoner/produksjon_ny.html', {'FEATURES': features,
        'pform': pform})


def view_produksjon_info(request, pid):
    if not features.TOGGLE_PRODUKSJONER:
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.user.has_perm('SITdata.change_produksjon'):
        access = 'admin'
    elif request.user.is_authenticated \
            and request.user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent"):
        access = 'own'
    else:
        access = 'other'
    voppslag = make_voppslag(produksjon)
    toppslag = make_toppslag(produksjon)
    return render(request, 'produksjoner/produksjon_info.html', {'FEATURES': features, 'access': access,
        'produksjon': produksjon, 'voppslag': voppslag, 'toppslag': toppslag})


@login_required
def view_produksjon_redi(request, pid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.user.has_perm('SITdata.change_produksjon'):
        ProduksjonForm = forms.ProduksjonAdminForm
    elif request.user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent"):
        ProduksjonForm = forms.ProduksjonOwnForm
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    voppslag = make_voppslag(produksjon)
    toppslag = make_toppslag(produksjon)
    if request.method == 'POST':
        pform = ProduksjonForm(request.POST, request.FILES, instance=produksjon)
        fform = forms.ForestillingForm(request.POST)
        aform = forms.AnmeldelseForm(request.POST, request.FILES)
        eform = forms.ErfaringProdForm(request.POST, request.FILES)
        if 'lagre_produksjon' in request.POST and pform.is_valid():
            pform.save()
            return redirect('produksjon_info', produksjon.id)
        elif 'lagre_forestilling' in request.POST and fform.is_valid():
            forestilling = fform.save(commit=False)
            forestilling.produksjon = produksjon
            forestilling.save()
            return redirect('produksjon_redi', produksjon.id)
        elif 'lagre_anmeldelse' in request.POST and aform.is_valid():
            anmeldelse = aform.save(commit=False)
            anmeldelse.produksjon = produksjon
            anmeldelse.save()
            return redirect('produksjon_redi', produksjon.id)
        elif 'lagre_erfaring' in request.POST and eform.is_valid():
            erfaring = eform.save(commit=False)
            erfaring.produksjon = produksjon
            erfaring.save()
            return redirect('produksjon_redi', produksjon.id)
    else:
        pform = ProduksjonForm(instance=produksjon)
        fform = forms.ForestillingForm()
        aform = forms.AnmeldelseForm()
        eform = forms.ErfaringProdForm()
    return render(request, 'produksjoner/produksjon_redi.html', {'FEATURES': features,
        'produksjon': produksjon, 'voppslag': voppslag, 'toppslag': toppslag,
        'pform': pform, 'fform': fform, 'aform': aform, 'eform': eform})


@permission_required('SITdata.delete_produksjon')
def view_produksjon_slett(request, pid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    produksjon = get_object_or_404(models.Produksjon, id=pid)
    if request.method == 'POST':
        produksjon.delete()
        return redirect('produksjoner')
    return render(request, 'produksjoner/produksjon_slett.html', {'FEATURES': features,
        'produksjon': produksjon})


@login_required
def view_forestilling_fjern(request, fid):
    if not (features.TOGGLE_PRODUKSJONER and features.TOGGLE_EDIT):
        return redirect('hoved')
    forestilling = get_object_or_404(models.Forestilling, id=fid)
    if request.user.has_perm('SITdata.delete_forestilling') \
        or request.user.medlem.erfaringer.all() & forestilling.produksjon.erfaringer.filter(
        verv__tittel="produsent"):
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
    if request.user.has_perm('SITdata.delete_anmeldelse') \
        or request.used.medlem.erfaringer.all() & forestilling.produksjon.erfaringer.filter(
        verv__tittel="produsent"):
        if request.method == 'POST':
            produksjon = anmeldelse.produksjon
            anmeldelse.delete()
            return redirect('produksjon_info', produksjon.id)
        return render(request, 'produksjoner/anmeldelse_fjern.html', {'FEATURES': features,
            'anmeldelse': anmeldelse})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_verv(request):
    if not features.TOGGLE_VERV:
        return redirect('hoved')
    vliste = models.Verv.objects.all()
    return render(request, 'verv/verv.html', {'FEATURES': features,
        'vliste': models.Verv.objects.all()})


@permission_required('SITdata.add_verv')
def view_verv_ny(request):
    if not (features.TOGGLE_VERV and features.TOGGLE_EDIT):
        return redirect('hoved')
    if request.method == 'POST':
        vform = forms.VervAdminForm(request.POST)
        if vform.is_valid():
            verv = vform.save()
            return redirect('verv_info', verv.id)
    else:
        vform = forms.VervAdminForm()
    return render(request, 'verv/verv_ny.html', {'FEATURES': features,
        'vform': vform})


@login_required
def view_verv_info(request, vid):
    if not features.TOGGLE_VERV:
        return redirect('hoved')
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    if request.user.has_perm('SITdata.change_verv'):
        access = 'admin'
    elif request.user.medlem.erfaringer.all() & verv.erfaringer.all():
        access = 'own'
    else:
        access = 'other'
    return render(request, 'verv/verv_info.html', {'FEATURES': features, 'access':access,
        'verv': verv})


@login_required
def view_verv_redi(request, vid):
    if not (features.TOGGLE_VERV and features.TOGGLE_EDIT):
        return redirect('hoved')
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    if models.Medlem.objects.filter(brukerkonto=request.user):
        serfaring = (request.user.medlem.erfaringer.all() & verv.erfaringer.all()).first()
    else:
        serfaring = None
    if request.user.has_perm('SITdata.change_verv'):
        VervForm = forms.VervAdminForm
        access = 'admin'
    elif serfaring:
        VervForm = forms.VervOwnForm
        access = 'own'
    else:
        return redirect('/konto/login/?next=%s' % request.path)
    if request.method == 'POST':
        vform = VervForm(request.POST, instance=verv)
        if access == 'admin':
            eform = forms.ErfaringVervForm(request.POST, request.FILES)
        else:
            eform = None
        if serfaring:
            sform = forms.ErfaringsskrivForm(request.POST, request.FILES, instance=serfaring)
        else:
            sform = None
        if 'lagre_verv' in request.POST and vform.is_valid():
            vform.save()
            return redirect('verv_info', verv.id)
        elif 'lagre_erfaring' in request.POST and eform.is_valid():
            erfaring = eform.save(commit=False)
            erfaring.verv = verv
            erfaring.save()
            return redirect('verv_redi', verv.id)
        elif 'lagre_erfaringsskriv' in request.POST and sform.is_valid():
            sform.save()
            return redirect('verv_redi', verv.id)
    else:
        vform = VervForm(instance=verv)
        if access == 'admin':
            eform = forms.ErfaringVervForm()
        else:
            eform = None
        if serfaring:
            sform = forms.ErfaringsskrivForm(instance=serfaring)
        else:
            sform = None
    return render(request, 'verv/verv_redi.html', {'FEATURES': features,
        'verv': verv, 'vform': vform, 'eform': eform, 'sform': sform})


@login_required
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
    if request.user.has_perm('SITdata.delete_erfaring') \
            or erfaring.produksjon \
            and request.user.medlem.erfaringer.all() & erfaring.produksjon.erfaringer.filter(verv__tittel="produsent"):
        if request.method == 'POST':
            medlem = erfaring.medlem
            erfaring.delete()
            return redirect('medlem_info', medlem.id)
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
def view_dokumenter(request):
    if not features.TOGGLE_DOKUMENTER:
        return redirect('hoved')
    return render(request, 'dokumenter.html', {'FEATURES': features})


@login_required
def view_arkiv(request):
    if not features.TOGGLE_ARKIV:
        return redirect('hoved')
    return render(request, 'arkiv.html', {'FEATURES': features})