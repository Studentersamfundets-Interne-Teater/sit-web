from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import datetime


class Medlem(models.Model):
    MTYPER = ((1,'SIT'),(2,'Regi'),(3,'FK'),(4,'VK'),
        (5,'SO'),(6,'TSS'),(7,'TKS'),(8,'SPO'),(9,'UKA'),(10,'ISFiT'),
        (11,'MG'),(12,'ITK'),(13,'ARK'),(14,'FG'),(15,'KSG'),
        (16,'KU'),(17,'KLST'),(18,'LØK'),(19,'DG'),(20,'Profil'),(21,'ekstern'))
    mtype = models.IntegerField("medlemstype",choices=MTYPER,default=1)
    fornavn = models.CharField(max_length=100)
    mellomnavn = models.CharField(blank=True,max_length=100)
    etternavn = models.CharField(max_length=100)
    fodselsdato = models.DateField("fødselsdato",blank=True,null=True)
    opptaksar = models.IntegerField("opptaksår",blank=True,null=True)
    UNDERGJENGER = ((1,'Kostyme'),(2,'Kulisse'),(3,'Skuespill'))
    undergjeng = models.IntegerField(choices=UNDERGJENGER,blank=True,null=True)
    STATUSER = ((1,'aktiv'),(2,'veteran'),(3,'pangsionist'),(4,'inaktiv'))
    status = models.IntegerField(choices=STATUSER,blank=True,null=True)
    portrett = models.ImageField(upload_to='portretter/',default='/default/katt.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    kallenavn = models.CharField(blank=True,max_length=100)
    telefon = models.CharField("telefonnummer",blank=True,max_length=100)
    epost = models.EmailField("e-postadresse",blank=True,max_length=100)
    studium = models.CharField(blank=True,max_length=200)
    jobb = models.CharField(blank=True,max_length=200)
    brukerkonto = models.OneToOneField(User,models.SET_NULL,blank=True,null=True)
    def brukernavn(self): # lager et brukernavn ut ifra navn på formen 'jonfla93'.
        return (self.fornavn[:3]+self.etternavn[:3]).lower()+str(self.opptaksar)[2:]
    class Meta:
        verbose_name_plural = "medlemmer"
        ordering = ['mtype','-opptaksar','undergjeng','etternavn','fornavn']
    def __str__(self):
        return self.fornavn+(" "+self.mellomnavn if self.mellomnavn else "")+" "+self.etternavn
    def get_absolute_url(self):
        return reverse('medlem_info',kwargs={'mid':self.id})


class Sitat(models.Model): # holder artige sitater gjort av medlemmer.
    medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='sitater')
    tekst = models.TextField() # holder selve sitatet.
    kontekst = models.TextField() # holder kontekst for sitatet (når, hvor, utdypende, ...).
    class Meta:
        verbose_name_plural = "sitater"
    def __str__(self):
        return str(self.medlem)+" "+self.kontekst


class Utmerkelse(models.Model): # holder utmerkelser gitt til medlemmer.
    medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='utmerkelser')
    TITLER = ((1,'ridder'),(2,'kommandør'),(3,'storkors'))
    tittel = models.IntegerField(choices=TITLER)
    ORDENER = ((1,'Den Gyldne Kat'),(2,'De Sorte Faars Ridderskab'),(3,'Den Træge Patron'),(4,'Polyhymnia'),(5,"Vrangstrupen"),(6,"Minerva Polyhymnia"))
    orden = models.IntegerField(choices=ORDENER,default=1)
    ar = models.IntegerField("år")
    def full_tittel(self): # lager en full tittel på utmerkelsen av typen "ridder av Den Gyldne Kat fra 2015".
        return self.get_tittel_display()+" av "+self.get_orden_display()+" fra "+str(self.ar)
    class Meta:
        verbose_name_plural = "utmerkelser"
        ordering = ['ar','orden','tittel']
    def __str__(self):
        return str(self.medlem)+" som "+self.full_tittel()


class vTag(models.Model): # holder klassifiseringer for verv (feks prodapp, øvapp, kunstnerisk forum, kulisse, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name = "vervtag"
        verbose_name_plural = "vervtags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Verv(models.Model):
    VTYPER = ((1,'styre'),(2,'ekstern-gjeng'),(3,'intern-gjeng'),(4,'produksjons'))
    # Typen 'gjeng' er ment for årsvervene som velges på genfors (utenom Styret).
    vtype = models.IntegerField("vervtype",choices=VTYPER)
    vtags = models.ManyToManyField(vTag,"vervtags",blank=True)
    tittel = models.CharField(max_length=100)
    erfaringsoverforing = models.BooleanField("erfaringsoverføring") # avgjør om vervet skal ha en egen infoside med mulighet for erfaringsskriv.
    epost = models.EmailField("e-postadresse",blank=True,max_length=60) # holder en eventuell e-postadresse for alle med vervet.
    henvendelser = models.CharField(blank=True,max_length=100) # holder en liste over hvilke henvendelser gjengvervet tar imot (til kontaktsida).
    instruks = models.TextField(blank=True) # holder en eventuell instruksfesta beskrivelse av vervet.
    beskrivelse = models.TextField(blank=True) # holder en eventuell grundigere beskrivelse av vervet.
    def plural(self): # bøyer vervnavnet i flertall (til listevisninger).
        if self.tittel[-7:] == "gjengis":
            return self.tittel[:-2]+"en"
        elif self.tittel[-2:] == "er":
            return self.tittel+"e"
        else:
            return self.tittel+"er"
    class Meta:
        verbose_name_plural = "verv"
        ordering = ['vtype','erfaringsoverforing','tittel']
    def __str__(self):
        return self.tittel


class Lokale(models.Model):
    navn = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "lokaler"
        ordering = ['navn']
    def __str__(self):
        return self.navn


class pTag(models.Model): # holder klassifiseringer for produksjoner (feks komedie, tragedie, musikal, revy, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name = "produksjonstag"
        verbose_name_plural = "produksjonstags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Produksjon(models.Model):
    PTYPER = ((1,'SIT'),(2,'KUP'),(3,'AFEI'),(4,'UKA'))
    ptype = models.IntegerField("produksjonstype",choices=PTYPER,default=1)
    ptags = models.ManyToManyField(pTag,"produksjonstags",blank=True)
    tittel = models.CharField(max_length=100)
    forfatter = models.CharField(max_length=200)
    opphavsar = models.IntegerField("opphavsår", blank=True, null=True)
    premieredato = models.DateField()
    varighet = models.CharField(blank=True,max_length=100)
    lokale = models.ManyToManyField(Lokale,related_name="produksjoner")
    banner = models.ImageField(upload_to='bannere/',default='/default/katter.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    plakat = models.ImageField(upload_to='plakater/',blank=True)
    opptak = models.FileField(upload_to='opptak/',blank=True) # holder et eventuelt film- eller lydopptak av hele forestillinga.
    program = models.FileField(upload_to='programmer/',blank=True)
    manus = models.FileField(upload_to='manus/',blank=True) # holder ei PDF-fil med fullt manus for forestillinga.
    partitur = models.FileField(upload_to='partitur/',blank=True) # holder ei PDF-fil med fullt partitur for forestillinga.
    visehefte = models.FileField(upload_to='visehefter/',blank=True) # holder ei PDF-fil med et eventuelt allsangvennlig visehefte fra forestillinga.
    info = models.TextField("beskrivelse (for eksterne)",blank=True) # holder en beskrivelse av produksjonen for eksterne lesere.
    memo = models.TextField("ytterligere anekdoter (for interne)",blank=True) # holder ytterligere anekdoter for interne lesere. 
    blurb = models.TextField("blurb (til forsida)",blank=True) # holder en reklametekst til bruk på forsida.
    pris = models.IntegerField("billettpris (for ikke-medlemmer)",blank=True,null=True) # holder billettpris for eksterne.
    medlemspris = models.IntegerField("billettpris (for medlemmer)",blank=True,null=True) # holder billettpris for medlemmer av Samfundet.
    billettlink = models.CharField(blank=True,max_length=200) # holder en link til kjøp av billetter.
    blestestart = models.DateField("blæstestart (på forsida)",blank=True,null=True) # avgjør datoen da forsida skal begynne å reklamere for produksjonen.
    FBlink = models.CharField("Facebook-link",blank=True,max_length=200) # holder en link til Facebook-arrangement.
    def semester(self): # lager en semesterkode av typen 'H2020'.
        return ("V" if self.premieredato.month < 7 else "H")+str(self.premieredato.year)
    class Meta:
        verbose_name_plural = "produksjoner"
        ordering = ['premieredato','tittel']
    def __str__(self):
        return self.tittel+" ("+self.semester()+")"
    def get_absolute_url(self):
        return reverse('produksjon_info',kwargs={'pid':self.id})


class Forestilling(models.Model): # holder forestillingstidspunktene for en gitt produksjon.
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='forestillinger')
    tidspunkt = models.DateTimeField()
    class Meta:
        verbose_name_plural = "forestillinger"
        ordering = ['tidspunkt']
    def __str__(self):
        return str(self.produksjon)+" den "+str(self.tidspunkt)


class Nummer(models.Model): # holder spesielle utdrag fra en produksjon (sang, monolog, sketsj, ...).
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='numre')
    tittel = models.CharField(max_length=100)
    opptak = models.FileField(upload_to='opptak/',blank=True) # holder et eventuelt film- eller lydopptak av nummeret.
    tekst = models.TextField() # holder manus for nummeret.
    noter = models.FileField(upload_to='noter/',blank=True) # holder eventuelle noter for nummeret.
    info = models.TextField("beskrivelse (for eksterne)",blank=True) # holder en beskrivelse av nummeret for eksterne lesere.
    memo = models.TextField("ytterligere anekdoter (for interne)",blank=True) # holder ytterligere anekdoter for interne lesere.
    class Meta:
        verbose_name_plural = "numre"
        ordering = ['produksjon__premieredato','tittel']
    def __str__(self):
        return self.tittel


class Anmeldelse(models.Model): # holder anmeldelser av produksjoner.
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='anmeldelser')
    forfatter = models.CharField(max_length=200)
    medium = models.CharField(max_length=100) # holder mediet der anmeldelsen ble publisert (avis, nettside, ...).
    gratis = models.BooleanField() # avgjør om anmeldelsen skal være tilgjengelig for eksterne lesere.
    fil = models.FileField(upload_to='anmeldelser/') # holder ei PDF-fil med den fulle anmeldelsen. 
    utdrag = models.TextField() # holder et utdrag av anmeldelsen for eksterne lesere.
    class Meta:
        verbose_name_plural = "anmeldelser"
        ordering = ['produksjon__premieredato','forfatter']
    def __str__(self):
        return self.forfatter+" om "+str(self.produksjon)


class Erfaring(models.Model): # holder konkrete erfaringer gjort av medlemmer i rollen som et gitt verv for en gitt produksjon.
    medlem = models.ForeignKey(Medlem,models.CASCADE,blank=True,null=True,related_name='erfaringer')
    navn = models.CharField(blank=True,max_length=200) # holder et eventuelt eksternt navn hvis personen ikke er lagra i databasen.
    verv = models.ForeignKey(Verv,models.CASCADE,blank=True,null=True,related_name='erfaringer')
    tittel = models.CharField(blank=True,max_length=100) # holder en eventuell spesiell tittel hvis vervet ikke er lagra i databasen.
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,blank=True,null=True,related_name='erfaringer')
    ar = models.IntegerField("år",blank=True,null=True) # holder et eventuelt år hvis vervet ikke er knytta til en produksjon.
    rolle = models.CharField(blank=True,max_length=100) # holder en utdypende rolle innafor vervet (feks Melchior Gabor, gitar, arbeidsleder eller konsulent).
    skriv = models.FileField("erfaringsskriv",upload_to='erfaringsskriv/',blank=True) # holder et eventuelt erfaringsskriv.
    def full_tittel(self): # lager en full tittel for erfaringa av typen "skuespiller (Melchior Gabor) i Spring Awakening".
        if self.produksjon:
            if self.verv and self.verv.vtype == 3 and self.verv.erfaringsoverforing == True:
                return str(self.verv)+" for "+str(self.produksjon)
            else:
                return (str(self.verv) if self.verv else self.tittel)+(" ("+self.rolle+")" if self.rolle else "")+" i "+str(self.produksjon)
        else:
                return (str(self.verv) if self.verv else self.tittel)+" i "+str(self.ar)
    class Meta:
        verbose_name_plural = "erfaringer"
        ordering = ['produksjon__premieredato','ar','verv__vtype','verv__erfaringsoverforing','verv__tittel','tittel','medlem__etternavn','navn']
    def __str__(self):
        return (str(self.medlem) if self.medlem else self.navn)+" som "+self.full_tittel()


class Arrangement(models.Model): # holder interne eller eksterne arrangementer som skal vises på forsida (feks kostymesalg, vårball, genfors, ...).
    ATYPER = ((1,'internt'),(2,'eksternt')) # avgjør om arrangementet skal synes for eksterne lesere.
    atype = models.IntegerField("arrangementtype",choices=ATYPER)
    arrangører = models.ManyToManyField(Verv,blank=True) # holder vervene som skal kunne redigere arrangementet.
    tittel = models.CharField(max_length=100)
    tidspunkt = models.DateTimeField()
    varighet = models.CharField(blank=True,max_length=100)
    lokale = models.ForeignKey(Lokale,models.PROTECT,related_name="arrangementer")
    banner = models.ImageField(upload_to='bannere/',default='default/katter.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    info = models.TextField("beskrivelse (for eksterne)",blank=True) # holder en beskrivelse av arrangementet for eksterne lesere.
    memo = models.TextField("ytterligere anekdoter (for interne)",blank=True) # holder ytterligere anekdoter for interne lesere.
    blurb = models.TextField("blurb (til forsida)",blank=True) # holder en reklametekst til bruk på forsida.
    blestestart = models.DateField("blæstestart (på forsida)",blank=True,null=True) # avgjør datoen da forsida skal begynne å reklamere for arrangementet.
    FBlink = models.CharField("Facebook-link",blank=True,max_length=200) # holder en link til et eventuelt Facebook-arrangement.
    def semester(self): # lager en semesterkode av typen 'H2020'.
        return ("V" if self.tidspunkt.month < 7 else "H")+str(self.tidspunkt.year)
    class Meta:
        verbose_name_plural = "arrangementer"
        ordering = ['tidspunkt','tittel']
    def __str__(self):
        return self.tittel+" ("+self.semester()+")"


class Hendelse(models.Model): # holder mindre hendelser som vises sammen med produksjoner, arrangementer og bilder på arkivsida.
    tittel = models.CharField(max_length=100)
    dato = models.DateField()
    beskrivelse = models.TextField()
    class Meta:
        verbose_name_plural = "hendelser"
        ordering = ['dato','tittel']
    def __str__(self):
        return self.tittel


class Foto(models.Model): # holder bilder fra produksjoner, arrangementer eller sosiale sammenkomster.
    FTYPER = ((1,'scene'),(2,'kostyme'),(3,'kulisse'),(4,'arbeid'),(5,'gruppe'),(6,'arrangement'),(7,'sosialt'))
    # Typen 'scene' er ment for bilder fra forestilling, mens typene 'kostyme' og 'kulisse' er ment for nærbilder av kostymer eller kulisser.
    # Typen 'arbeid' er ment for bilder av sying, bygging, øving eller møter.
    # Typen 'gruppe' er ment for portrett- eller gruppebilder tatt av FG (feks prodapp-bilde, bandbilde, ...).
    ftype = models.IntegerField("fototype",choices=FTYPER)
    medlemmer = models.ManyToManyField(Medlem,blank=True) # holder ei eventuell liste over medlemmene som er avbilda.
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,blank=True,null=True,related_name='bilder')
    arrangement = models.ForeignKey(Arrangement,models.CASCADE,blank=True,null=True,related_name='bilder')
    dato = models.DateField(blank=True,null=True) # holder en eventuell dato hvis bildet ikke er knytta til en produksjon eller et arrangement.
    FGlink = models.CharField("FG-link",blank=True,max_length=200) # holder en link til bildet i Fotogjengens arkiv.
    fil = models.ImageField(upload_to='bilder/',blank=True) # holder ei eventuell fil hvis bildet ikke er fra Fotogjengen.
    kontekst = models.TextField() # holder en bildetekst til bildet (hva, når, hvor, utdypende, ...).
    class Meta:
        verbose_name_plural = "fotoer"
        ordering = ['ftype','produksjon__premieredato','arrangement__tidspunkt','dato']
    def __str__(self):
        if (self.produksjon):
            return self.get_ftype_display()+"bilde fra "+str(self.produksjon)
        elif (self.arrangement):
            return self.get_ftype_display()+"bilde fra "+str(self.arrangement)
        else:
            return self.get_ftype_display()+"bilde fra den"+str(self.dato)


class Uttrykk(models.Model): # holder forklaringer på ord og forkortelser for nye medlemmer (feks "MG", "SIGP", "Store Øvre", ...).
    tittel = models.CharField(max_length=100)
    beskrivelse = models.TextField()
    class Meta:
        verbose_name_plural = "uttrykk"
        ordering = ['tittel']
    def __str__(self):
        return self.tittel


class dTag(models.Model): # holder klassifiseringer for dokumenter (feks referat, sjekkeblekke, instruks, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name = "dokumenttag"
        verbose_name_plural = "dokumenttags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Dokument(models.Model): # holder dokumenter og filer som ikke er knytta til noen av modellene ovafor (feks referater, sjekkeblekker, ...).
    dtags = models.ManyToManyField(dTag,"dokumenttags",blank=True)
    tittel = models.CharField(max_length=100)
    dato = models.DateField()
    fil = models.FileField(upload_to='dokumenter/')
    class Meta:
        verbose_name_plural = "dokumenter"
        ordering = ['dato','tittel']
    def __str__(self):
        return self.tittel+" ("+str(self.dato)+")"