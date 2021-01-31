
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

import os

from SITdata import models, forms
from SITdata import skrift_transfers


def view_hoved(request):
    # skrift_transfers.transfer_all_medlemmer("/Users/jacob/Downloads/sit skrift/sit/")
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


def make_voppslag(produksjon):
    vids = produksjon.erfaringer.all().values_list('verv', flat=True).distinct().order_by()
    voppslag = {}
    for vid in vids:
        if vid == None:
            continue
        verv = models.Verv.objects.get(pk=vid)
        erfaringer = produksjon.erfaringer.filter(verv=vid)
        if erfaringer.count() > 1:
            voppslag[verv.plural()] = erfaringer
        else:
            voppslag[verv] = erfaringer
    return voppslag

def make_toppslag(produksjon):
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
    voppslag = make_voppslag(produksjon)
    toppslag = make_toppslag(produksjon)
    return render(request, 'produksjoner/produksjon_info.html',
                  {'access': access, 'produksjon': produksjon, 'voppslag': voppslag, 'toppslag': toppslag})


@login_required
def view_produksjon_redi(request, pid):
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
    return render(request, 'produksjoner/produksjon_redi.html',
                  {'produksjon': produksjon, 'voppslag': voppslag, 'toppslag': toppslag,
                  'pform': pform, 'fform': fform, 'aform': aform, 'eform': eform})


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
            return redirect('produksjon_info', produksjon.id)
        return render(request, 'produksjoner/forestilling_fjern.html', {'forestilling': forestilling})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_anmeldelse_fjern(request, aid):
    anmeldelse = get_object_or_404(models.Anmeldelse, id=aid)
    if request.user.has_perm('SITdata.delete_anmeldelse') \
        or request.used.medlem.erfaringer.all() & forestilling.produksjon.erfaringer.filter(
        verv__tittel="produsent"):
        if request.method == 'POST':
            produksjon = anmeldelse.produksjon
            anmeldelse.delete()
            return redirect('produksjon_info', produksjon.id)
        return render(request, 'produksjoner/anmeldelse_fjern.html', {'anmeldelse': anmeldelse})
    else:
        return redirect('/konto/login?next=%s' % request.path)


@login_required
def view_verv(request):
    return render(request, 'verv/verv.html', {'vliste': models.Verv.objects.all()})


@login_required
def view_verv_info(request, vid):
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    if request.user.has_perm('SITdata.change_verv'):
        access = 'admin'
    elif request.user.medlem.erfaringer.all() & verv.erfaringer.all():
        access = 'own'
    else:
        access = 'other'
    return render(request, 'verv/verv_info.html', {'access':access, 'verv': verv})


@login_required
def view_verv_redi(request, vid):
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
    return render(request, 'verv/verv_redi.html',
                  {'verv': verv, 'vform': vform, 'eform': eform, 'sform': sform})


@login_required
def view_verv_slett(request, vid):
    verv = get_object_or_404(models.Verv, id=vid)
    if not verv.erfaringsoverforing:
        return redirect('verv')
    if request.method == 'POST':
        verv.delete()
        return redirect('verv')
    return render(request, 'verv/verv_slett.html', {'verv': verv})


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