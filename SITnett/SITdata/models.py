from django.db import models
from django.urls import reverse

import datetime

# Create your models here.

class Medlem(models.Model):
	MTYPER = ((1,'SIT'),(2,'Regi'),(3,'FK'),(4,'VK'),
		(5,'SO'),(6,'TSS'),(7,'TKS'),(8,'SPO'),(9,'UKA'),(10,'ISFiT'),
		(11,'MG'),(12,'ITK'),(13,'ARK'),(14,'FG'),(15,'KSG'),
		(16,'KU'),(17,'KLST'),(18,'LØK'),(19,'DG'),(20,'Profil'),(21,'ekstern'))
	UGJENGER = ((1,'Kostyme'),(2,'Kulisse'),(3,'Skuespill'))
	STATUSER = ((1,'aktiv'),(2,'veteran'),(3,'pangsionist'),(4,'permittert'))
	mtype = models.IntegerField("medlemstype",choices=MTYPER,default=1)
	fornavn = models.CharField(max_length=30)
	mellomnavn = models.CharField(blank=True,max_length=30)
	etternavn = models.CharField(max_length=30)
	fodsel = models.DateField("fødselsdato")
	opptak = models.IntegerField("opptaksår")
	ugjeng = models.IntegerField("undergjeng",choices=UGJENGER)
	status = models.IntegerField(choices=STATUSER)
	portrett = models.ImageField(default='portretter/katt.png',upload_to='portretter/')
	telefon = models.CharField("telefonnummer",max_length=8)
	epost = models.EmailField("e-postadresse",max_length=60)
	studium = models.CharField(max_length=30)
	jobb = models.CharField(blank=True,max_length=30)
	kallenavn = models.CharField(blank=True,max_length=30)
	class Meta:
		verbose_name_plural = "medlemmer"
		ordering = ['etternavn','fornavn']
	def __str__(self):
		return self.fornavn+(" "+self.mellomnavn if self.mellomnavn else "")+" "+self.etternavn
	def get_absolute_url(self):
		return reverse('medlem_profil',kwargs={'mid':self.id})


class Sitat(models.Model):
	sitat = models.TextField(max_length=100)
	dato = models.DateField()
	kontekst = models.CharField(max_length=50)
	medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='sitater')
	class Meta:
		verbose_name_plural = "sitater"
		ordering = ['dato']


class Utmerkelse(models.Model):
	UTYPER = ((1,'ridder'),(2,'kommandør'),(3,'storkors'))
	ORDENER = ((1,'Den Gyldne Kat'),(2,'De Sorte Faars Ridderskab'),(3,'Den Træge Patron'),(4,'Polyhymnia'),(5,"Vrangstrupen"),(6,"Minerva Polyhymnia"))
	utype = models.IntegerField("utmerkelsestype",choices=UTYPER)
	orden = models.IntegerField(choices=ORDENER,default=1)
	dato = models.DateField()
	medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='utmerkelser')
	def tittel(self):
		return self.get_utype_display()+" av "+self.get_orden_display()+" fra "+str(self.dato.year)
	class Meta:
		verbose_name_plural = "utmerkelser"
		ordering = ['dato']
	def __str__(self):
		return str(self.medlem)+" som "+self.tittel()


class Verv(models.Model):
	VTYPER = ((1,'styreverv'),(2,'ansvarsverv'),(3,'produksjonsverv_med_erfaringsskriv'),(4,'produksjonsverv_uten_erfaringsskriv'))
	vtype = models.IntegerField("vervtype",choices=VTYPER)
	tittel = models.CharField(max_length=50)
	info = models.TextField("beskrivelse",blank=True)
	instruks = models.TextField(blank=True)
	def plural(self):
		if tittel[-2:] == "er":
			return self.tittel+"e"
		else:
			return self.tittel+"er"
	class Meta:
		verbose_name_plural = "verv"
		ordering = ['vtype','tittel']
	def __str__(self):
		return self.tittel


class Produksjon(models.Model):
	PTYPER = ((1,'SIT'),(2,'AFEI'),(3,'UKA'))
	ptype = models.IntegerField("produksjonstype",choices=PTYPER,default=1)
	revy = models.BooleanField(default=False)
	tittel = models.CharField(max_length=50)
	info = models.TextField("beskrivelse")
	memo = models.TextField("kommentar",blank=True)
	forfatter = models.CharField(max_length=100)
	opphav = models.IntegerField("opphavsår")
	varighet = models.CharField(blank=True,max_length=22)
	premiere = models.DateTimeField()
	lokale = models.CharField(max_length=50)
	banner = models.ImageField(default='bannere/banner.png',upload_to='bannere/')
	plakat = models.ImageField(default='plakater/plakat.png',upload_to='plakater/')
	program = models.FileField(blank=True,upload_to='programmer/')
	film = models.FileField(blank=True,upload_to='filmer/')
	blestestart = models.DateField("blæstestart",blank=True,null=True) 
	FBlink = models.CharField("Facebook-link",blank=True,max_length=100)
	billettlink = models.CharField(blank=True,max_length=100)
	def semester(self):
		return ("V" if self.premiere.month < 7 else "H")+str(self.premiere.year)
	class Meta:
		verbose_name_plural = "produksjoner"
		ordering = ['ptype','premiere']
	def __str__(self):
		return self.tittel+" ("+self.semester()+")"
	def get_absolute_url(self):
		return reverse('produksjon_profil',kwargs={'pid':self.id})


class Forestilling(models.Model):
	tidspunkt = models.DateTimeField()
	produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='forestillinger')
	class Meta:
		verbose_name_plural = "forestillinger"
		ordering = ['tidspunkt']


class Anmeldelse(models.Model):
	forfatter = models.CharField(max_length=50)
	medium = models.CharField(max_length=50)
	dato = models.DateField()
	tekst = models.FileField(upload_to='anmeldelser/')
	utdrag = models.TextField(blank=True)
	produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='anmeldelser')
	class Meta:
		verbose_name_plural = "anmeldelser"
		ordering = ['dato']


class Arrangement(models.Model):
	ATYPER = ((1,'internt'),(2,'eksternt'))
	atype = models.IntegerField("arrangementtype",choices=ATYPER)
	tittel = models.CharField(max_length=50)
	info = models.TextField("beskrivelse")
	memo = models.TextField("kommentar",blank=True)
	tidspunkt = models.DateTimeField()
	varighet = models.CharField(blank=True,max_length=22)
	lokale = models.CharField(max_length=10)
	banner = models.ImageField(default='banner.png',upload_to='bannere/')
	class Meta:
		verbose_name_plural = "arrangementer"
		ordering = ['tidspunkt','tittel']
	def __str__(self):
		return self.tittel


class Foto(models.Model):
	FTYPER = ((1,'scene'),(2,'kostyme'),(3,'kulisse'),(4,'arbeid'),(5,'gruppe'),(6,'arrangement'),(7,'sosialt'))
	ftype = models.IntegerField("fototype",choices=FTYPER)
	FG = models.BooleanField()
	FGlink = models.CharField("FG-link",blank=True,max_length=100)
	foto = models.ImageField(blank=True,upload_to='bilder/')
	produksjon = models.ForeignKey(Produksjon,models.CASCADE,blank=True,null=True,related_name='bilder')
	arrangement = models.ForeignKey(Arrangement,models.CASCADE,blank=True,null=True,related_name='bilder')
	dato = models.DateField(blank=True,null=True)
	kontekst = models.TextField()
	class Meta:
		verbose_name_plural = "fotoer"
		ordering = ['ftype']


class Erfaring(models.Model):
	medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='erfaringer')
	verv = models.ForeignKey(Verv,models.CASCADE,related_name='erfaringer')
	produksjon = models.ForeignKey(Produksjon,models.CASCADE,blank=True,null=True,related_name='erfaringer')
	ar = models.IntegerField("år",blank=True,null=True)
	rolle = models.CharField(blank=True,max_length=30)
	skriv = models.FileField("erfaringsskriv",blank=True,upload_to='erfaringsskriv/')
	def tittel(self):
		if self.verv.vtype <= 2:
			return str(self.verv)+" i "+str(self.ar)
		elif self.verv.vtype == 3:
			return str(self.verv)+" for "+str(self.produksjon)
		else:
			return str(self.verv)+(" ("+self.rolle+")" if self.rolle else "")+" i "+str(self.produksjon)
	class Meta:
		verbose_name_plural = "erfaringer"
		ordering = ['ar','produksjon__premiere','verv__vtype','verv__tittel']
	def __str__(self):
		return str(self.medlem)+" som "+self.tittel()