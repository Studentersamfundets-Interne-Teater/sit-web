from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

import datetime

def verbose_date(date):
# lager en dato-string på formen "15. februar 2021".
    dato = str(date.day)+". "
    dato += settings.MONTH_NAMES[date.month]+" "
    dato += str(date.year)
    return dato

def verbose_datetime(datetime):
# lager en tidspunkt-string på formen "15. februar 2021 klokka 15.15".
    tidspunkt = verbose_date(datetime.date())
    tidspunkt += " klokka "
    tidspunkt += str(datetime.hour)+"."
    if datetime.minute < 10:
        tidspunkt += "0"
    tidspunkt += str(datetime.minute)
    return tidspunkt

def verbose_date_span(date1, date2):
# lager en periode-string på formen "15.–16. februar"/"15. januar – 16. februar".
    if date1.month == date2.month:
        datoer = str(date1.day)+".–"+str(date2.day)+". "
        datoer += settings.MONTH_NAMES[date1.month]
    else:
        datoer = str(date1.day)+". "
        datoer += settings.MONTH_NAMES[date1.month]+" – "
        datoer += str(date2.day)+". "
        datoer += settings.MONTH_NAMES[date2.month]
    return datoer


class Medlem(models.Model):
    MEDLEMSTYPER = ((1,'SIT'),(2,'Regi'),(3,'FK'),(4,'VK'),
        (5,'SO'),(6,'TSS'),(7,'TKS'),(8,'SPO'),(9,'UKA'),(10,'ISFiT'),
        (11,'MG'),(12,'ITK'),(13,'ARK'),(14,'FG'),(15,'KSG'),
        (16,'KU'),(17,'KLST'),(18,'LØK'),(19,'DG'),(20,'SM'),(21,'Profil'),(22,'ekstern'))
    medlemstype = models.IntegerField(choices=MEDLEMSTYPER,default=1)
    fornavn = models.CharField(max_length=100)
    mellomnavn = models.CharField(blank=True,max_length=100)
    etternavn = models.CharField(max_length=100)
    fodselsdato = models.DateField("fødselsdato",blank=True,null=True)
    opptaksar = models.IntegerField("opptaksår",blank=True,null=True)
    UNDERGJENGER = ((1,'Kostyme'),(2,'Kulisse'),(3,'Skuespill'))
    undergjeng = models.IntegerField(choices=UNDERGJENGER,blank=True,null=True)
    STATUSER = ((1,'aktiv'),(2,'veteran'),(3,'pangsjonist'),(4,'inaktiv'))
    status = models.IntegerField(choices=STATUSER,blank=True,null=True)
    portrett = models.ImageField(upload_to='portretter/',default='/default/katt.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    offentlig_portrett = models.BooleanField(blank=True,default=False) # avgjør om portrettet skal vises offentlig eller kun for interne. 
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
        ordering = ['medlemstype','-opptaksar','undergjeng','etternavn','fornavn']
    def __str__(self):
        return self.fornavn+(" "+self.mellomnavn if self.mellomnavn else "")+" "+self.etternavn
    def get_absolute_url(self):
        return reverse('medlem_info',kwargs={'mid':self.id})


class Sitat(models.Model):
# holder artige sitater gjort av medlemmer.
    medlem = models.ForeignKey(Medlem,models.CASCADE,related_name='sitater')
    utsagn = models.TextField() # holder selve sitatet.
    kontekst = models.TextField() # holder kontekst for sitatet (når, hvor, utdypende, ...).
    class Meta:
        verbose_name_plural = "sitater"
    def __str__(self):
        return str(self.medlem)+" "+self.kontekst


class Utmerkelse(models.Model):
# holder utmerkelser gitt til medlemmer.
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
        ordering = ['orden','-ar','tittel']
    def __str__(self):
        return str(self.medlem)+" som "+self.full_tittel()


class Vervtag(models.Model):
# holder klassifiseringer for verv (feks prodapp, øvapp, kunstnerisk forum, kulisse, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name_plural = "vervtags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Verv(models.Model):
    VERVTYPER = ((1,'styre'),(2,'ekstern-gjeng'),(3,'intern-gjeng'),(4,'produksjons'))
    # Typene 'ekstern-gjeng' og 'intern-gjeng' er ment for årsvervene som velges på genfors (utenom Styret).
    # 'ekstern-gjeng' dukker opp på den offentlige kontaktsida, mens 'intern-gjeng' kun dukker opp når man er logga inn.
    vervtype = models.IntegerField(choices=VERVTYPER)
    vervtags = models.ManyToManyField(Vervtag,blank=True)
    tittel = models.CharField(max_length=100)
    erfaringsoverforing = models.BooleanField("erfaringsoverføring") # avgjør om vervet skal ha en egen infoside med mulighet for erfaringsskriv.
    epost = models.EmailField("e-postadresse",blank=True,max_length=60) # holder en eventuell e-postadresse for alle med vervet.
    henvendelser = models.CharField(blank=True,max_length=100) # holder en liste over hvilke henvendelser gjengvervet tar imot (til kontaktsida).
    instruks = models.TextField(blank=True) # holder en eventuell instruksfesta beskrivelse av vervet.
    beskrivelse = models.TextField(blank=True) # holder en eventuell grundigere beskrivelse av vervet.
    def plural(self): # bøyer vervnavnet i flertall (til listevisninger).
        if self.tittel[:10] == "medlem av ":
            return self.tittel[10:]
        elif self.tittel[-6:] == "medlem":
            return self.tittel+"mer"
        elif self.tittel[-7:] == "gjengis":
            return self.tittel[:-2]+"en"
        elif self.tittel[-9:] == "ansvarlig":
            return self.tittel+"e"
        elif self.tittel[-2:] == "er":
            return self.tittel+"e"
        elif self.tittel[-1:] == "e":
            return self.tittel+"r"
        else:
            return self.tittel+"er"
    class Meta:
        verbose_name_plural = "verv"
        ordering = ['vervtype','erfaringsoverforing','tittel']
    def __str__(self):
        return self.tittel
    def get_absolute_url(self):
        return reverse('verv_info',kwargs={'vid':self.id})


class Lokale(models.Model):
    navn = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "lokaler"
        ordering = ['navn']
    def __str__(self):
        return self.navn


class Produksjonstag(models.Model):
# holder klassifiseringer for produksjoner (feks komedie, tragedie, musikal, revy, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name_plural = "produksjonstags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Produksjon(models.Model):
    PRODUKSJONSTYPER = ((1,'SIT'),(2,'KUP'),(3,'AFEI'),(4,'UKA'),(5,'ISFiT'))
    produksjonstype = models.IntegerField(choices=PRODUKSJONSTYPER,default=1)
    produksjonstags = models.ManyToManyField(Produksjonstag,blank=True)
    tittel = models.CharField(max_length=100)
    forfatter = models.CharField(blank=True,max_length=200)
    opphavsar = models.IntegerField("opphavsår", blank=True, null=True)
    premieredato = models.DateField()
    varighet = models.CharField(blank=True,max_length=100)
    lokale = models.ManyToManyField(Lokale,related_name="produksjoner")
    banner = models.ImageField(upload_to='bannere/',default='/default/katter.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    plakat = models.ImageField(upload_to='plakater/',blank=True)
    program = models.FileField(upload_to='programmer/',blank=True)
    manus = models.FileField(upload_to='manus/',blank=True) # holder ei PDF-fil med fullt manus for forestillinga.
    partitur = models.FileField(upload_to='partitur/',blank=True) # holder ei PDF-fil med fullt partitur for forestillinga.
    visehefte = models.FileField(upload_to='visehefter/',blank=True) # holder ei PDF-fil med et eventuelt allsangvennlig visehefte fra forestillinga.
    beskrivelse = models.TextField(blank=True) # holder en beskrivelse av produksjonen for eksterne lesere.
    anekdoter = models.TextField(blank=True) # holder ytterligere anekdoter for interne lesere. 
    reklame = models.TextField(blank=True) # holder en reklametekst til bruk på forsida.
    pris = models.IntegerField(blank=True,null=True) # holder billettpris for eksterne.
    medlemspris = models.IntegerField(blank=True,null=True) # holder billettpris for medlemmer av Samfundet.
    billettlink = models.CharField(blank=True,max_length=200) # holder en link til kjøp av billetter.
    blestestart = models.DateField("blæstestart",blank=True,null=True) # holder datoen da forsida skal begynne å reklamere for produksjonen.
    FBlink = models.CharField("Facebook-link",blank=True,max_length=200) # holder en link til Facebook-arrangement.
    def semester(self): # lager en semesterkode av typen 'H2020'.
        return ("V" if self.premieredato.month < 7 else "H")+str(self.premieredato.year)
    def spilleperiode(self): # lager en spilleperiode-string på formen "15.–16. februar"/"15. januar – 16. februar".
        if self.forestillinger.count() > 1:
            forste_dato = self.forestillinger.first().tidspunkt.date()
            siste_dato = self.forestillinger.last().tidspunkt.date()
            datoer = verbose_date_span(forste_dato,siste_dato)
        else:
            datoer = verbose_date(self.premieredato)[:-4]
        return datoer
    def full_premieredato(self): # lager en premieredato-string på formen "15. februar 2021" hvis datoen er kjent, ellers "Ukjent".
        if ((self.premieredato.month == 1 or self.premieredato.month == 7) and self.premieredato.day == 1) or (self.premieredato.month == 12 and self.premieredato.day == 24):
            return "Ukjent"
        else:
            return verbose_date(self.premieredato)
    class Meta:
        verbose_name_plural = "produksjoner"
        ordering = ['-premieredato','produksjonstype','tittel']
    def __str__(self):
        return self.tittel+" ("+self.semester()+")"
    def get_absolute_url(self):
        return reverse('produksjon_info',kwargs={'pid':self.id})


class Forestilling(models.Model):
# holder forestillingstidspunktene for en gitt produksjon.
    produksjon = models.ForeignKey(Produksjon,models.CASCADE,related_name='forestillinger')
    tidspunkt = models.DateTimeField()
    def fullt_tidspunkt(self): # lager en tidspunkt-string på formen "15. februar 2021 klokka 15.15".
        return verbose_datetime(self.tidspunkt)
    class Meta:
        verbose_name_plural = "forestillinger"
        ordering = ['tidspunkt']
    def __str__(self):
        return str(self.produksjon)+" den "+self.fullt_tidspunkt()


class Nummer(models.Model):
# holder spesielle utdrag fra en produksjon (sang, monolog, sketsj, ...).
    produksjon = models.ForeignKey(Produksjon,models.PROTECT,related_name='numre')
    tittel = models.CharField(max_length=100)
    manus = models.TextField() # holder manus for nummeret.
    noter = models.FileField(upload_to='noter/',blank=True) # holder eventuelle noter for nummeret.
    beskrivelse = models.TextField(blank=True) # holder en beskrivelse av nummeret for eksterne lesere.
    anekdoter = models.TextField(blank=True) # holder ytterligere anekdoter for interne lesere.
    class Meta:
        verbose_name_plural = "numre"
        ordering = ['-produksjon__premieredato','tittel']
    def __str__(self):
        return '"'+self.tittel+'"'+" fra "+str(self.produksjon)


class Anmeldelse(models.Model):
# holder anmeldelser av produksjoner.
    produksjon = models.ForeignKey(Produksjon,models.PROTECT,related_name='anmeldelser')
    forfatter = models.CharField(max_length=200)
    medium = models.CharField(max_length=100) # holder mediet der anmeldelsen ble publisert (avis, nettside, ...).
    offentlig = models.BooleanField() # avgjør om hele anmeldelsen skal ligge offentlig eller kun for interne.
    fil = models.FileField(upload_to='anmeldelser/') # holder ei PDF-fil med den fulle anmeldelsen. 
    utdrag = models.TextField() # holder et utdrag av anmeldelsen for eksterne lesere.
    class Meta:
        verbose_name_plural = "anmeldelser"
        ordering = ['forfatter','-produksjon__premieredato']
    def __str__(self):
        return self.forfatter+" om "+str(self.produksjon)


class Erfaring(models.Model):
# holder konkrete erfaringer gjort av medlemmer i rollen som et gitt verv for en gitt produksjon.
    medlem = models.ForeignKey(Medlem,models.PROTECT,blank=True,null=True,related_name='erfaringer')
    navn = models.CharField(blank=True,max_length=200) # holder et eventuelt eksternt navn hvis personen ikke er lagra i databasen.
    verv = models.ForeignKey(Verv,models.PROTECT,blank=True,null=True,related_name='erfaringer')
    tittel = models.CharField(blank=True,max_length=100) # holder en eventuell spesiell tittel hvis vervet ikke er lagra i databasen.
    produksjon = models.ForeignKey(Produksjon,models.PROTECT,blank=True,null=True,related_name='erfaringer')
    ar = models.IntegerField("år",blank=True,null=True) # holder et eventuelt år hvis vervet ikke er knytta til en produksjon.
    rolle = models.CharField(blank=True,max_length=100) # holder en utdypende rolle innafor vervet (feks Melchior Gabor, gitar, arbeidsleder eller konsulent).
    erfaringsskriv = models.FileField(upload_to='erfaringsskriv/',blank=True) # holder et eventuelt erfaringsskriv.
    def full_tittel(self): # lager en full tittel for erfaringa på formen "skuespiller ("Melchior Gabor") i Spring Awakening (H2020)".
        tittel = (str(self.verv) if self.verv else self.tittel)
        tittel += (" ("+self.rolle+")" if self.rolle else "")
        tittel += " i "+(str(self.produksjon) if self.produksjon else str(self.ar))
        return tittel
    class Meta:
        verbose_name_plural = "erfaringer"
        ordering = ['-produksjon__premieredato','-ar','verv__vervtype','verv__erfaringsoverforing','verv__tittel','tittel','medlem__etternavn','navn']
    def __str__(self):
        return (str(self.medlem) if self.medlem else self.navn)+" som "+self.full_tittel()


class Arrangement(models.Model):
# holder interne eller eksterne arrangementer som skal vises på forsida (feks kostymesalg, vårball, genfors, ...).
    arrangorer = models.ManyToManyField(Verv,verbose_name="arrangører",blank=True) # holder vervene som skal kunne redigere arrangementet.
    tittel = models.CharField(max_length=100)
    offentlig = models.BooleanField(default=False) # avgjør om arrangementet skal ligge offentlig eller kun for interne.
    tidspunkt = models.DateTimeField()
    varighet = models.CharField(blank=True,max_length=100)
    lokale = models.ForeignKey(Lokale,models.PROTECT,related_name="arrangementer")
    banner = models.ImageField(upload_to='bannere/',default='default/katter.png') # holder et bilde til bruk på forsida, i listevisninger og så videre.
    beskrivelse = models.TextField(blank=True) # holder en beskrivelse av arrangementet for eksterne lesere.
    anekdoter = models.TextField(blank=True) # holder ytterligere anekdoter for interne lesere.
    reklame = models.TextField(blank=True) # holder en reklametekst til bruk på forsida.
    blestestart = models.DateField("blæstestart (på forsida)",blank=True,null=True) # avgjør datoen da forsida skal begynne å reklamere for arrangementet.
    FBlink = models.CharField("Facebook-link",blank=True,max_length=200) # holder en link til et eventuelt Facebook-arrangement.
    def semester(self): # lager en semesterkode på formen 'H2020'.
        return ("V" if self.tidspunkt.month < 7 else "H")+str(self.tidspunkt.year)
    class Meta:
        verbose_name_plural = "arrangementer"
        ordering = ['-tidspunkt','tittel']
    def __str__(self):
        return self.tittel+" ("+self.semester()+")"


class Hendelse(models.Model):
# holder mindre hendelser som vises sammen med produksjoner, arrangementer og bilder på arkivsida.
    tittel = models.CharField(max_length=100)
    dato = models.DateField()
    beskrivelse = models.TextField()
    class Meta:
        verbose_name_plural = "hendelser"
        ordering = ['-dato','tittel']
    def __str__(self):
        return self.tittel


class Foto(models.Model):
# holder bilder fra produksjoner, numre, arrangementer eller sosiale sammenkomster.
    FOTOTYPER = ((1,'scene'),(2,'kostyme'),(3,'kulisse'),(4,'arbeid'),(5,'dalje'),
        (6,'arrangement'),(7,'gruppe'),(8,'sosialt'))
    # Typen 'scene' er ment for bilder fra forestilling, mens typene 'kostyme' og 'kulisse' er ment for nærbilder av kostymer eller kulisser.
    # Typen 'arbeid' er ment for bilder av sying, bygging, øving eller møter.
    # Typen 'gruppe' er ment for portrett- eller gruppebilder tatt av FG (feks gjengfoto, prodapp-bilde, bandbilde, ...).
    fototype = models.IntegerField(choices=FOTOTYPER)
    fotograf = models.CharField(blank=True,max_length=200)
    offentlig = models.BooleanField(default=True) # avgjør om bildet skal ligge offentlig eller kun for interne.
    medlemmer = models.ManyToManyField(Medlem,blank=True) # holder ei eventuell liste over medlemmene som er med i fotoet.
    produksjon = models.ForeignKey(Produksjon,models.PROTECT,blank=True,null=True,related_name='bilder')
    nummer = models.ForeignKey(Nummer,models.PROTECT,blank=True,null=True,related_name='bilder')
    arrangement = models.ForeignKey(Arrangement,models.PROTECT,blank=True,null=True,related_name='bilder')
    dato = models.DateField(blank=True,null=True) # holder en eventuell dato hvis bildet ikke er knytta til en produksjon, et nummer eller et arrangement.
    FGlink = models.CharField("FG-link",blank=True,max_length=200) # holder en link til bildet i Fotogjengens arkiv.
    fil = models.ImageField(upload_to='bilder/',blank=True) # holder ei eventuell fil hvis bildet ikke er fra Fotogjengen.
    kontekst = models.TextField() # holder en infotekst til bildet (hva, når, hvor, utdypende, ...).
    class Meta:
        verbose_name_plural = "fotoer"
        ordering = ['-produksjon__premieredato','-arrangement__tidspunkt','-dato','fototype']
    def __str__(self):
        if (self.produksjon):
            return self.get_fototype_display()+"bilde fra "+str(self.produksjon)
        elif (self.nummer):
            return self.get_fototype_display()+"bilde fra nummeret "+str(self.nummer)
        elif (self.arrangement):
            return self.get_fototype_display()+"bilde fra "+str(self.arrangement)
        else:
            return self.get_fototype_display()+"bilde fra den "+verbose_date(self.dato)


class Opptak(models.Model):
# holder opptak fra produksjoner, numre, arrangementer eller sosiale sammenkomster.
    OPPTAKSTYPER = ((1,'video'),(2,'lyd'))
    opptakstype = models.IntegerField(choices=OPPTAKSTYPER)
    offentlig = models.BooleanField(default=True) # avgjør om opptaket skal ligge offentlig eller kun for interne.
    medlemmer = models.ManyToManyField(Medlem,blank=True) # holder ei eventuell liste over medlemmene som er med i opptaket.
    produksjon = models.ForeignKey(Produksjon,models.PROTECT,blank=True,null=True,related_name='opptak')
    nummer = models.ForeignKey(Nummer,models.PROTECT,blank=True,null=True,related_name='opptak')
    arrangement = models.ForeignKey(Arrangement,models.PROTECT,blank=True,null=True,related_name='opptak')
    dato = models.DateField(blank=True,null=True) # holder en eventuell dato hvis opptaket ikke er knytta til en produksjon, et nummer eller et arrangement.
    kilde = models.ForeignKey('self',models.PROTECT,blank=True,null=True,related_name='utdrag') # holder referanse til et eventuelt annet opptak som dette opptaket er utdrag fra.
    kildestart = models.TimeField(blank=True,null=True) # holder tida i kildeopptaket der det eventuelle utdraget starter.
    kildestopp = models.TimeField(blank=True,null=True) # holder tida i kildeopptaket der det eventuelle utdraget stopper.
    fil = models.FileField(upload_to='opptak/',blank=True) # holder selve fila med opptaket hvis opptaket ikke er et utdrag.
    kontekst = models.TextField() # holder en infotekst til opptaket (hva, når, hvor, utdypende, ...).
    class Meta:
        verbose_name_plural = "opptak"
        ordering = ['-produksjon__premieredato','-arrangement__tidspunkt','-dato','opptakstype']
    def __str__(self):
        if (self.produksjon):
            return self.get_opptakstype_display()+"opptak av "+str(self.produksjon)
        elif (self.nummer):
            return self.get_opptakstype_display()+"opptak av nummeret "+str(self.nummer)
        elif (self.arrangement):
            return self.get_opptakstype_display()+"opptak fra "+str(self.arrangement)
        else:
            return self.get_opptakstype_display()+"opptak fra den "+verbose_date(self.dato)


class Uttrykk(models.Model):
# holder forklaringer på ord og forkortelser for nye medlemmer (feks "MG", "SIGP", "Store Øvre", ...).
    tittel = models.CharField(max_length=100)
    beskrivelse = models.TextField()
    class Meta:
        verbose_name_plural = "uttrykk"
        ordering = ['tittel']
    def __str__(self):
        return self.tittel


class Dokumenttag(models.Model):
# holder klassifiseringer for dokumenter (feks referat, sjekkeblekke, instruks, ...).
    tag = models.CharField(max_length=60)
    class Meta:
        verbose_name_plural = "dokumenttags"
        ordering = ['tag']
    def __str__(self):
        return self.tag

class Dokument(models.Model):
# holder dokumenter og filer som ikke er knytta til noen av modellene ovafor (feks referater, sjekkeblekker, ...).
    dokumenttags = models.ManyToManyField(Dokumenttag,blank=True)
    tittel = models.CharField(max_length=100)
    dato = models.DateField()
    fil = models.FileField(upload_to='dokumenter/')
    class Meta:
        verbose_name_plural = "dokumenter"
        ordering = ['-dato','tittel']
    def __str__(self):
        return self.tittel+" ("+str(self.dato)+")"


class Ar(models.Model):
# holder datoer, tekster og innstillinger for et bestemt år, som årets styre kan kontrollere.
    arstall = models.IntegerField("årstall",primary_key=True)
    gjengfoto = models.ForeignKey(Foto,models.PROTECT,blank=True,null=True,related_name="ar") # holder et eventuelt gjengfoto av årets SIT.
    styrebilde = models.ImageField(upload_to='styrebilder/',blank=True) # holder et gruppebilde av årets styre.
    forsidetittel = models.CharField(blank=True,max_length=200) # holder en eventuell tittel som ligger ute på forsida.
    forsidebilde = models.ForeignKey(Foto,models.PROTECT,blank=True,null=True,related_name="forsider") # holder et eventuelt bilde som ligger ute på forsida.
    forsidetekst = models.TextField(blank=True) # holder en eventuell tekst som ligger ute på forsida.
    opptaksstart = models.DateField(blank=True,null=True) # holder datoen da forsida skal begynne å reklamere for opptak.
    soknadsfrist = models.DateTimeField("søknadsfrist",blank=True,null=True) # holder årets tidsfrist for å søke SIT.
    opptakstekst_kostyme = models.TextField("opptakstekst (kostyme)",blank=True) # holder opptaksteksten for kostyme som ligger ute på opptakssida.
    opptaksbilde_kostyme = models.ForeignKey(Foto,models.PROTECT,verbose_name="opptaksbilde (kostyme)",blank=True,null=True,related_name="kostymeopptaksar") # holder et bilde til opptaksteksten for kostyme.
    opptakstekst_kulisse = models.TextField("opptakstekst (kulisse)",blank=True) # holder opptaksteksten for kulisse som ligger ute på opptakssida.
    opptaksbilde_kulisse = models.ForeignKey(Foto,models.PROTECT,verbose_name="opptaksbilde (kulisse)",blank=True,null=True,related_name="kulisseopptaksar") # holder et bilde til opptaksteksten for kulisse.
    opptakstekst_skuespill = models.TextField("opptakstekst (skuespill)",blank=True) # holder opptaksteksten for skuespill som ligger ute på opptakssida.
    opptaksbilde_skuespill = models.ForeignKey(Foto,models.PROTECT,verbose_name="opptaksbilde (skuespill)",blank=True,null=True,related_name="skuespillopptaksar") # holder et bilde til opptaksteksten for skuespill.
    opptakstekst_annet = models.TextField("opptakstekst (annet)",blank=True) # holder opptaksteksten for andre ansvar som ligger ute på opptakssida.
    opptaksbilde_annet = models.ForeignKey(Foto,models.PROTECT,verbose_name="opptaksbilde (annet)",blank=True,null=True,related_name="annetopptaksar") # holder et bilde til opptaksteksten for andre ansvar.
    varmotestart = models.DateField("vårmøtestart",blank=True,null=True) # holder datoen for vårens første mandagsmøte.
    varmotestopp = models.DateField("vårmøtestopp",blank=True,null=True) # holder datoen for vårens siste mandagsmøte.
    hostmotestart = models.DateField("høstmøtestart",blank=True,null=True) # holder datoen for høstens første mandagsmøte.
    hostmotestopp = models.DateField("høstmøtestopp",blank=True,null=True) # holder datoen for høstens siste mandagsmøte.
    genforstidspunkt = models.DateTimeField(blank=True,null=True) # holder tidspunkt for årets generalforsamling.
    class Meta:
        verbose_name = "år"
        verbose_name_plural = "år"
        ordering = ['-arstall']
    def __str__(self):
        return str(self.arstall)
    def get_absolute_url(self):
        return reverse('ar_info',kwargs={'arstall':self.arstall})