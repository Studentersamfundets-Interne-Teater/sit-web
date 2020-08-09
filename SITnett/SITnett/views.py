from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404

from SITdata import models,forms

def hoved(request):
	return render(request,'hoved.html')

def info(request):
	return render(request,'info.html')

def opptak(request):
	return render(request,'opptak.html')

def kontakt(request):
	return render(request,'kontakt.html')

def medlemmer(request):
	return render(request,'medlemmer.html',{'mliste':models.Medlem.objects.all()})

def medlem_ny(request):
	if (request.method == 'POST'):
		mform = forms.MedlemForm(request.POST,request.FILES)
		if mform.is_valid():
			medlem = mform.save()
			return HttpResponseRedirect(reverse('medlem_info',kwargs={'mid':medlem.id}))
	else:
		mform = forms.MedlemForm()
	return render(request,'medlem_ny.html',{'mform':mform})

def medlem_info(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	return render(request,'medlem_info.html',{'medlem':medlem})

def medlem_redi(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	if (request.method == 'POST'):
		mform = forms.MedlemForm(request.POST,request.FILES,instance=medlem)
		eform = forms.ErfaringMedForm(request.POST,request.FILES)
		uform = forms.UtmerkelseForm(request.POST)
		if mform.is_valid():
			mform.save()
			return HttpResponseRedirect(reverse('medlem_info',kwargs={'mid':medlem.id}))
		elif uform.is_valid():
			utmerkelse = uform.save(commit=False)
			utmerkelse.medlem = medlem
			utmerkelse.save()
			return HttpResponseRedirect(reverse('medlem_redi',kwargs={'mid':medlem.id}))
		elif eform.is_valid():
			erfaring = eform.save(commit=False)
			erfaring.medlem = medlem
			erfaring.save()
			return HttpResponseRedirect(reverse('medlem_redi',kwargs={'mid':medlem.id}))
	else:
		mform = forms.MedlemForm(instance=medlem)
		eform = forms.ErfaringMedForm()
		uform = forms.UtmerkelseForm()
	return render(request,'medlem_redi.html',{'medlem':medlem,'mform':mform,'uform':uform,'eform':eform})

def medlem_slett(request,mid):
	medlem = get_object_or_404(models.Medlem,id=mid)
	if (request.method == 'POST'):
		medlem.delete()
		return HttpResponseRedirect(reverse('medlemmer'))
	return render(request,'medlem_slett.html',{'medlem':medlem})

def utmerkelse_fjern(request,uid):
	utmerkelse = get_object_or_404(models.Utmerkelse,id=uid)
	if (request.method == 'POST'):
		medlem = utmerkelse.medlem
		utmerkelse.delete()
		return HttpResponseRedirect(reverse('medlem_info',kwargs={'mid':medlem.id}))
	return render(request,'utmerkelse_fjern.html',{'utmerkelse':utmerkelse})

def produksjoner(request):
	return render(request,'produksjoner.html',{'pliste':models.Produksjon.objects.all()})

def produksjon_ny(request):
	if (request.method == 'POST'):
		pform = forms.ProduksjonForm(request.POST,request.FILES)
		if pform.is_valid():
			produksjon = pform.save()
			return HttpResponseRedirect(reverse('produksjon_info',kwargs={'pid':produksjon.id}))
	else:
		pform = forms.ProduksjonForm()
	return render(request,'produksjon_ny.html',{'pform':pform})

def produksjon_info(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
	return render(request,'produksjon_info.html',{'produksjon':produksjon})

def produksjon_redi(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
	if (request.method == 'POST'):
		pform = forms.ProduksjonForm(request.POST,request.FILES,instance=produksjon)
		fform = forms.ForestillingForm(request.POST)
		eform = forms.ErfaringProdForm(request.POST,request.FILES)
		if pform.is_valid():
			pform.save()
			return HttpResponseRedirect(reverse('produksjon_info',kwargs={'pid':produksjon.id}))
		elif fform.is_valid():
			forestilling = fform.save(commit=False)
			forestilling.produksjon = produksjon
			forestilling.save()
			return HttpResponseRedirect(reverse('produksjon_redi',kwargs={'pid':produksjon.id}))
		elif eform.is_valid():
			erfaring = eform.save(commit=False)
			erfaring.produksjon = produksjon
			erfaring.save()
			return HttpResponseRedirect(reverse('produksjon_redi',kwargs={'pid':produksjon.id}))
	else:
		pform = forms.ProduksjonForm(instance=produksjon)
		fform = forms.ForestillingForm()
		eform = forms.ErfaringProdForm()
	return render(request,'produksjon_redi.html',{'produksjon':produksjon,'pform':pform,'fform':fform,'eform':eform})

def produksjon_slett(request,pid):
	produksjon = get_object_or_404(models.Produksjon,id=pid)
	if (request.method == 'POST'):
		produksjon.delete()
		return HttpResponseRedirect(reverse('produksjoner'))
	return render(request,'produksjon_slett.html',{'produksjon':produksjon})

def forestilling_fjern(request,fid):
	forestilling = get_object_or_404(models.Forestilling,id=fid)
	if (request.method == 'POST'):
		produksjon = forestilling.produksjon
		forestilling.delete()
		return HttpResponseRedirect(reverse('produksjon_info',kwargs={'pid':forestilling.produksjon.id}))
	return render(request,'forestilling_fjern.html',{'forestilling':forestilling})

def verv(request):
	return render(request,'verv.html')

def erfaring_fjern(request,eid):
	erfaring = get_object_or_404(models.Erfaring,id=eid)
	if (request.method == 'POST'):
		medlem = erfaring.medlem
		erfaring.delete()
		return HttpResponseRedirect(reverse('medlem_info',kwargs={'mid':medlem.id}))
	return render(request,'erfaring_fjern.html',{'erfaring':erfaring})

def uttrykk(request):
	return render(request,'uttrykk.html')

def dokumenter(request):
	return render(request,'dokumenter.html')

def arkiv(request):
	return render(request,'arkiv.html')
