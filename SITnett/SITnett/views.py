from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required,permission_required

from SITdata import models,forms


def view_hoved(request):
	return render(request,'hoved.html')

def view_info(request):
	return render(request,'info.html')

def view_opptak(request):
	return render(request,'opptak.html')

def view_kontakt(request):
	return render(request,'kontakt.html')

def view_medlemmer(request):
	return render(request,'medlemmer/medlemmer.html',{'mliste':models.Medlem.objects.all()})

@permission_required('SITdata.add_medlem')
def view_medlem_ny(request):
	if request.method == 'POST':
		mform = forms.MedlemForm(request.POST,request.FILES)
		if mform.is_valid():
			medlem = mform.save()
			if 'opprett_brukerkonto' in request.POST:
				brukerkonto = User.objects.create_user(medlem.brukernavn(),medlem.epost,'ta-de-du!')
				medlem.brukerkonto = brukerkonto
				medlem.save()
			return redirect('medlem_info',medlem.id)
	else:
		mform = forms.MedlemForm()
	return render(request,'medlemmer/medlem_ny.html',{'mform':mform})

def view_medlem_info(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	if request.user.has_perm('SITdata.change_medlem'):
		access = 'admin'
	elif request.user == medlem.brukerkonto:
		access = 'own'
	else:
		access = 'other'
	return render(request,'medlemmer/medlem_info.html',{'access':access,'medlem':medlem})

@login_required
def view_medlem_redi(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	if request.user.has_perm('SITdata.change_medlem'):
		MedlemForm = forms.MedlemAdminForm
	elif request.user == medlem.brukerkonto:
		MedlemForm = forms.MedlemOwnForm
	else:
		MedlemForm = forms.MedlemOtherForm
	if request.method == 'POST':
		mform = MedlemForm(request.POST,instance=medlem)
		eform = forms.ErfaringMedForm(request.POST,request.FILES)
		uform = forms.UtmerkelseForm(request.POST)
		if mform.is_valid():
			mform.save()
			if 'opprett_brukerkonto' in request.POST:
				brukerkonto = User.objects.create_user(medlem.brukernavn(),medlem.epost,'ta-de-du!')
				medlem.brukerkonto = brukerkonto
				medlem.save()
			elif 'fjern_brukerkonto' in request.POST:
				brukerkonto = medlem.brukerkonto
				brukerkonto.delete()
			return redirect('medlem_info',medlem.id)
		elif uform.is_valid():
			utmerkelse = uform.save(commit=False)
			utmerkelse.medlem = medlem
			utmerkelse.save()
			return redirect('medlem_redi',medlem.id)
		elif eform.is_valid():
			erfaring = eform.save(commit=False)
			erfaring.medlem = medlem
			erfaring.save()
			return redirect('medlem_redi',medlem.id)
	else:
		mform = MedlemForm(instance=medlem)
		eform = forms.ErfaringMedForm()
		uform = forms.UtmerkelseForm()
	return render(request,'medlemmer/medlem_redi.html',{'medlem':medlem,'mform':mform,'uform':uform,'eform':eform})

@permission_required('SITdata.delete_medlem')
def view_medlem_slett(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	if (request.method == 'POST'):
		medlem.delete()
		return redirect('medlemmer')
	return render(request,'medlemmer/medlem_slett.html',{'medlem':medlem})

@permission_required('SITdata.delete_utmerkelse')
def view_utmerkelse_fjern(request,uid):
	utmerkelse = get_object_or_404(models.Utmerkelse,id=uid)
	if (request.method == 'POST'):
		medlem = utmerkelse.medlem
		utmerkelse.delete()
		return redirect('medlem_info',medlem.id)
	return render(request,'medlemmer/utmerkelse_fjern.html',{'utmerkelse':utmerkelse})

def view_produksjoner(request):
	return render(request,'produksjoner/produksjoner.html',{'pliste':models.Produksjon.objects.all()})

@permission_required('SITdata.add_produksjon')
def view_produksjon_ny(request):
	if request.method == 'POST':
		pform = forms.ProduksjonForm(request.POST,request.FILES)
		if pform.is_valid():
			produksjon = pform.save()
			return redirect('produksjon_info',produksjon.id)
	else:
		pform = forms.ProduksjonForm()
	return render(request,'produksjoner/produksjon_ny.html',{'pform':pform})

def view_produksjon_info(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
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
	return render(request,'produksjoner/produksjon_info.html',{'access':access,'produksjon':produksjon, 'verv_dict':verv_dict})

@login_required
def view_produksjon_redi(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
	if request.user.has_perm('SITdata.change_produksjon'):
		ProduksjonForm = forms.ProduksjonAdminForm
	elif request.user.medlem.erfaringer.all() & produksjon.erfaringer.filter(verv__tittel="produsent"):
		ProduksjonForm = forms.ProduksjonOwnForm
	else:
		return redirect('/konto/login/?next=%s'%request.path)
	if request.method == 'POST':
		pform = ProduksjonForm(request.POST,request.FILES,instance=produksjon)	
		fform = forms.ForestillingForm(request.POST)
		eform = forms.ErfaringProdForm(request.POST,request.FILES)
		if pform.is_valid():
			pform.save()
			return redirect('produksjon_info',produksjon.id)
		elif fform.is_valid():
			forestilling = fform.save(commit=False)
			forestilling.produksjon = produksjon
			forestilling.save()
			return redirect('produksjon_redi',produksjon.id)
		elif eform.is_valid():
			erfaring = eform.save(commit=False)
			erfaring.produksjon = produksjon
			erfaring.save()
			return redirect('produksjon_redi',produksjon.id)
	else:
		pform = ProduksjonForm(instance=produksjon)
		fform = forms.ForestillingForm()
		eform = forms.ErfaringProdForm()
	return render(request,'produksjoner/produksjon_redi.html',{'produksjon':produksjon,'pform':pform,'fform':fform,'eform':eform})

@permission_required('SITdata.delete_produksjon')
def view_produksjon_slett(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
	if request.method == 'POST':
		produksjon.delete()
		return redirect('produksjoner')
	return render(request,'produksjoner/produksjon_slett.html',{'produksjon':produksjon})

@login_required
def view_forestilling_fjern(request,fid):
	forestilling = get_object_or_404(models.Forestilling,id=fid)
	if request.user.has_perm('SITdata.delete_forestilling') \
	or request.user.medlem.erfaringer.all() & forestilling.produksjon.erfaringer.filter(verv__tittel="produsent"):
		if request.method == 'POST':
			produksjon = forestilling.produksjon
			forestilling.delete()
			return redirect('produksjon_info',forestilling.produksjon.id)
		return render(request,'produksjoner/forestilling_fjern.html',{'forestilling':forestilling})
	else:
		return redirect('/konto/login?next=%s'%request.path)

@login_required
def view_verv(request):
	return render(request,'verv.html')

@login_required
def view_erfaring_fjern(request,eid):
	erfaring = get_object_or_404(models.Erfaring,id=eid)
	if request.user.has_perm('SITdata.delete_erfaring') \
	or erfaring.produksjon \
	and request.user.medlem.erfaringer.all() & erfaring.produksjon.erfaringer.filter(verv__tittel="produsent"):
		if request.method == 'POST':
			medlem = erfaring.medlem
			erfaring.delete()
			return redirect('medlem_info',medlem.id)
		return render(request,'medlemmer/erfaring_fjern.html',{'erfaring':erfaring})
	else:
		return redirect('/konto/login?next=%s'%request.path)

@login_required
def view_uttrykk(request):
	return render(request,'uttrykk.html')

@login_required
def view_dokumenter(request):
	return render(request,'dokumenter.html')

@login_required
def view_arkiv(request):
	return render(request,'arkiv.html')